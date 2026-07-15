# -*- coding: utf-8 -*-



def calcular_c_ideal(rotas):
    """
    C_ideal[j] = soma das durações das operações do job j,
    assumindo que ele nunca espera por nenhuma máquina.
    Não depende da solução — só dos dados da instância.
    """
    c_ideal = {}
    for j, operacoes in enumerate(rotas):
        c_ideal[j] = sum(duracao for (maquina, duracao) in operacoes)
    return c_ideal


def soma_todas_duracoes(rotas):
    """
    Soma de todas as durações de todas as operações da instância.
    É um limite superior legítimo do Cmax de qualquer solução viável
    (pior caso: tudo processado em sequência, sem paralelismo nenhum).
    Usado para construir M — não é um valor arbitrário.
    """
    return sum(duracao for operacoes in rotas for (maquina, duracao) in operacoes)


def calcular_c_real(rotas, solucao):
   
    n_jobs = len(rotas)
    job_pronto = {j: 0 for j in range(n_jobs)}
    job_ponteiro = {j: 0 for j in range(n_jobs)}
    maquina_livre = {m: 0 for m in solucao}
    maquina_ponteiro = {m: 0 for m in solucao}

    cronograma = []
    n_operacoes = sum(len(r) for r in rotas)

    while len(cronograma) < n_operacoes:
        candidatos = []  # (inicio_possivel, maquina, job, duracao, idx_op)

        for m in solucao:
            if maquina_ponteiro[m] >= len(solucao[m]):
                continue

            j = solucao[m][maquina_ponteiro[m]]
            idx_op = job_ponteiro[j]

            if idx_op >= len(rotas[j]):
                continue

            maquina_da_operacao, duracao = rotas[j][idx_op]
            if maquina_da_operacao != m:
                continue  # job ainda não chegou nessa etapa

            inicio_possivel = max(job_pronto[j], maquina_livre[m])
            candidatos.append((inicio_possivel, m, j, duracao, idx_op))

        if not candidatos:
            # deadlock: espera circular entre máquinas — nenhuma operação
            # consegue avançar. Devolve o que já foi agendado até aqui.
            return None, cronograma

        menor_inicio = min(c[0] for c in candidatos)
        for inicio, m, j, duracao, idx_op in candidatos:
            if inicio != menor_inicio:
                continue
            fim = inicio + duracao
            cronograma.append((j, idx_op, m, inicio, fim))
            job_pronto[j] = fim
            job_ponteiro[j] += 1
            maquina_livre[m] = fim
            maquina_ponteiro[m] += 1

    c_real = {
        j: max(fim for (jj, idx, m, ini, fim) in cronograma if jj == j)
        for j in range(n_jobs)
    }
    return c_real, cronograma


def avaliar(rotas, solucao, M=None):
    """
    Custo(s) = Cmax_real(s), se a solução for viável
    Custo(s) = M + operações não agendadas, se travar (deadlock)

    M: limite superior do Cmax (soma de todas as durações + 1). Se não
       for passado, é recalculado aqui — mas o ideal é calcular uma vez
       fora da busca local (ver soma_todas_duracoes) e reusar, para não
       ficar recomputando a cada avaliação.

    Retorna: (custo, viavel, c_real_ou_None, cronograma)
    """
    if M is None:
        M = soma_todas_duracoes(rotas) + 1

    c_real, cronograma = calcular_c_real(rotas, solucao)

    if c_real is None:
        n_total = sum(len(r) for r in rotas)
        n_presas = n_total - len(cronograma)
        custo = M + n_presas
        return custo, False, None, cronograma

    cmax = max(c_real.values())
    return cmax, True, c_real, cronograma


if __name__ == "__main__":
    rotas_exemplo = [
        [(0, 4), (1, 3), (2, 2)],   # job 0
        [(1, 3), (0, 4), (2, 3)],   # job 1
        [(2, 5), (0, 2), (1, 3)],   # job 2
    ]
    M = soma_todas_duracoes(rotas_exemplo) + 1
    print("M (soma de todas as durações + 1):", M)

    solucao_viavel = {
        0: [0, 1, 2],
        1: [0, 1, 2],
        2: [2, 1, 0],
    }
    custo, viavel, c_real, cronograma = avaliar(rotas_exemplo, solucao_viavel, M)
    print("\nSolução viável:")
    print("  custo:", custo, " viavel:", viavel, " c_real:", c_real)

    solucao_deadlock = {
        0: [1, 0, 2],
        1: [0, 1, 2],
        2: [2, 1, 0],
    }
    custo, viavel, c_real, cronograma = avaliar(rotas_exemplo, solucao_deadlock, M)
    print("\nSolução com deadlock:")
    print("  custo:", custo, " viavel:", viavel)
    print("  operações agendadas antes de travar:", len(cronograma), "de", sum(len(r) for r in rotas_exemplo))