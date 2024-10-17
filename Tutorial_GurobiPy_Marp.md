---
marp: true
title: "Tutorial GurobiPy"
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

# Introdução ao GurobiPy

GurobiPy é uma interface Python para o solver Gurobi, amplamente utilizado para resolver problemas de otimização linear, inteira, e não-linear.

---

# Instalação e Obtenção de Licença Acadêmica

1. **Registro no site Gurobi**: Acesse [https://www.gurobi.com](https://www.gurobi.com).
2. **Criação de uma conta**: Clique em "Sign Up" e crie uma conta com seu e-mail institucional.
3. **Solicitação da Licença Acadêmica**:
    - Vá para [https://www.gurobi.com/academia/academic-program-and-licenses/](https://www.gurobi.com/academia/academic-program-and-licenses/).
    - Clique em "Apply for a Free Academic License".
    - Preencha os dados com as informações de sua instituição e e-mail acadêmico.
4. **Instalação da licença**: Após aprovação, você receberá as instruções por e-mail para ativar a licença no seu sistema.

---

# Instalação do GurobiPy

## No Linux/Windows/macOS
Após a obtenção da licença, você pode instalar o GurobiPy usando `pip`:
```bash
pip install gurobipy
```

---

# Exemplo em Python: Problema da Mochila

Aqui está um exemplo simples de um problema da **mochila** usando GurobiPy:

```python
from gurobipy import Model, GRB

# Criação do modelo
model = Model("Problema da Mochila")

# Definir as variáveis de decisão binárias
x1 = model.addVar(vtype=GRB.BINARY, name="x1")
x2 = model.addVar(vtype=GRB.BINARY, name="x2")
x3 = model.addVar(vtype=GRB.BINARY, name="x3")

# Definir a função objetivo (maximizar)
model.setObjective(10*x1 + 13*x2 + 18*x3, GRB.MAXIMIZE)

# Adicionar a restrição de capacidade
model.addConstr(5*x1 + 6*x2 + 8*x3 <= 10, "capacidade")

# Otimizar o modelo
model.optimize()

# Exibir a solução
for v in model.getVars():
    print(f'{v.varName}: {v.x}')

print(f'Valor da mochila: {model.objVal}')
```

---

# Uso Avançado do GurobiPy

GurobiPy é amplamente utilizado para resolver problemas complexos, como:

- **Problemas de Roteamento** (Vehicle Routing Problem)
- **Otimização de Portfólio** em Finanças
- **Problemas de Programação de Produção** em Fábricas

---

# Solução de Problemas Não Lineares

Além de problemas lineares, o Gurobi também pode resolver problemas não-lineares (quadráticos ou conicos). Exemplo:

```python
# Função objetivo quadrática
model.setObjective(x1**2 + x2**2, GRB.MINIMIZE)
```

---

# Conclusão

GurobiPy é uma ferramenta robusta e eficiente para resolver problemas de otimização complexos. A licença acadêmica é uma ótima forma de acessá-lo gratuitamente para fins educacionais e de pesquisa.

---

# Próximos Passos
- Explore mais exemplos em [https://www.gurobi.com/documentation/](https://www.gurobi.com/documentation/)
- Tente resolver problemas de programação linear inteira mista (MILP) e quadrática (QP).
