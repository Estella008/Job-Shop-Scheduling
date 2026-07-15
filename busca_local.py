

import copy
from avaliacao import soma_todas_duracoes, calcular_c_real, avaliar


def maquinas_do_job(rotas, job):
    
    return [maquina for (maquina, duracao) in rotas[job]]


def gerar_vizinhos_swap(solucao, maquina, job_critico):
    
    lista = solucao[maquina]
    pos = lista.index(job_critico)
    if pos == 0:
        return []
    nova = copy.deepcopy(solucao)
    nova[maquina][pos], nova[maquina][pos - 1] = nova[maquina][pos - 1], nova[maquina][pos]
    return [(nova, (pos - 1, pos))]


def melhor_movimento(rotas, solucao, M):
    
    custo_atual, viavel_atual, c_real, _ = avaliar(rotas, solucao, M)
    if not viavel_atual:
        raise ValueError("melhor_movimento recebeu uma solução inviável de partida")

    job_critico = max(c_real, key=c_real.get)  # quem determina o Cmax
    maquinas_alvo = maquinas_do_job(rotas, job_critico)

    melhor_custo = custo_atual
    melhor_solucao = None
    melhor_info = None

    for m in maquinas_alvo:
        for nova_solucao, (i, j) in gerar_vizinhos_swap(solucao, m, job_critico):
            custo_novo, viavel_novo, c_real_novo, _ = avaliar(rotas, nova_solucao, M)
            if not viavel_novo:
                continue  # deadlock: descartado
            # aceita também empates (<=), não só melhora estrita (<),
            # para não travar cedo demais num platô do Cmax
            if custo_novo <= melhor_custo:
                melhor_custo = custo_novo
                melhor_solucao = nova_solucao
                melhor_info = {
                    "maquina": m, "posicoes": (i, j),
                    "job_critico": job_critico, "cmax_job_critico": c_real[job_critico],
                    "cmax": custo_novo,
                }

    if melhor_solucao is None:
        return None, custo_atual, None
    return melhor_solucao, melhor_custo, melhor_info


def _canon(solucao):
    """Representação hashável da solução, para detectar repetição de estado."""
    return tuple(sorted((m, tuple(lista)) for m, lista in solucao.items()))


def busca_local(rotas, solucao_inicial, max_iter=200, verbose=True):
    """
    Aplica melhor_movimento repetidamente até não achar mais candidato,
    até repetir um estado já visitado (ciclo — possível agora que
    aceitamos empates), ou até atingir max_iter.

    Retorna (melhor_solucao, melhor_custo, historico)
    """
    M = soma_todas_duracoes(rotas) + 1
    solucao = copy.deepcopy(solucao_inicial)
    custo_atual, viavel, c_real, _ = avaliar(rotas, solucao, M)
    if not viavel:
        raise ValueError("busca_local precisa começar de uma solução viável")

    historico = [{"iter": 0, "cmax": custo_atual}]
    visitados = {_canon(solucao)}
    if verbose:
        print(f"[iter 0] Cmax={custo_atual}")

    for it in range(1, max_iter + 1):
        nova_solucao, novo_custo, info = melhor_movimento(rotas, solucao, M)
        if nova_solucao is None:
            if verbose:
                print(f"[iter {it}] nenhuma troca dispon\u00edvel — ótimo local atingido")
            break

        canon_nova = _canon(nova_solucao)
        if canon_nova in visitados:
            if verbose:
                print(f"[iter {it}] estado já visitado (ciclo de empates) — parando")
            break
        visitados.add(canon_nova)

        solucao = nova_solucao
        historico.append({"iter": it, "cmax": novo_custo})
        if verbose:
            print(f"[iter {it}] swap em M{info['maquina']} pos{info['posicoes']} "
                  f"(job crítico {info['job_critico']}, C={info['cmax_job_critico']}) "
                  f"-> Cmax={novo_custo}")

    return solucao, historico[-1]["cmax"], historico


if __name__ == "__main__":
    rotas = [
        [(0, 4), (1, 3), (2, 2)],   # job 0
        [(1, 3), (0, 4), (2, 3)],   # job 1
        [(2, 5), (0, 2), (1, 3)],   # job 2
    ]
    solucao_inicial = {
        0: [0, 1, 2],
        1: [0, 1, 2],
        2: [2, 1, 0],
    }

    solucao_final, custo_final, historico = busca_local(rotas, solucao_inicial)
    print()
    print("Solução final:", solucao_final)
    print("Cmax final:", custo_final)