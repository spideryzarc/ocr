---
marp: true
title: "Revisão: Teoria dos Grafos"
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
# Em todas as minhas obras o Senhor será glorificado.\t

---

# Histórico da Teoria dos Grafos

A Teoria dos Grafos teve início com **Leonhard Euler** em 1736 com o problema das **Pontes de Königsberg**. Desde então, foi aplicada em redes de transporte, biologia, e redes sociais.

![bg right:40%](https://upload.wikimedia.org/wikipedia/commons/5/5d/Konigsberg_bridges.png)


---

# Definição de Grafo

Um **grafo** é uma estrutura composta de:
- **Vértices (nós):** Representam os objetos.
- **Arestas (ligações):** Conectam os vértices.

Exemplo: Redes sociais, rotas de transporte.

![bg right:40%](https://upload.wikimedia.org/wikipedia/commons/5/5d/Konigsberg_bridges.png)

---

# Tipos de Grafos

1. **Grafo Dirigido:** Arestas com direção.
2. **Grafo Não Dirigido:** Arestas sem direção.
3. **Grafo Completo:** Todos os pares de vértices estão conectados.
4. **Grafo Bipartido:** Vértices divididos em dois conjuntos, sem conexões internas.
5. **Árvore:** Grafo acíclico e conexo.
6. **Árvore Geradora Mínima (MST):** Conecta todos os vértices com o menor custo total.
7. **Grafo Ponderado:** Arestas possuem pesos.

---

# Isomorfismo de Grafos

Dois grafos são **isomorfos** se existe uma correspondência entre seus vértices e arestas que preserva as conexões.
- Exemplo: Grafos com a mesma estrutura, mas com disposição visual diferente.

---

# Componentes dos Grafos

1. **Caminho:** Sequência de vértices conectados.
2. **Ciclo:** Caminho que começa e termina no mesmo vértice.
3. **Grafo Conexo:** Existe um caminho entre qualquer par de vértices.

---

# Caminhos e Ciclos Especiais

1. **Ciclo Euleriano:** Passa por todas as arestas exatamente uma vez.
   - **Critério:** O grafo é conexo e todos os vértices têm grau par.
2. **Ciclo Hamiltoniano:** Passa por todos os vértices exatamente uma vez.

---

# Representações de Grafos

1. **Matriz de Adjacência:** Matriz \( n \times n \) indicando a existência de arestas entre vértices.
2. **Lista de Adjacência:** Cada vértice possui uma lista de seus vértices adjacentes.

---

# Algoritmos Clássicos em Grafos

1. **Busca em Largura (BFS):** Explora todos os vértices de uma camada antes de avançar.
2. **Busca em Profundidade (DFS):** Explora profundamente antes de retroceder.
3. **Dijkstra:** Encontra o caminho mais curto em grafos ponderados.
4. **Bellman-Ford:** Caminhos curtos com arestas de pesos negativos.
5. **Prim e Kruskal:** Encontram a árvore geradora mínima (MST).

---

# Problemas Clássicos de Grafos

1. **Caminho Mínimo:** Encontra o caminho de menor custo entre dois vértices.
2. **Fluxo Máximo:** Encontra o maior fluxo entre dois vértices respeitando capacidades.
3. **Cobertura de Vértices:** Menor conjunto de vértices que cobre todas as arestas.
4. **Coloração de Grafos:** Atribui cores aos vértices para evitar arestas conectando vértices de mesma cor.

---

# Aplicações de Grafos

1. **Redes de Comunicação:** Modelagem de conexões entre computadores.
2. **Redes de Transporte:** Otimização de rotas.
3. **Redes Sociais:** Análise de conexões e influência.
4. **Biologia Computacional:** Modelagem de interações entre genes e proteínas.

---

# Conclusão

A Teoria dos Grafos é uma área versátil e essencial para modelar e resolver problemas em diversas áreas. Estudar algoritmos de grafos permite resolver problemas de grande escala de forma eficiente.

---

# Próximos Passos

- Estude algoritmos avançados de grafos.
- Explore problemas NP-completos como coloração de grafos.
- Pratique a implementação de algoritmos clássicos como BFS e DFS.