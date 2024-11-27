---
marp: true
title: "Otimização Combinatória em Grafos - Algoritmos"
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

# Algoritmos de Otimização Combinatória em Grafos

Neste módulo, vamos estudar alguns algoritmos de otimização combinatória em grafos para os problema estudados no módulo anterior.

![bg right:40%](empty.svg)

---

# Problema da Mochila

Dados um **conjunto de itens**, cada um com um **peso** e um **valor**, e uma mochila com **capacidade máxima**, o problema da mochila consiste em selecionar itens para **maximizar o valor total**, **sem exceder a capacidade** da mochila.

![bg left:50% ](images/knapsack.jpeg)

---

## Anedota 

* Imagine que  você encontrou um gênio na caverna que pode resolver o problema da mochila para você.
* Você mostra que tem 4 itens e para decidir quais itens levar.
* O gênio diz que infelizmente só pode resolver o problema para 3 itens.
* O que você faz?
* ...
* Divide o problema em dois problemas com 3 itens:
  * 1. Assumo que **vou levar** um determinado item. Resulta um problema com os demais itens e capacidade reduzida.
  * 2. Assumo que **não vou levar** o item. Resulta um problema com os demais itens e capacidade original.

---
## Formalizando

- Seja $w_i$ o peso do item $i$ e $v_i$ o valor do item $i$.
- Seja $W$ a capacidade da mochila.
- Seja $n$ o número de itens.

$$
M([1,\ldots,n], W) = \left\{ \begin{array}{ll}
M([2,\ldots,n], W) & \text{se } w_1 > W \\
\max \{ M([2,\ldots,n], W), M([2,\ldots,n], W - w_1) +v_1 \} & \text{caso contrário}
\end{array} \right.
$$