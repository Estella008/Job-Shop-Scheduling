# Job Shop Scheduling com VNS

Este projeto implementa uma solução heurística para o problema **Job Shop Scheduling Problem (JSSP)** usando **busca local** e a metaheurística **VNS (Variable Neighborhood Search)** com *shaking*.

O objetivo é minimizar o **Cmax** (*makespan*), que representa o tempo total de conclusão do cronograma.

## Problema

No Job Shop Scheduling, existem **jobs** e **máquinas**. Cada job possui uma sequência fixa de operações, e cada operação deve ser executada em uma máquina específica durante uma determinada duração.

O objetivo é encontrar uma ordem de execução das operações nas máquinas que minimize o tempo de conclusão do último job.

## Estrutura do projeto

```text
.
├── avaliacao.py
├── busca_local.py
├── ler_instancia.py
├── main.py
├── shaking.py
├── vns.py
├── ft10.txt
├── swv20.txt
└── README.md
```

## Requisitos

- Python 3.10 ou superior

O projeto usa apenas bibliotecas padrão do Python.

## Como executar

Na pasta do projeto, execute:

```bash
python main.py ft10.txt
```

No Windows, se o comando `python` não estiver disponível, use:

```bash
py main.py ft10.txt
```

Para executar sem imprimir o cronograma completo:

```bash
py main.py ft10.txt --quiet --seed 42 --sem-cronograma
```

Também é possível executar a segunda instância:

```bash
py main.py swv20.txt --quiet --seed 42 --sem-cronograma
```

## Parâmetros

```text
--k-max           valor máximo de k no VNS
--max-iter        número máximo de tentativas do VNS
--seed            semente para reprodutibilidade
--quiet           mostra apenas o resultado final
--sem-cronograma  não imprime o cronograma detalhado
```

Exemplo com parâmetros explícitos:

```bash
py main.py ft10.txt --k-max 5 --max-iter 200 --seed 42 --sem-cronograma
```

## Formato da entrada

A primeira linha informa:

```text
número_de_jobs número_de_máquinas
```

Cada linha seguinte representa um job. Os valores aparecem em pares:

```text
máquina duração
```

Exemplo:

```text
3 3
0 4 1 3 2 2
1 3 0 4 2 3
2 5 0 2 1 3
```

Nesse exemplo, o primeiro job executa:

```text
Máquina 0 por 4 unidades de tempo
Máquina 1 por 3 unidades de tempo
Máquina 2 por 2 unidades de tempo
```

## Cálculo do valor da solução

Para uma solução viável, o valor da solução é o **Cmax**:

```text
Cmax = max(C_i)
```

Onde `C_i` é o tempo de conclusão do job `i`.

Se a solução for inviável por *deadlock*, o algoritmo aplica uma penalização:

```text
custo = M + q
```

Onde:

```text
M = soma de todas as durações das operações + 1
q = número de operações que não conseguiram ser agendadas
```

Assim, soluções inviáveis recebem custo pior e tendem a ser descartadas durante a busca.

## Heurística e metaheurística

A busca local usada é uma **best improvement restrita**. Ela identifica o job crítico, ou seja, o job que determina o maior tempo de conclusão, e gera vizinhos por meio de trocas de prioridade (*swap*) desse job nas máquinas por onde ele passa.

A metaheurística usada é o **VNS**. O algoritmo parte de uma solução inicial viável, aplica busca local e, quando chega a um ótimo local, usa *shaking* para perturbar a solução e tentar escapar da estagnação.

## Exemplo de saída

Executando:

```bash
py main.py ft10.txt --quiet --seed 42 --sem-cronograma
```

Saída obtida:

```text
Instancia: ft10.txt
Jobs: 10
Maquinas: 10
Cmax inicial: 3394

=== Resultado final ===
Cmax final: 2779
Conclusao por job: {0: 395, 1: 697, 2: 1071, 3: 1479, 4: 1830, 5: 1992, 6: 2266, 7: 2723, 8: 2693, 9: 2779}

Solucao por maquina:
  M0: J0 -> J1 -> J2 -> J3 -> J4 -> J5 -> J6 -> J8 -> J7 -> J9
  M1: J0 -> J1 -> J2 -> J3 -> J4 -> J5 -> J6 -> J8 -> J7 -> J9
  M2: J0 -> J1 -> J2 -> J3 -> J4 -> J5 -> J6 -> J7 -> J9 -> J8
  M3: J0 -> J1 -> J2 -> J3 -> J4 -> J5 -> J6 -> J8 -> J9 -> J7
  M4: J0 -> J1 -> J2 -> J3 -> J4 -> J5 -> J6 -> J7 -> J8 -> J9
  M5: J0 -> J1 -> J2 -> J3 -> J4 -> J5 -> J6 -> J7 -> J8 -> J9
  M6: J0 -> J1 -> J2 -> J3 -> J4 -> J5 -> J6 -> J7 -> J9 -> J8
  M7: J0 -> J1 -> J2 -> J3 -> J4 -> J5 -> J6 -> J7 -> J8 -> J9
  M8: J0 -> J1 -> J2 -> J3 -> J4 -> J5 -> J6 -> J7 -> J9 -> J8
  M9: J0 -> J1 -> J2 -> J3 -> J4 -> J5 -> J6 -> J7 -> J8 -> J9
```

## Resultados dos testes

Os testes abaixo foram executados com:

```text
k_max = 5
max_iter_total = 200
seed = 42
```

| Instância | Jobs | Máquinas | Cmax inicial | Cmax final | Melhora | Tentativas VNS | Tempo aproximado |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ft10.txt | 10 | 10 | 3394 | 2779 | 18,12% | 5 | 0,200 s |
| swv20.txt | 50 | 10 | 18932 | 18255 | 3,58% | 5 | 0,557 s |

## Vídeo de apresentação

Link do vídeo:


https://youtu.be/UeEsxjOXsZA


## Autoria

Trabalho desenvolvido para a disciplina de Tópicos em Algoritmos.

Autor(a): Estella
