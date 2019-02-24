from z3 import *

"""
Y := X;
Z := 1;
while 1<Y do
  Z := Z * Y;
  Y := Y - 1;
Y := 0
"""

x, y, z = Ints("x y z")
Var = [x, y, z]

l1, l2, l3, l4, l5, l6, lH = Ints("l1 l2 l3 l4 l5 l6 lH")
Lab = [l1, l2, l3, l4, l5, l6, lH]

en1 = BoolVector("en1", len(Var)*len(Lab))
ex1 = BoolVector("ex1", len(Var)*len(Lab))
en2 = BoolVector("en2", len(Var)*len(Lab))
ex2 = BoolVector("ex2", len(Var)*len(Lab))
en3 = BoolVector("en3", len(Var)*len(Lab))
ex3 = BoolVector("ex3", len(Var)*len(Lab))
en4 = BoolVector("en4", len(Var)*len(Lab))
ex4 = BoolVector("ex4", len(Var)*len(Lab))
en5 = BoolVector("en5", len(Var)*len(Lab))
ex5 = BoolVector("ex5", len(Var)*len(Lab))
en6 = BoolVector("en6", len(Var)*len(Lab))
ex6 = BoolVector("ex6", len(Var)*len(Lab))

#-----------------------------
# HELPER FUNCTIONS
#-----------------------------

# I think of `pairs` as a flattened 2d array, with Var being the first index,
# and Lab the second. Thus the index in pairs is len(Lab)*Var + Lab
def to_index(tuple):
    v = Var.index(tuple[0])
    l = Lab.index(tuple[1])
    return v*len(Lab) + l

# Shorthand for above function
def I(v,l):
    return to_index((v,l))

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

#-----------------------------
# SATISFIABLE FUNCTIONS
#-----------------------------



def En1(en1):
    return And(
        Not(en1[I(x, l1)]),
        Not(en1[I(x, l2)]),
        Not(en1[I(x, l3)]),
        Not(en1[I(x, l4)]),
        Not(en1[I(x, l5)]),
        Not(en1[I(x, l6)]),
        (en1[I(x, lH)]),
        Not(en1[I(y, l1)]),
        Not(en1[I(y, l2)]),
        Not(en1[I(y, l3)]),
        Not(en1[I(y, l4)]),
        Not(en1[I(y, l5)]),
        Not(en1[I(y, l6)]),
        (en1[I(y, lH)]),
        Not(en1[I(z, l1)]),
        Not(en1[I(z, l2)]),
        Not(en1[I(z, l3)]),
        Not(en1[I(z, l4)]),
        Not(en1[I(z, l5)]),
        Not(en1[I(z, l6)]),
        (en1[I(z, lH)]),
    )


s = Solver()

s.add(En1(en1))
print s.check()
print s.model()
