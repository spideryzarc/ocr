---
marp: true
title: "Introdução à Otimização Combinatória em Grafos"
theme: default
class: lead
footer: "OCR - Albert E. F. Muritiba"
paginate: true
backgroundColor: #ffffff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
style: |
  .small{
    font-size: 0.75rem;
  }
# Em todas as minhas obras o Senhor será glorificado.	
---

# Introdução à Otimização Combinatória em Grafos

---

# Apresentação do Curso

## Ementa
- Tipos de problemas de otimização combinatória e de otimização em redes.
- Empacotamento e cobertura via programação linear inteira e algoritmos de aproximação.
- Problemas de caminho mínimo: Dantzig, Dijkstra, Floyd.
- Problemas de fluxo: teorema Max Flow/Min Cut, algoritmos de aumento de fluxo e fluxo de custo mínimo.
- Árvores geradoras e algoritmos de Prim e Kruskal.

---

## Avaliação
- Provas teóricas (40%)
- Implementação de algoritmos (30%)
- Projeto final (30%)

---

## Bibliografia
- AHUJA, R.K.; MAGNANTI, T.L.; ORLIN, J.B. *Network Flows: Theory, Algorithms, and Applications*. Prentice Hall, USA, 1993.
- BAZARAA, M.; JARVIS, A.; SHERALI, H. *Linear Programming and Network Flows*. Wiley, 4ª. edição, 2011.
- SZWARCFITER, J. *Grafos e Algoritmos Computacionais*. Campus, 2ª. Edição, 1986.
- ARENALES, M.; ARMENTANO, V.; MORABITO, R; YANASSE, H. *Pesquisa Operacional*. Editora Campus (Elsevier), 2ª. Edição, 2011.
- GOLDBARG, M.C. e LUNNA, H.P.L. *Otimização Combinatória e Programação Linear: Modelos e Algoritmos*. 2ª Edição. Editora Campus Ltda, Rio de Janeiro, 2005.
- PAPADIMITRIOU, C.H.; STEIGLITZ, K. *Combinatorial Optimization: Algorithms and Complexity*. Dover Publications, 1998.

---

## Linguagens de Programação

- Todos os exemplos e atividades práticas serão realizados em **Python**.
- O aluno poderá entregar os trabalhos em **outras linguagens**, desde que seja uma linguagem 'popular', de **fácil compreensão e execução**.
- Como `solver` de programação linear inteira, será utilizado o **GUROBI** ou **SCIP**.

---

## Conhecimentos Prévios (Levantamento)

- **Programação:** Qual a sua experiência com programação? (Python, C++, Java, etc.)
- **Complexidade:** Já estudou complexidade de algoritmos? (Big-O, NP-Completo)
- **Programação Linear:** Já teve contato com programação linear ou otimização?
- **Teoria dos Grafos:** Já estudou teoria dos grafos? (Grafos, Árvores, etc.)

---

# O que é Otimização Combinatória?

* Processo de encontrar a **melhor solução** dentre um **conjunto finito** ou contável de soluções possíveis.
* No geral, uma solução para um problema de otimização combinatória pode ser visto como uma **sequência de decisões discretas** que levam a um resultado ótimo.
<br>
* **Aplicações:** Planejamento logístico, design de circuitos, alocação de recursos, etc.

---

# Exemplos de Problemas de Otimização

- **Problema da Mochila:** Seleção de itens com maior valor, respeitando restrições de peso.
- **Cobertura de Conjuntos:** Seleção do menor número de subconjuntos que cubra todos os elementos.
- **Empacotamento/Corte de Estoque:** Corte de materiais para minimizar desperdício ou empacotamento de itens em caixas.
- **Problema do Caixeiro Viajante:** Rota mais curta que visite todas as cidades uma vez.

---

## Problema da Mochila (*Knapsack*)

Dados um **conjunto de itens**, cada um com um **peso** e um **valor**, e uma mochila com **capacidade máxima**, o problema da mochila consiste em selecionar itens para **maximizar o valor total**, **sem exceder a capacidade** da mochila.

![bg left:50% ](images/knapsack.jpeg)


---
### Modelo de Programação Linear Inteira

- **Conjuntos:** $I = \{1,2,...,n\}$ de itens,
- **Parâmetros:** 
  - $v_i$ (valor do item $i$), 
  - $w_i$ (peso do item $i$), 
  - $W$ (capacidade da mochila).
