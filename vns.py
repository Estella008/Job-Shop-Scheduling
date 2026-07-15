


from avaliacao import soma_todas_duracoes, avaliar
from busca_local import busca_local
from shaking import shaking


def vns(rotas, solucao_inicial, k_max=5, max_iter_total=200, verbose=True):
    M = soma_todas_duracoes(rotas) + 1

    if verbose:
        print("=== busca local a partir da solução inicial ===")
    melhor_solucao, melhor_custo, _ = busca_local(rotas, solucao_inicial, verbose=verbose)

    if verbose:
        print(f"\nÓtimo local de partida: Cmax={melhor_custo}\n")

    k = 1
    it = 0
    while k <= k_max and it < max_iter_total:
        it += 1

        solucao_pert, custo_pert, viavel = shaking(rotas, melhor_solucao, k, M)

        if not viavel:
            if verbose:
                print(f"[tentativa {it}] shaking k={k} travou (deadlock) — descarta, k={k+1}")
            k += 1
            continue

        if verbose:
            print(f"[tentativa {it}] shaking k={k} -> Cmax perturbado={custo_pert}, "
                  f"rodando busca local...")

        solucao_local, custo_local, _ = busca_local(rotas, solucao_pert, verbose=False)

        if custo_local < melhor_custo:
            if verbose:
                print(f"  -> melhorou! Cmax {melhor_custo} -> {custo_local}. k volta a 1.")
            melhor_solucao, melhor_custo = solucao_local, custo_local
            k = 1
        else:
            if verbose:
                print(f"  -> não melhorou (achou {custo_local}, melhor é {melhor_custo}). k={k+1}")
            k += 1

    if verbose:
        print(f"\n=== parada: k={k} > k_max={k_max} ou {it} tentativas ===")
        print(f"Melhor Cmax encontrado: {melhor_custo}")

    return melhor_solucao, melhor_custo


if __name__ == "__main__":
    rotas = [
        [(0, 4), (1, 3), (2, 2)],   # job 0
        [(1, 3), (0, 4), (2, 3)],   # job 1
        [(2, 5), (0, 2), (1, 3)],   # job 2
    ]
    # solução inicial gulosa (LPT), a mesma usada nos exemplos anteriores
    solucao_inicial = {
        0: [0, 1, 2],
        1: [0, 1, 2],
        2: [2, 1, 0],
    }

    melhor_solucao, melhor_custo = vns(rotas, solucao_inicial, k_max=5, max_iter_total=50)
    print()
    print("Solução final:", melhor_solucao)
    print("Cmax final:", melhor_custo)