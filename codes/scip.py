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

