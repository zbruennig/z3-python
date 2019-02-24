from z3 import *

""" Program 1

if (!a && !b) h();
else
    if(!a) g();
    else f();
"""

""" Program 2

if(a) f();
else
    if(b) g();
    else h();
"""

A, B = Bools('A B')
F, G, H = Bools('F G H')

p1e = If(Not(A), G, F)
p1 = If(And(Not(A), Not(B)), H, p1e)

##############################################

p2e = If(B, G, H)
p2 = If(A, F, p2e)

s = Solver()
s.add(Not(p1 == p2))
print s.check()
# print s.model()
