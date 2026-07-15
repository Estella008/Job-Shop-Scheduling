# -*- coding: utf-8 -*-
"""
Depende de c_real_ideal.py (soma_todas_duracoes, avaliar).

Shaking: perturbação aleatória usada quando a busca local estagna.
Ao contrário da busca local (guiada pelo job crítico), aqui as trocas
são sorteadas de propósito, para escapar do ótimo local atual.
"""

import copy
import random
from avaliacao import avaliar
from avaliacao import soma_todas_duracoes, avaliar


def perturbar(solucao, k, rng=None):
    """
    Aplica k trocas aleatórias de posição nas listas de prioridade
    das máquinas (cada troca sorteia uma máquina e duas posições
    dela; podem cair na mesma máquina ou em máquinas diferentes).

    rng: instância de random.Random, opcional (útil pra reprodutibilidade
         em testes). Se não passar, usa o módulo random global.
    """
    if rng is None:
        rng = random

    nova = copy.deepcopy(solucao)
    maquinas = list(nova.keys())

    for _ in range(k):
        m = rng.choice(maquinas)
        n = len(nova[m])
        if n < 2:
            continue  # máquina com 0 ou 1 operação não tem o que trocar
        i, j = rng.sample(range(n), 2)
        nova[m][i], nova[m][j] = nova[m][j], nova[m][i]

    return nova


def shaking(rotas, solucao, k, M, rng=None):
    
    
    nova_solucao = perturbar(solucao, k, rng=rng)
    custo, viavel, c_real, _ = avaliar(rotas, nova_solucao, M)
    return nova_solucao, custo, viavel


if __name__ == "__main__":
    

    rotas = [
        [(0, 4), (1, 3), (2, 2)],
        [(1, 3), (0, 4), (2, 3)],
        [(2, 5), (0, 2), (1, 3)],
    ]
    M = soma_todas_duracoes(rotas) + 1

    solucao = {
        0: [0, 1, 2],
        1: [1, 0, 2],
        2: [2, 0, 1],
    }  # a solução ótima local que a busca local encontrou (Cmax=13)

    custo_base, viavel_base, c_real_base, _ = avaliar(rotas, solucao, M)
    print(f"Solução base: Cmax={custo_base}  viável={viavel_base}")
    print()

    rng = random.Random(42)  # semente fixa só pra este teste ser reprodutível
    for k in [1, 2, 3]:
        nova_solucao, custo, viavel = shaking(rotas, solucao, k, M, rng=rng)
        print(f"k={k}: solucao={nova_solucao}  Cmax/custo={custo}  viável={viavel}")