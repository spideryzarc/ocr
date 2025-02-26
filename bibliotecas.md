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


## Exemplo

```python
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 1)

nx.draw(G, with_labels=True)
plt.show()
```

---

# 🏗️ Estruturas de Grafos

- **Grafo não direcionado** (`Graph`)
- **Grafo direcionado** (`DiGraph`)
- **Multigrafo** (`MultiGraph`)
- **Multigrafo direcionado** (`MultiDiGraph`)

---

# Adicionando Arestas e Vértices

```python
G.add_node(1) # Adiciona um nó
G.add_edge(1, 2) # Adiciona uma aresta
G.add_edges_from([(2, 3), (3, 1)]) # Adiciona várias arestas
```

- Observação: os nós são adicionados automaticamente ao adicionar uma aresta.

---

# Adicionando Atributos

```python
G.add_edge(1, 2, weight=3.0)
G.add_node(1, color='red')
```
- Atributos podem ser adicionados a nós e arestas.
- Comumente usamos: `weight`, `color`, `label`, `capacity`, etc.
- Mas aceita qualquer nome, pois são argumentos variáveis.

---

# Acessando Atributos

```python
G.nodes[1]['color']
G.edges[1, 2]['weight']
```

- Acessamos os atributos de nós e arestas através de um dicionário.

---

# Removendo Arestas e Vértices

```python
G.remove_node(1) # Remove um nó
G.remove_edge(1, 2) # Remove uma aresta
G.remove_edges_from([(2, 3), (3, 1)]) # Remove várias arestas
```

- Observação: ao remover um nó, todas as arestas conectadas a ele são removidas.


---

# 📊 Visualização de Grafos

- NetworkX não possui uma função de visualização, mas é compatível com diversas bibliotecas de visualização.

```python
import matplotlib.pyplot as plt
nx.draw(G, with_labels=True)
plt.show()
```

- [Galeria](https://networkx.org/documentation/stable/auto_examples/index.html)

![bg right:40% 90%](https://networkx.org/documentation/stable/_images/sphx_glr_plot_multipartite_graph_001.png)

---

# Travessia de Grafos

- NetworkX possui funções para percorrer grafos de diversas formas. [doc](https://networkx.org/documentation/stable/reference/algorithms/traversal.html)

- Exemplo: **BFS** (Busca em Largura)

```python
bfs = nx.bfs_edges(G, source=1)
print(list(bfs))
```

---

# Algortimos de Otimização Combinatória

- NetworkX possui diversos algoritmos para otimização combinatória em grafos. [doc](https://networkx.org/documentation/stable/reference/algorithms/index.html)

- Exemplos:
  - Caminho Mínimo
  - Árvores Geradoras Mínimas
  - Fluxo Máximo
  - Casamento Máximo
  - Problema do Caixeiro Viajante

---

# 🔹 Caminho Mínimo

- Uma ampla gama de algoritmos para encontrar o caminho mais curto entre dois nós.[doc](https://networkx.org/documentation/stable/reference/algorithms/shortest_paths.html)
  - Dijkstra
  - Bellman-Ford
  - Floyd-Warshall
  - A*
  - Johnson



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
