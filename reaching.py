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

# Lab = EnumSort("Lab", ["l1", "l2", "l3", "l4", "l5", "l6", "l?"])

# En1
# En1 = Function("En1", Var, Lab, BoolSort())

x, y, z = Ints("x y z")
Var = [x, y, z]

l1, l2, l3, l4, l5, l6, lH = Ints("l1 l2 l3 l4 l5 l6 lH")
Lab = [l1, l2, l3, l4, l5, l6, lH]

lab = IntVector("lab", len(Lab))

Pair = Datatype("Pair")
Pair.declare("Pair", ("v", IntSort()), ("l", IntSort()))
Pair = Pair.create()



#Concise syntax for creating a new Pair/Tuple of (Var, Lab)
def P(v, l):
    return Pair.Pair(v,l)

#Since I am using IntSorts, I need to limit my ints to only the ones I define in Pair and List
def only_allowed_vl(lists):
    pairs = [P(v, l) for v in Var for l in Lab]
    length = len(pairs)
    lists.append(pairs)
    U = union(lists)
    return length == len(U)

def contains(list, pair):
    for l in list:
        if l == pair:
            return True
    return False

def En1(en1):
    #En1 = {(x,?),(y,?),(z,?)}
    x = y = z = False
    print en1
    return True

# all = [en1, en2, en3, en4, en5, en6, ex1, ex2, ex3, ex4, ex5, ex6]

# Example_pair = Pair.Pair(x,lH)
# Bad_pair = Pair.Pair(2,22)
#
# print only_allowed_vl([[Example_pair],[Example_pair]])

s = Solver()

s.add()
print s.check(contains(test,P(1,2)))
# print s.model()
