---
marp: true
title: "Otimização Combinatória em Grafos - Bibliotecas"
theme: default
class: lead
footer: "OCR - Albert E. F. Muritiba"
paginate: true
backgroundColor: #ffffff
backgroundImage: url('https://spideryzarc.github.io/labCD/bg/light_curve.jpg')
style: |
  .small{
    font-size: 0.75rem;
  }
# Em todas as minhas obras o Senhor será glorificado.	
---

# Bibliotecas para Otimização Combinatória em Grafos

Há diversas bibliotecas para manipulação de grafos e otimização combinatória. Neste curso, focaremos na biblioteca `NetworkX`, que é uma das mais populares e de fácil utilização. 


---

No entanto, há outras bibliotecas que podem ser úteis dependendo do problema a ser resolvido.

- [NetworkX](https://networkx.org/)
- [Graph-tool](https://graph-tool.skewed.de/)
- [Igraph](https://igraph.org/)
- [Snap](https://snap.stanford.edu/)
- [Boost Graph Library](https://www.boost.org/doc/libs/1_76_0/libs/graph/doc/index.html)
- [Lemon](https://lemon.cs.elte.hu/trac/lemon)
- [OGDF](https://ogdf.github.io/)

---

# *NetworkX*

- Biblioteca Python para criação, manipulação e estudo de estruturas, dinâmicas e funções de redes complexas.

![bg right:40% 90%](https://networkx.org/_static/networkx_logo.svg)

---

## Instalação

```bash
pip install networkx
```

---

## Exemplo

```python
import networkx as nx

G = nx.Graph()
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 1)

nx.draw(G, with_labels=True)
```

---

# 🏗️ Estruturas de Grafos

- **Grafo não direcionado** (`Graph`)
- **Grafo direcionado** (`DiGraph`)
- **Grafo ponderado** (atributo `weight` nas arestas)
- **Grafo bipartido** (`bipartite`)

```python
G = nx.DiGraph()
G.add_weighted_edges_from([(1, 2, 4.5), (2, 3, 3.0)])
```

---

# 🔹 Caminho Mínimo

## 📍 Algoritmo de Dijkstra

- Encontra o caminho mais curto entre dois nós em grafos com pesos não negativos.

```python
shortest_path = nx.shortest_path(G, source=1, target=3, weight='weight')
print(shortest_path)
```

- Alternativas:
  - **Bellman-Ford** (suporta pesos negativos)
  - **A*** (A-star) para buscas guiadas

---

# 🌳 Árvores Geradoras Mínimas

- Encontram a árvore de menor custo conectando todos os nós.
- Aplicações: redes elétricas, telecomunicações, transporte.

```python
T = nx.minimum_spanning_tree(G, algorithm='prim')
nx.draw(T, with_labels=True)
```

- Algoritmos:
  - **Prim** (adiciona vértices gradualmente)
  - **Kruskal** (adiciona arestas ordenadas)

---

# 🚰 Fluxo Máximo em Redes

- O problema do **fluxo máximo** busca a maior quantidade de fluxo entre um nó origem e um nó destino.

```python
flow_value, flow_dict = nx.maximum_flow(G, s=1, t=3)
print(flow_value)
```

- Algoritmos:
  - **Ford-Fulkerson**
  - **Edmonds-Karp**

---

# 🎭 Casamento Máximo (Grafos Bipartidos)

- Encontrar o maior número de combinações possíveis entre dois grupos distintos.

```python
from networkx.algorithms import bipartite
matching = bipartite.maximum_matching(G)
```

- Aplicações:
  - Designação de tarefas
  - Alocação de recursos

---

# 🤖 Problema do Caixeiro Viajante (TSP)

- Encontrar o menor caminho que passe por todos os vértices uma única vez.

```python
import networkx.algorithms.approximation as approx
path = approx.traveling_salesman_problem(G, cycle=True)
```

- Algoritmos:
  - Aproximações heurísticas
  - Algoritmos exatos para pequenas instâncias

---

# 📍 Aplicações Práticas

- **Roteamento de veículos** 🚚
- **Escalonamento de tarefas** ⏳
- **Distribuição de energia** ⚡
- **Redes de comunicação** 🌐

---

# 📚 Referências e Materiais Extras

- **Documentação NetworkX**: [https://networkx.org/](https://networkx.org/)
- **Livro: Network Science - Barabási**
- **Exercícios práticos:** Implementação de TSP e fluxo máximo

---

# 🚀 Obrigado! Dúvidas?

**E-mail:** [Seu Contato]

🎯 Vamos praticar no Jupyter Notebook!
