from z3 import *

"""
Y := X;
Z := 1;
while 1<Y do
  Z := Z * Y;
  Y := Y - 1;
Y := 0
"""

def union(lists):
    #Union of many sets
    if len(lists) < 2:
        return lists
    def u(l1, l2):
        list = l1
        for t in l2:
            if not t in list:
                list.append(t)
        return list
    #New list created so this function is immutable
    memory = [[]]
    for l in lists:
        memory.append(l)
    return reduce((lambda l1, l2: u(l1, l2)), memory)

# Var = EnumSort("Var", ["x", "y", "z"])
# Var.declare("x")
# Var.declare("y")
# Var.declare("z")
# Var = Var.create()
# x, y, z = Var()

# Lab = EnumSort("Lab", ["l1", "l2", "l3", "l4", "l5", "l6", "l?"])

# Lab = Datatype("Lab")
# Lab.declare("l1")
# Lab.declare("l2")
# Lab.declare("l3")
# Lab.declare("l4")
# Lab.declare("l5")
# Lab.declare("l6")
# Lab.declare("l?")
# Lab = Lab.create()

# En1
# En1 = Function("En1", Var, Lab, BoolSort())

x, y, z = Ints("x y z")
Var = [x, y, z]

l1, l2, l3, l4, l5, l6, lH = Ints("l1 l2 l3 l4 l5 l6 lH")
Lab = [l1, l2, l3, l4, l5, l6, lH]

Pair = Datatype("Pair")
Pair.declare("Pair", ("v", IntSort()), ("l", IntSort()))
Pair = Pair.create()

List = Datatype("List")
List.declare('cons', ('car', Pair), ('cdr', List))
List.declare('nil')
List = List.create()

en1, en2, en3, en4, en5, en6 = Consts('en1 en2 en3 en4 en5 en6', List)
ex1, ex2, ex3, ex4, ex5, ex6 = Consts('ex1 ex2 ex3 ex4 ex5 ex6', List)

#Concise syntax for creating a new Pair/Tuple of (Var, Lab)
def P(v, l):
    return Pair.Pair(v,l)

# En1 = []
# Ex1 = []
# En2 = []
# Ex2 = []
# En3 = []
# Ex3 = []
# En4 = []
# Ex4 = []
# En5 = []
# Ex5 = []
# En6 = []
# Ex6 = []

def only_allowed_vl(lists):
    pairs = [P(v, l) for v in Var for l in Lab]
    length = len(pairs)
    lists.append(pairs)
    U = union(lists)
    return length == len(U)

def En1(en1):
    #En1 = {(x,?),(y,?),(z,?)}
    x = y = z = False
    for p in en1:
        print p
    return True

en1 = [P(x, lH), P(y, lH), P(z, lH)]
ex1 = []
en2 = []
ex2 = []
en3 = []
ex3 = []
en4 = []
ex4 = []
en5 = []
ex5 = []
en6 = []
ex6 = []
all = [en1, en2, en3, en4, en5, en6, ex1, ex2, ex3, ex4, ex5, ex6]

Example_pair = Pair.Pair(x,lH)
Bad_pair = Pair.Pair(2,22)

print only_allowed_vl([[Example_pair],[Example_pair]])

s = Solver()
s.add(En1(en1))
s.add()

# s.add(only_allowed_vl(all))
print s.check()
