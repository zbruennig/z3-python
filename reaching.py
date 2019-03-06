from z3 import *

"""
Y := X; [1]
Z := 1; [2]
while 1<Y [3] do
  Z := Z * Y; [4]
  Y := Y - 1; [5]
Y := 0 [6]
"""

x, y, z = Ints("x y z")
Var = [x, y, z]

l1, l2, l3, l4, l5, l6, lH = Ints("1 2 3 4 5 6 ?")
Lab = [l1, l2, l3, l4, l5, l6, lH]

ln = len(Var)*len(Lab)

en1 = BoolVector("en1", ln)
ex1 = BoolVector("ex1", ln)
en2 = BoolVector("en2", ln)
ex2 = BoolVector("ex2", ln)
en3 = BoolVector("en3", ln)
ex3 = BoolVector("ex3", ln)
en4 = BoolVector("en4", ln)
ex4 = BoolVector("ex4", ln)
en5 = BoolVector("en5", ln)
ex5 = BoolVector("ex5", ln)
en6 = BoolVector("en6", ln)
ex6 = BoolVector("ex6", ln)

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

# And the opposite way, return a (v,l) tuple from the index
def from_index(n):
    v = n // len(Lab)
    l = n % len(Lab)
    return (Var[v], Lab[l])

# Shorthand for above function, short for reverse
def R(n):
    return from_index(n)

# Returns True if the pair at index n has Var v, or False otherwise
def has_v(v,n):
    i = Var.index(v)
    min = len(Lab)*i
    max = len(Lab)*(i+1) - 1
    return min <= n <= max

# Returns True if the pair at index n has Lab l, or False otherwise
def has_l(l,n):
    i = Lab.index(l)
    return n % len(Lab) == i

def union(bools):
    return Or(bools)

def print_model(m):
    includes = {}
    for k in m:
        if m[k]: #All the true values
            # Printer assumes z3 format of vectorName__index
            k = k.__str__()
            # This defaults to unicode, so for pretty printing we use ascii
            rc = k[0:k.find('_')].encode("ascii")
            index = k[k.find('_')+2:]
            pair = R(int(index))
            try:
                includes[rc].append(pair)
            except:
                includes[rc] = [pair]
    # Prints in a reasonable order to read
    for k,v in sorted(includes.items(), key=lambda (x,y): (x[2:], x[0:2])):
        print k.upper()+":",
        print sorted(v, key=lambda x: (x[0].__str__(), x[1].__str__()))

#-----------------------------
# SATISFIABLE FUNCTIONS
# Basic structure adapted from:
# https://gist.github.com/shahril96/6541420e976fd5d9876ce66615b11e64
#-----------------------------

# All equations are mutable lists, we can pass them around as we please!

enex = [
    None,
    (en1, ex1),
    (en2, ex2),
    (en3, ex3),
    (en4, ex4),
    (en5, ex5),
    (en6, ex6)
    ]

def initialize(equation):
    for i in range(ln):
        if i % len(Lab) == len(Lab)-1: # (_,l?)
            r.append(equation[i] == True)
        else:
            r.append(equation[i] == False)

def predecessors(lab, *pred):
    eq_pair = Lab.index(lab) + 1
    exits = map((lambda x: enex[x][1]), pred)
    for i in range(ln):
        preds = map((lambda x: x[i]), exits)
        r.append(enex[eq_pair][0][i] == union(preds))

def assignment(var, lab):
    eq_pair = Lab.index(lab) + 1
    for i in range(ln):
        if has_v(var, i):
            if i == I(var, lab):
                r.append(enex[eq_pair][1][i] == True)
            else:
                r.append(enex[eq_pair][1][i] == False)
        else:
            r.append(enex[eq_pair][1][i] == enex[eq_pair][0][i])

def non_assignment(lab):
    eq_pair = Lab.index(lab) + 1
    for i in range(ln):
        r.append(enex[eq_pair][1][i] == enex[eq_pair][0][i])

def conditional(equation):
    return None

def loop(equation):
    return None

def En1():
    initialize(en1)

def Ex1():
    assignment(y, l1)

def En2():
    predecessors(l2, 1)

def Ex2():
    assignment(z, l2)

def En3():
    predecessors(l3, 2, 5)

def Ex3():
    non_assignment(l3)

def En4():
    predecessors(l4, 3)

def Ex4():
    assignment(z, l4)

def En5():
    predecessors(l5, 4)

def Ex5():
    assignment(y, l5)

def En6():
    predecessors(l6, 3)

def Ex6():
    assignment(y, l6)

#-----------------------------
# Driver code
#-----------------------------

functions = [En1, Ex1, En2, Ex2, En3, Ex3, En4, Ex4, En5, Ex5, En6, Ex6]
s = Solver()

for f in functions:
    r = []
    f()
    s.add(And(r))

if s.check() == sat:
    print_model(s.model())
else:
    print s.check()
