import argparse
import random
from pathlib import Path

from avaliacao import avaliar
from ler_instancia import ler_instancia
from vns import vns


def construir_solucao_inicial(jobs):
    
    num_maquinas = max(max(maquina for maquina, _ in job) for job in jobs) + 1
    jobs_por_maquina = {maquina: [] for maquina in range(num_maquinas)}

    for job_id, job in enumerate(jobs):
        for maquina, _ in job:
            jobs_por_maquina[maquina].append(job_id)

    return {
        maquina: sorted(job_ids)
        for maquina, job_ids in jobs_por_maquina.items()
    }


def imprimir_solucao(solucao):
    print("\nSolucao por maquina:")
    for maquina in sorted(solucao):
        sequencia = " -> ".join(f"J{job}" for job in solucao[maquina])
        print(f"  M{maquina}: {sequencia}")


def imprimir_cronograma(cronograma):
    print("\nCronograma final:")
    print("  Job  Op  Maq  Inicio  Fim")
    for job, operacao, maquina, inicio, fim in sorted(cronograma, key=lambda item: (item[3], item[2], item[0])):
        print(f"  J{job:<3} {operacao:<3} M{maquina:<3} {inicio:<7} {fim}")


def criar_parser():
    parser = argparse.ArgumentParser(
        description="Executa o algoritmo VNS para o problema Job Shop Scheduling."
    )
    parser.add_argument(
        "instancia",
        nargs="?",
        default="ft10.txt",
        help="Caminho do arquivo de instancia. Padrao: ft10.txt",
    )
    parser.add_argument("--k-max", type=int, default=5, help="Valor maximo de k no VNS.")
    parser.add_argument(
        "--max-iter",
        type=int,
        default=200,
        help="Numero maximo de tentativas do VNS.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Semente para deixar as perturbacoes aleatorias reprodutiveis.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Mostra apenas o resultado final.",
    )
    parser.add_argument(
        "--sem-cronograma",
        action="store_true",
        help="Nao imprime o cronograma detalhado ao final.",
    )
    return parser


def resolver_caminho_instancia(caminho):
    caminho_instancia = Path(caminho)
    if caminho_instancia.exists() or caminho_instancia.is_absolute():
        return caminho_instancia
    return Path(__file__).resolve().parent / caminho_instancia


def main():
    args = criar_parser().parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    caminho_instancia = resolver_caminho_instancia(args.instancia)
    jobs = ler_instancia(caminho_instancia)
    solucao_inicial = construir_solucao_inicial(jobs)

    custo_inicial, viavel_inicial, _, _ = avaliar(jobs, solucao_inicial)
    if not viavel_inicial:
        raise RuntimeError("A solucao inicial gerada nao e viavel.")

    print(f"Instancia: {caminho_instancia}")
    print(f"Jobs: {len(jobs)}")
    print(f"Maquinas: {len(solucao_inicial)}")
    print(f"Cmax inicial: {custo_inicial}")

    melhor_solucao, melhor_custo = vns(
        jobs,
        solucao_inicial,
        k_max=args.k_max,
        max_iter_total=args.max_iter,
        verbose=not args.quiet,
    )

    custo_final, viavel_final, c_real, cronograma = avaliar(jobs, melhor_solucao)
    if not viavel_final:
        raise RuntimeError("O VNS retornou uma solucao inviavel.")

    print("\n=== Resultado final ===")
    print(f"Cmax final: {melhor_custo}")
    print(f"Conclusao por job: {c_real}")
    imprimir_solucao(melhor_solucao)

    if not args.sem_cronograma:
        imprimir_cronograma(cronograma)

    if custo_final != melhor_custo:
        print(f"\nAviso: custo reavaliado ({custo_final}) difere do custo retornado ({melhor_custo}).")


if __name__ == "__main__":
    main()


