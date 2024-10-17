---
marp: true
title: "Tutorial SCIP"
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

# Introdução ao SCIP

SCIP (Solving Constraint Integer Programs) é uma poderosa ferramenta para resolver problemas de Programação Linear Inteira (PLI), Programação Linear Mista (MILP) e mais. É amplamente utilizado em pesquisa e indústrias pela sua eficiência.

---

# Instalação do SCIP

## No Linux (Ubuntu)
```bash
sudo apt update
sudo apt install scip
```

## No Windows e macOS
Baixe a versão apropriada do SCIP em: [https://scipopt.org/index.php#download].

---

# Modo Interativo: Exemplo Simples

## Problema da Mochila
Itens com valores: 10, 13, 18 e pesos: 5, 6, 8. Capacidade da mochila: 10.
Maximizar valor sem ultrapassar a capacidade.

---

## Definir o Problema no SCIP

1. Criar variáveis binárias
```bash
create variable x1 binary
create variable x2 binary
create variable x3 binary
```

2. Definir a função objetivo
```bash
set obj sense maximize
add obj 10 x1
add obj 13 x2
add obj 18 x3
```

---

## Restrições e Solução

1. Adicionar a restrição de capacidade
```bash
add cons 5 x1 + 6 x2 + 8 x3 <= 10
```

2. Resolver o problema
```bash
optimize
```

3. Exibir a solução
```bash
display solution
```

---

# Salvando e Exportando o Modelo

Você pode salvar o modelo para análise posterior:
```bash
write problem mochila.lp
```

---

# Uso com Python (PySCIPOpt)

SCIP oferece uma API Python para resolução de problemas. Instale com:
```bash
pip install pyscipopt
```

---

## Exemplo em Python: Problema da Mochila
```python
from pyscipopt import Model

model = Model("Problema da Mochila")
x1 = model.addVar("x1", vtype="B")
x2 = model.addVar("x2", vtype="B")
x3 = model.addVar("x3", vtype="B")

model.setObjective(10*x1 + 13*x2 + 18*x3, "maximize")
model.addCons(5*x1 + 6*x2 + 8*x3 <= 10)

model.optimize()

solution = model.getBestSol()
print("x1 =", solution[x1])
print("x2 =", solution[x2])
print("x3 =", solution[x3])
print("Valor da mochila =", model.getObjVal())
```

---

# Problemas Avançados com SCIP

Além do problema de **mochila**, o SCIP pode resolver:

- **MILP (Programação Linear Mista Inteira)**
- **MINLP (Programação Não Linear Inteira)**
- **Programação por Restrições (CSP)**

---

# Conclusão

O SCIP é uma ferramenta versátil para resolver problemas de otimização complexos, com aplicações em várias áreas como logística, indústria, e pesquisa.

---

# Próximos Passos
- Explore a documentação oficial: [https://scipopt.org/doc/html/index.php]
- Pratique com exemplos mais complexos (MILP, MINLP).

