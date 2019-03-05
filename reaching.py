from z3 import *

"""
Y := X; [1]
Z := 1; [2]
while 1<Y [3] do
  Z := Z * Y; [4]
  Y := Y - 1; [5]
Y := 0 [6]
"""

"""
    EECS 742 - Z3 Reaching Modeling

    Zachary Bruennig
    https://github.com/zbruennig/z3-python

    !Important
    Execute this program using python 2!!
    It will not compile with python 3 due to differences in how each language handles lambdas.

    This program outputs the following:

    EN1: [(x, ?), (y, ?), (z, ?)]
    EX1: [(x, ?), (y, 1), (z, ?)]
    EN2: [(x, ?), (y, 1), (z, ?)]
    EX2: [(x, ?), (y, 1), (z, 2)]
    EN3: [(x, ?), (y, 1), (y, 5), (z, 2), (z, 4)]
    EX3: [(x, ?), (y, 1), (y, 5), (z, 2), (z, 4)]
    EN4: [(x, ?), (y, 1), (y, 5), (z, 2), (z, 4)]
    EX4: [(x, ?), (y, 1), (y, 5), (z, 4)]
    EN5: [(x, ?), (y, 1), (y, 5), (z, 4)]
    EX5: [(x, ?), (y, 5), (z, 4)]
    EN6: [(x, ?), (y, 1), (y, 5), (z, 2), (z, 4)]
    EX6: [(x, ?), (y, 6), (z, 2), (z, 4)]

    From this output, the following questions can be answered:
    1) X has not been initialized at the end of the program
        The end of the program is EX6, and in this reaching definition the only label for X is ?
    2) The assignment of Z at either label 2 or 4 may reach label 6
        In EX6, the pairs (z, 2) and (z, 4) are present.
    3) The assignment of Z at label 2 does not reach label 5
        In neither EN5 nor EX5 does the pair (z, 2) appear.
    4) There is no model where X has been assigned before program exit
        By adding the following condition to our SAT problem,
        asserting that (x, ?) must not be present in EX6,
         we can show this is true.

         xH = I(x, lH)
         s.add(Not(ex6[xH]))
"""

x, y, z = Ints("x y z")
Var = [x, y, z]

l1, l2, l3, l4, l5, l6, lH = Ints("1 2 3 4 5 6 ?")
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

ln = len(en1)

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

def union(*bools):
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

en = [
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

def assignment(var, lab, eq_pair):
    for i in range(ln):
        if has_v(var, i):
            if i == I(var, lab):
                r.append(en[eq_pair][1][i] == True)
            else:
                r.append(en[eq_pair][1][i] == False)
        else:
            r.append(en[eq_pair][1][i] == en[eq_pair][0][i])

def conditional(equation):
    return None

def loop(equation):
    return None

def En1():
    initialize(en1)

def Ex1():
    assignment(y, l1, 1)

def En2():
    for i in range(ln):
        r.append(en2[i] == ex1[i])

def Ex2():
    assignment(z, l2, 2)

def En3():
    for i in range(ln):
        r.append(en3[i] == union(ex2[i], ex5[i]))

def Ex3():
    for i in range(ln):
        r.append(ex3[i] == en3[i])

def En4():
    for i in range(ln):
        r.append(en4[i] == ex3[i])

def Ex4():
    assignment(z, l4, 4)

def En5():
    for i in range(ln):
        r.append(en5[i] == ex4[i])

def Ex5():
    assignment(y, l5, 5)

def En6():
    for i in range(ln):
        r.append(en6[i] == ex3[i])

def Ex6():
    assignment(y, l6, 6)

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
