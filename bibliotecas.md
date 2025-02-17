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