- **Variáveis de Decisão:** $x_i \in \{0,1\}$, onde $x_i = 1$ se o item $i$ é selecionado.
- **Modelo:**
$$
\begin{align*}
\max & \sum_{i \in I} v_i x_i \\
\text{s.a.} & \sum_{i \in I} w_i x_i \leq W \\
& x_i \in \{0,1\} \quad \forall i \in I
\end{align*}
$$

---
### Modelo PLI Implementado em Python (SCIP)

```python
def knapsack(C:int,profits:list,weights:list)->tuple:
    ''' C: int - capacity of the knapsack
        profits: list - list of profits of each item
        weights: list - list of weights of each item
        return: tuple - (max_profit, items)'''
    n = len(profits)
    model = Model("knapsack")
    x = [model.addVar(vtype="B") for i in range(n)]
    # add objective function
    model.setObjective(qsum(profits[i]*x[i] for i in range(n)), "maximize")
    # add constraints
    model.addCons(qsum(weights[i]*x[i] for i in range(n)) <= C)
    model.optimize() # solve the model
    max_profit = model.getObjVal() # get the optimal value
    # get the selected items
    items = [i for i in range(n) if model.getVal(x[i]) > 0.5]
    return max_profit, items
```
---

## Cobertura de Conjuntos (*set cover*)

Dado um **conjunto de elementos** e um **conjunto de subconjuntos**, o problema de cobertura de conjuntos consiste em selecionar o **menor número de subconjuntos** que **cubra todos os elementos**.

Se os conjuntos tiverem **custos associados**, o objetivo é **minimizar o custo total** dos subconjuntos selecionados.

