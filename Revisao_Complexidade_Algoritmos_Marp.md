---
marp: true
title: "Revisão: Complexidade de Algoritmos"
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

# O que é Complexidade de Algoritmos?

A complexidade de um algoritmo mede o desempenho em termos de tempo (tempo de execução) ou espaço (memória) necessários para resolver um problema com base no tamanho da entrada.

- **Complexidade de Tempo**: Quanto tempo um algoritmo leva para ser executado.
- **Complexidade de Espaço**: A quantidade de memória extra necessária.

---

# Notações Assintóticas

- **O Grande (Big O)**: Pior caso.
- **\(\Omega\) Grande**: Melhor caso.
- **\(\Theta\)**: Caso médio, quando limitado superior e inferiormente.

Exemplo: \(O(n)\), \(\Omega(n)\), \(\Theta(n)\).

---

# Classificações Comuns de Complexidade de Tempo

1. **Constante - \(O(1)\)**: O tempo não depende do tamanho da entrada.
2. **Logarítmica - \(O(\log n)\)**: Cresce com o logaritmo da entrada.
3. **Linear - \(O(n)\)**: Cresce linearmente.
4. **Linearítmica - \(O(n \log n)\)**: Exemplo: Mergesort.
5. **Quadrática - \(O(n^2)\)**: Exemplo: Ordenação por inserção.
6. **Exponencial - \(O(2^n)\)**: Algoritmos de força bruta.

---

# Exemplo de Análise: Busca Linear

```python
def busca_linear(lista, x):
    for i in range(len(lista)):
        if lista[i] == x:
            return i
    return -1
```
- **Complexidade de Tempo**: \(O(n)\).
- **Complexidade de Espaço**: \(O(1)\).

---

# Exemplo de Análise: Busca Binária

```python
def busca_binaria(lista, x):
    esquerda, direita = 0, len(lista) - 1
    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        if lista[meio] == x:
            return meio
        elif lista[meio] < x:
            esquerda = meio + 1
        else:
            direita = meio - 1
    return -1
```
- **Complexidade de Tempo**: \(O(\log n)\).
- **Complexidade de Espaço**: \(O(1)\).

---

# Complexidade de Espaço: Exemplo Recursivo

```python
def fatorial(n):
    if n == 0:
        return 1
    return n * fatorial(n - 1)
```
- **Tempo**: \(O(n)\).
- **Espaço**: \(O(n)\).

---

# Classes de Problemas: P, NP e NP-Completo

1. **P**: Resolvido em tempo polinomial.
2. **NP**: Solução pode ser verificada em tempo polinomial.
3. **NP-Completos**: Problemas mais difíceis em NP.

Exemplos: Caixeiro Viajante, Problema da Mochila.

---

# Técnicas para Melhorar a Eficiência

1. **Divisão e Conquista**: Dividir o problema em subproblemas menores.
   - Exemplo: Mergesort.

2. **Programação Dinâmica**: Armazenar soluções de subproblemas.
   - Exemplo: Fibonacci otimizado.

3. **Algoritmos Gulosos**: Aproximação para problemas NP-completos.
   - Exemplo: Algoritmo de Prim.

---

# Conclusão

Compreender a complexidade dos algoritmos é crucial para escolher a melhor solução para um problema. A escolha de um algoritmo eficiente pode reduzir drasticamente o tempo de execução em grandes entradas.

---

# Próximos Passos

- Compare algoritmos com diferentes complexidades.
- Explore problemas NP-completos e métodos de aproximação.
- Estude algoritmos paralelos e distribuídos.

