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

# Tipos de Variáveis [doc](https://pyscipopt.readthedocs.io/en/latest/tutorials/vartypes.html)

- `C` (Continuous): Variável contínua.
- `I` (Integer): Variável inteira.
- `B` (Binary): Variável binária.
- `M` (Implicit integer): Variável inteira implícita.

--- 

# Parâmetros de Execução [doc](https://pyscipopt.readthedocs.io/en/latest/tutorials/model.html)

Os principais parâmetros de execução podem ser configurados com o método `setIntParam` e `setRealParam`.

```python
model.setRealParam("limits/time", 60) # Limite de tempo
model.setRealParam("limits/memory", 1024) # Limite de memória
model.setIntParam("lp/threads", 4) # Número de threads
```

---

# Parâmetros de *plugins* [doc](https://pyscipopt.readthedocs.io/en/latest/tutorials/model.html)

Plugins são extensões do SCIP que podem ser ativadas ou desativadas. Por exemplo, o *plugins* de corte de planos.

```python
from pyscipopt import Model, SCIP_PARAMSETTING

scip = Model()
scip.setHeuristics(SCIP_PARAMSETTING.AGGRESSIVE)
scip.setPresolve(SCIP_PARAMSETTING.FAST)
scip.setEmphasis(SCIP_PARAMSETTING.FEASIBILITY)

```

---

# *Callbacks* [doc](https://pyscipopt.readthedocs.io/en/latest/tutorials/eventhandler.html)

*Callbacks* são funções que são chamadas em determinados eventos durante a resolução do problema. Por exemplo, para adicionar cortes ou *lazy constraints*.

```python
from pyscipopt import Model, SCIP_EVENTTYPE

def print_obj_value(model, event):
    print("New best solution found with objective value: {}".format(model.getObjVal()))

m = Model()
m.attachEventHandlerCallback(print_obj_value, [SCIP_EVENTTYPE.BESTSOLFOUND])
m.optimize()
```



