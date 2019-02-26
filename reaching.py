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
s = Solver()

# En1
r = [] # short for rules
for i in range(ln):
    if i % len(Lab) == 6: # (_,l?)
        r.append(en1[i] == True)
    else:
        r.append(en1[i] == False)
s.add(And(r))


# Ex1
r = []
for i in range(ln):
    if has_v(y, i):
        if i == I(y, l1):
            r.append(ex1[i] == True)
        else:
            r.append(ex1[i] == False)
    else:
        r.append(ex1[i] == en1[i])
s.add(And(r))

# En2
r = []
for i in range(ln):
    r.append(en2[i] == ex1[i])
s.add(And(r))

# Ex2
r = []
for i in range(ln):
    if has_v(z, i):
        if i == I(z, l2):
            r.append(ex2[i] == True)
        else:
            r.append(ex2[i] == False)
    else:
        r.append(ex2[i] == en2[i])
s.add(And(r))

# En3
r = []
for i in range(ln):
    r.append(en3[i] == union(ex2[i], ex5[i]))
s.add(And(r))

# Ex3
r = []
for i in range(ln):
    r.append(ex3[i] == en3[i])
s.add(And(r))

# En4
En4 = []
for i in range(ln):
    En4.append(en4[i] == ex3[i])
s.add(And(En4))

# Ex4
r = []
for i in range(ln):
    if has_v(z, i):
        if i == I(z, l4):
            r.append(ex4[i] == True)
        else:
            r.append(ex4[i] == False)
    else:
        r.append(ex4[i] == en4[i])
s.add(And(r))

# En5
r = []
for i in range(ln):
    r.append(en5[i] == ex4[i])
s.add(And(r))

# Ex5
r = []
for i in range(ln):
    if has_v(y, i):
        if i == I(y, l5):
            r.append(ex5[i] == True)
        else:
            r.append(ex5[i] == False)
    else:
        r.append(ex5[i] == en5[i])
s.add(And(r))

# En6
r = []
for i in range(ln):
    r.append(en6[i] == ex3[i])
s.add(And(r))

# Ex6
r = []
for i in range(ln):
    if has_v(y, i):
        if i == I(y, l6):
            r.append(ex6[i] == True)
        else:
            r.append(ex6[i] == False)
    else:
        r.append(ex6[i] == en6[i])
s.add(And(r))

# Question 4
xH = I(x, lH)
s.add(Not(ex6[xH]))

if s.check() == sat:
    print_model(s.model())
else:
    print s.check()