![bg left height:500](https://upload.wikimedia.org/wikipedia/commons/4/4b/Set-Cover.svg)

---

### Modelo de Programação Linear Inteira

- **Conjuntos:** 
  - $I=\{1,2,...,n\}$ de elementos,
  - $S=\{s_1,s_2,...,s_m\}$ de subconjuntos.
- **Parâmetros:** 
  - $c_j$ (custo do subconjunto $s_j$),
  - $A_{ij}$ (1 se o elemento $i$ está no subconjunto $j$, 0 caso contrário).
- **Variáveis de Decisão:** $x_j \in \{0,1\}$, onde $x_j = 1$ se o subconjunto $j$ é selecionado.
- **Modelo:**
$$
\begin{align*}
\min & \sum_{j \in S} c_j x_j \\
\text{s.a.} & \sum_{j \in S} A_{ij} x_j \geq 1 \quad \forall i \in I \\
& x_j \in \{0,1\} \quad \forall j \in S
\end{align*}
$$

---

### Modelo PLI Implementado em Python (SCIP)

```python
def set_cover(n:int,costs:list,A:np.array)->tuple:
    ''' n: int - number of elements
        costs: list - list of costs of each subset
        A: np.array - binary matrix, A[i,j] = 1 if element i is in subset j 
        return: tuple - (min_cost, subsets)'''
    m = len(costs)
    model = Model("set_cover")
    x = [model.addVar(vtype="B") for j in range(m)]
    # add objective function
    model.setObjective(qsum(costs[j]*x[j] for j in range(m)), "minimize")
    # add constraints
    for i in range(n):
        model.addCons(qsum(A[i,j]*x[j] for j in range(m)) >= 1)
    model.optimize() # solve the model
    min_cost = model.getObjVal() # get the optimal value
    # get the selected subsets
    subsets = [j for j in range(m) if model.getVal(x[j]) > 0.5]
    return min_cost, subsets
```

---

## Empacotamento/Corte de Estoque (*Cutting Stock*)

Dado um **conjunto de itens** e um conjunto de pacotes (*bins*) com **tamanhos fixos**, 
o problema de empacotamento consiste em distribuir os itens nos pacotes de forma a **minimizar o número de pacotes utilizados**.

Do ponto de vista do corte, o problema consiste em **cortar** um **material** em **peças menores** de forma a **minimizar o desperdício**.

---

### Modelo de Programação Linear Inteira

- **Conjuntos:** 
  - $I=\{1,2,...,n\}$ de itens,
  - $J=\{1,2,...,m\}$ de pacotes.
- **Parâmetros:** 
  - $w_i$ (demanda do item $i$),
  - $c_j$ (capacidade do pacote $j$),
- **Variáveis de Decisão:** 
  - $x_{ij} \in \{0,1\}$, onde $x_{ij} = 1$ se o item $i$ é colocado no pacote $j$.
  - $y_j \in \{0,1\}$, onde $y_j = 1$ se o pacote $j$ é utilizado.

---

- **Modelo:**

$$
\begin{align*}
\min & \sum_{j \in J} y_j \\
\text{s.a.} & \sum_{i \in I} w_i x_{ij} \leq c_j y_j \quad \forall j \in J \\
& \sum_{j \in J} x_{ij} = 1 \quad \forall i \in I \\
& x_{ij}, y_j \in \{0,1\} \quad \forall i \in I, j \in J
\end{align*}
$$

---

### Modelo PLI Implementado em Python (SCIP)

```python
def bpp(n:int,m:int,w:list,W:list)->tuple:
    model = Model("bpp")
    x = {(i,j):model.addVar(vtype="B") for i in range(n) for j in range(m)}
    y = [model.addVar(vtype="B") for j in range(m)]
    # add objective function
    model.setObjective(qsum(y), "minimize")
    # add constraints
    for i in range(n):
        model.addCons(qsum(x[i,j] for j in range(m)) == 1)
    for j in range(m):
        model.addCons(qsum(w[i]*x[i,j] for i in range(n)) <= W[j]*y[j])
    # optimize
    model.optimize()
    min_bins = model.getObjVal()
    bin_assignment = [[j for j in range(m) if model.getVal(x[i,j]) > 0.5][0] for i in range(n)]
    return min_bins, bin_assignment
```
---



## Caixeiro Viajante

Dado um **conjunto de cidades** e as **distâncias** entre elas, o problema do caixeiro viajante consiste em encontrar a **rota mais curta** que **visite todas as cidades uma vez** e retorne à cidade de origem.

O problema é **NP-Completo**, o que significa que não existe um algoritmo eficiente para resolvê-lo em tempo polinomial.

---

### Modelo de Programação Linear Inteira (MTZ)
Miller-Tucker-Zemlin (1960)
- **Conjuntos:** 
  - $I=\{0,1,2,...,n-1\}$ : cidades,
  - $I'= I/\{0\}$ : cidades excluindo a cidade de origem.
  - $A=\{(i,j): i,j \in I\}$ : arcos.
- **Parâmetros:**  $d_{ij}$ (distância entre as cidades $i$ e $j$).
- **Variáveis de Decisão:** 
  - $x_{ij} \in \{0,1\}$, onde $x_{ij} = 1$ se o arco $(i,j)$ é selecionado.
  - $u_i \in \mathbb{Z}$, onde $u_i$ é a posição da cidade $i$ na rota.

---

- **Modelo:**
$$
\begin{align*}
\min & \sum_{(i,j) \in A} d_{ij} x_{ij} \\
\text{s.a.} & \sum_{j \in I} x_{ij} = 1 \quad \forall i \in I \\
& \sum_{i \in I} x_{ij} = 1 \quad \forall j \in I \\
& u_i - u_j + n.x_{ij} \leq n-1 \quad \forall i \in I, j \in I', i \neq j \\
& x_{ij} \in \{0,1\} \quad \forall (i,j) \in A\\
& u_i \in \mathbb{Z^+} \quad \forall i \in I
\end{align*}
$$
> onde $n$ é o número de cidades.

---

### Modelo PLI Implementado em Python (SCIP)

```python
def tsp_mtz(c:np.array)->tuple:
    n = c.shape[0]
    model = Model("tsp")
    x = {(i,j):model.addVar(vtype="B") for i in range(n) for j in range(n)}
    u = [model.addVar(vtype="C") for i in range(n)]
    model.setObjective(qsum(c[i,j]*x[i,j] for i in range(n) for j in range(n)), "minimize")
    for i in range(n):
        model.addCons(qsum(x[i,j] for j in range(n) if i!=j ) == 1)
        model.addCons(qsum(x[j,i] for j in range(n) if i!=j ) == 1)
    for i in range(n):
        for j in range(1,n):
            if i != j: model.addCons(u[i] - u[j] + n*x[i,j] <= n-1)
    model.optimize()
    min_cost = model.getObjVal()
    u_val = [model.getVal(u[i]) for i in range(n)]
    tour = np.argsort(u_val)
    return min_cost, tour
```

---

### Modelo de Programação Linear Inteira (DFJ)
Dantzig-Fulkerson-Johnson (1954)

- **Conjuntos:** 
  - $I=\{0,1,2,...,n-1\}$ : cidades,
  - $A=\{(i,j): i,j \in I\}$ : arcos.
- **Parâmetros:**  $d_{ij}$ (distância entre as cidades $i$ e $j$).
- **Variáveis de Decisão:** 
  - $x_{ij} \in \{0,1\}$, onde $x_{ij} = 1$ se o arco $(i,j)$ é selecionado.

---

- **Modelo:**
$$
\begin{align*}
\min & \sum_{(i,j) \in A} d_{ij} x_{ij} \\
\text{s.a.} & \sum_{j \in I} x_{ij} = 1 \quad \forall i \in I \\
& \sum_{i \in I} x_{ij} = 1 \quad \forall j \in I \\
& \sum_{(i,j) \in S} x_{ij} \leq \sharp(S)-1 \quad \forall S \subsetneq I, S \neq \emptyset \\
& x_{ij} \in \{0,1\} \quad \forall (i,j) \in A
\end{align*}
$$

> Onde $S$ é um subconjunto de cidades, e $\sharp(S)$ é o número de elementos em $S$.
> Observe que a restrição de *subtour elimination* é **exponencial**, o que torna o modelo impraticável para **instâncias** grandes.
  
---

Uma variação da restrição de *subtour elimination*:

$$
\begin{align*}
& \sum_{i \in S}\sum_{j \notin S} x_{ij} \geq 1 \quad \forall S \subsetneq I, S \neq \emptyset \\
\end{align*}
$$


---

 * Na prática, **relaxamos** a restrição de *subtour elimination* e resolvemos o problema iterativamente,
 * A cada iteração, identificamos um *subtour* e **adicionamos** uma restrição para eliminá-lo,
 * O processo é repetido até que não existam mais subtours.
 * As restrições relaxadas são chamadas de **lazy constraints**.
 * Não confundir com *cutting planes*, que são restrições adicionadas ao modelo para melhorar a convergência.
 * ***Lazy constraints*** são necessárias para garantir a **correção** do modelo (sem elas, o modelo pode retornar soluções inválidas),
 * ***Cutting planes*** são utilizadas para **melhorar a eficiência** do modelo.
 

---


---

# Problemas de Otimização em Redes
- **Problema de Caminho Mínimo:** Encontrar o caminho de menor custo entre dois nós em um grafo.
- **Problema de Fluxo Máximo:** Quantidade máxima de fluxo de uma fonte a um destino em uma rede.
- **Problema da Árvore Geradora Mínima:** Conectar todos os nós com o menor custo total.

---

## Caminho Mínimo

<!-- TODO: colocar imagem didática do problema de caminho mínimo -->

![height:500](https://upload.wikimedia.org/wikipedia/commons/5/57/Dijkstra_Animation.gif)

---

## Fluxo Máximo

<!-- TODO: colocar imagem didática do problema de fluxo máximo -->
![height:500](https://upload.wikimedia.org/wikipedia/commons/5/5d/Maxflow.png)

---

## Árvore Geradora Mínima

<!-- TODO: colocar imagem didática do problema da árvore geradora mínima -->
![height:500](https://upload.wikimedia.org/wikipedia/commons/d/d2/Minimum_spanning_tree.svg)

---

# Importância da Otimização Combinatória e Redes

- **Eficiência Computacional:** Otimizar recursos, tempo e energia em diversos sistemas.
- **Tomada de Decisões:** Aplicações em engenharia, economia, transportes, e mais.
- **Resolução de Problemas Reais:** Aplicações em logística, telecomunicações, e planejamento urbano.

---

# Estrutura Matemática de Grafos
- **Grafo:** Conjunto de vértices (nós) e arestas (conexões).
- **Tipos de Grafos:** Dirigidos e não dirigidos, ponderados e não ponderados.
- **Exemplo:** Exibição de um grafo simples (grafo de transporte).

---

# Aplicações Clássicas em Engenharia
- **Redes de Transporte:** Otimização de rotas, redes rodoviárias.
- **Telecomunicações:** Roteamento de dados, redes de comunicação.
- **Planejamento Urbano:** Design de redes de água, energia e esgoto.

---

# Atividade Prática
- **Discussão em Grupo:** Identificar problemas de otimização combinatória e redes que poderiam ser encontrados no dia a dia.
- **Exemplo:** Planejamento de rotas de entrega ou distribuição de internet.

---

# Leituras Recomendadas
- **Szwarcfiter (Cap. 1):** Introdução à Teoria de Grafos
- **Ahuja et al. (Cap. 1):** Fundamentos de Fluxos em Redes

---

# Próxima Aula
- **Tema:** Programação Linear Inteira
- **Tópicos:** Fundamentos e formulações básicas, *solvers* de PLI e exemplos práticos.

