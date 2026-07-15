def ler_instancia(caminho_arquivo):
    """  

    Exemplo de retorno para o job 0 da instancia ft10:
        [(0, 29), (1, 78), (2, 9), (3, 36), (4, 49), (5, 11), (6, 62), (7, 56), (8, 44), (9, 21)]
    """
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        linhas = [linha.strip() for linha in f if linha.strip() and not linha.startswith("#")]

    num_jobs, num_maquinas = map(int, linhas[0].split())

    jobs = []
    for linha_job in linhas[1:1 + num_jobs]:
        numeros = list(map(int, linha_job.split()))
        pares = [(numeros[i], numeros[i + 1]) for i in range(0, len(numeros), 2)]
        jobs.append(pares)

    return jobs


if __name__ == "__main__":
    jobs = ler_instancia("ft10.txt")
    for i, job in enumerate(jobs):
        print(f"Job {i}: {job}")