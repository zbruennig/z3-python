from z3 import *
import generate

# #TODO these must be generated for every variable
# x, y, z = Ints("x y z")
# Var = [x, y, z]
#
# #TODO these must be generated for every label
# l1, l2, l3, l4, l5, l6, lH = Ints("1 2 3 4 5 6 ?")
# Lab = [l1, l2, l3, l4, l5, l6, lH]
#
# ln = len(Var)*len(Lab)
# #TODO these must be generated for every label
# en1 = BoolVector("en1", ln)
# ex1 = BoolVector("ex1", ln)
# en2 = BoolVector("en2", ln)
# ex2 = BoolVector("ex2", ln)
# en3 = BoolVector("en3", ln)
# ex3 = BoolVector("ex3", ln)
# en4 = BoolVector("en4", ln)
# ex4 = BoolVector("ex4", ln)
# en5 = BoolVector("en5", ln)
# ex5 = BoolVector("ex5", ln)
# en6 = BoolVector("en6", ln)
# ex6 = BoolVector("ex6", ln)
# #-----------------------------
# # HELPER FUNCTIONS
# #-----------------------------
#
# # I think of `pairs` as a flattened 2d array, with Var being the first index,
# # and Lab the second. Thus the index in pairs is len(Lab)*Var + Lab
# def to_index(tuple):
#     v = Var.index(tuple[0])
#     l = Lab.index(tuple[1])
#     return v*len(Lab) + l
#
# # Shorthand for above function
# def I(v,l):
#     return to_index((v,l))
#
# # And the opposite way, return a (v,l) tuple from the index
# def from_index(n):
#     v = n // len(Lab)
#     l = n % len(Lab)
#     return (Var[v], Lab[l])
#
# # Shorthand for above function, short for reverse
# def R(n):
#     return from_index(n)
#
# # Returns True if the pair at index n has Var v, or False otherwise
# def has_v(v,n):
#     i = Var.index(v)
#     min = len(Lab)*i
#     max = len(Lab)*(i+1) - 1
#     return min <= n <= max
#
# # Returns True if the pair at index n has Lab l, or False otherwise
# def has_l(l,n):
#     i = Lab.index(l)
#     return n % len(Lab) == i
#
# def union(bools):
#     return Or(bools)
#
# def print_model(m):
#     includes = {}
#     for k in m:
#         if m[k]: #All the true values
#             # Printer assumes z3 format of vectorName__index
#             k = k.__str__()
#             # This defaults to unicode, so for pretty printing we use ascii
#             rc = k[0:k.find('_')].encode("ascii")
#             index = k[k.find('_')+2:]
#             pair = R(int(index))
#             try:
#                 includes[rc].append(pair)
#             except:
#                 includes[rc] = [pair]
#     # Prints in a reasonable order to read
#     for k,v in sorted(includes.items(), key=lambda (x,y): (x[2:], x[0:2])):
#         print k.upper()+":",
#         print sorted(v, key=lambda x: (x[0].__str__(), x[1].__str__()))
#
# #-----------------------------
# # EN/EX forms, all features in our language follow one of these prototypes
# #-----------------------------
#
# def initialize(equation):
#     for i in range(ln):
#         if i % len(Lab) == len(Lab)-1: # (_,l?)
#             r.append(equation[i] == True)
#         else:
#             r.append(equation[i] == False)
#
# def predecessors(lab, *pred):
#     eq_pair = Lab.index(lab) + 1
#     exits = map((lambda x: enex[x][1]), pred)
#     for i in range(ln):
#         preds = map((lambda x: x[i]), exits)
#         r.append(enex[eq_pair][0][i] == union(preds))
#
# def assignment(var, lab):
#     eq_pair = Lab.index(lab) + 1
#     for i in range(ln):
#         if has_v(var, i):
#             if i == I(var, lab):
#                 r.append(enex[eq_pair][1][i] == True)
#             else:
#                 r.append(enex[eq_pair][1][i] == False)
#         else:
#             r.append(enex[eq_pair][1][i] == enex[eq_pair][0][i])
#
# def non_assignment(lab):
#     eq_pair = Lab.index(lab) + 1
#     for i in range(ln):
#         r.append(enex[eq_pair][1][i] == enex[eq_pair][0][i])
#
# def conditional(equation):
#     return None
#
# def loop(equation):
#     return None
#
# s = Solver()
# r = []
# enex = [
#     #TODO This must be generated for every label
#     None,
#     (en1, ex1),
#     (en2, ex2),
#     (en3, ex3),
#     (en4, ex4),
#     (en5, ex5),
#     (en6, ex6)
#     ]
#
# #TODO this must be generated, possibly without comments
# # EN
# initialize(en1)
# predecessors(l2, 1)
# predecessors(l3, 2, 5)
# predecessors(l4, 3)
# predecessors(l5, 4)
# predecessors(l6, 3)
# # EX
# assignment(y, l1)
# assignment(z, l2)
# non_assignment(l3)
# assignment(z, l4)
# assignment(y, l5)
# assignment(y, l6)
#
# s.add(And(r))
# if s.check() == sat:
#     print_model(s.model())
# else:
#     print s.check()

generate.ast("reaching.imp")
