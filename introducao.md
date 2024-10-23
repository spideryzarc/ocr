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

- **Conjuntos:** $U$ de elementos, $S$ de subconjuntos.
- **Parâmetros:** 
  - $c_s$ (custo do subconjunto $s$), 
  - $U_s$ (elementos cobertos por $s$).
  - **Variáveis de Decisão:** $x_s \in \{0,1\}$, onde $x_s = 1$ se o subconjunto $s$ é selecionado.
- **Modelo:**

$$
\begin{align*}
\min & \sum_{s \in S} c_s x_s \\
\text{s.a.} & \sum_{s \in S} x_s \cdot U_s \geq 1 \quad \forall u \in U \\
& x_s \in \{0,1\} \quad \forall s \in S
\end{align*}
$$


---

## Caixeiro Viajante

<!-- TODO: colocar imagem didática do problema do caixeiro viajante -->
![height:500](https://upload.wikimedia.org/wikipedia/commons/1/11/Map_of_the_United_States_with_interstate_highways.svg)



---

# O que são Redes?

Redes são sistemas modelados como grafos, onde nós (vértices) representam objetos e arestas (ligações) representam as conexões entre eles.
<br>
>**Exemplos:** Redes de transporte, redes de comunicação, redes de distribuição de energia.


<!-- TODO: colocar imagem didática de uma rede de transporte -->


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

