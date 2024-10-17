---
marp: true
title: "Programação Linear Inteira"
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

# Programação Linear Inteira

---

# O que é Programação Linear Inteira (PLI)?
- **Definição:** PLI é uma forma de Programação Linear (PL) em que algumas ou todas as variáveis devem assumir valores inteiros.
- **Diferença com PL:** Em PL, as variáveis podem assumir valores fracionários, mas em PLI, essas variáveis são restritas a valores inteiros.

---

# Exemplos de Aplicação
- **Problema da Mochila:** Selecionar itens de maior valor sem ultrapassar o limite de peso.
- **Cobertura de Conjuntos:** Selecionar o menor número de subconjuntos que cubram todos os elementos de um conjunto.

---

# Formulação de Problemas com PLI
- **Passo 1:** Definir as variáveis de decisão.
- **Passo 2:** Estabelecer a função objetivo (maximização ou minimização).
- **Passo 3:** Incluir as restrições (garantindo que as variáveis sejam inteiras).

---

# Diferenças entre PL e PLI
- **Programação Linear (PL):** Soluções podem ser fracionárias (ex.: \(x = 2.5\)).
- **Programação Linear Inteira (PLI):** Soluções precisam ser inteiras (ex.: \(x = 2\)).
- **Impacto:** Algumas soluções fracionárias não são viáveis em muitos problemas do mundo real.

---

# Algoritmos para Resolver PLI
- **Branch-and-Bound:** Explora soluções ao dividir o problema em subproblemas menores.
- **Cutting Planes:** Adiciona restrições (cortes) ao problema para eliminar soluções fracionárias.

---

# Ferramentas Computacionais para PLI
- **Solvers:** CPLEX, Gurobi, GLPK, CBC.
- **Exemplo Prático:** Resolver um pequeno problema de PLI usando uma dessas ferramentas.

---

# Complexidade Computacional
- **NP-completo:** Muitos problemas de PLI são NP-completos, o que significa que não há algoritmos que garantam soluções em tempo polinomial para todos os casos.
- **Impacto:** A resolução de problemas de grande escala pode se tornar inviável.

---

# Discussão e Exemplos Práticos
- **Problema da Mochila:** Resolver um problema prático de PLI usando programação linear.
- **Exercício:** Formule um problema de otimização e resolva-o usando PLI.

---

# Leituras Recomendadas
- **Bazaraa et al. (Cap. 3):** Fundamentos de Programação Linear e Inteira.
- **Goldbarg e Lunna (Cap. 1):** Introdução à Programação Linear Inteira.

---

# Próxima Aula
- **Tema:** Algoritmos de Aproximação
- **Tópicos:** Algoritmos para problemas de empacotamento e cobertura.
