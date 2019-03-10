from z3 import *
import generate
import sys


# #TODO these must be generated for every variable
# x, y, z = Ints("x y z")
# Var = [x, y, z]
#
# #TODO these must be generated for every label
# l1, l2, l3, l4, l5, l6, lH = Ints("1 2 3 4 5 6 ?")
# Lab = [l1, l2, l3, l4, l5, l6, lH]
#
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

if len(sys.argv) <= 1:
    sys.stderr.write('usage: %s filename\n' % sys.argv[0])
    sys.exit(1)
else:
    stmts = generate.labels(sys.argv[1])
    labs = len(stmts) - 1
    vars = []
    for i in range(1, len(stmts)):
        stmt = stmts[i]
        var = stmt[2]
        if var != None and var not in vars:
            vars.append(var)
    # print stmts
    # print vars, labs

    # Generate temp files

    #DECLARE-Vars
    comma_separated = space_separated = ""
    for v in vars:
        comma_separated = comma_separated + v + ", "
        space_separated = space_separated + v + " "
    comma_separated = comma_separated[:len(comma_separated)-2]
    space_separated = space_separated[:len(space_separated)-1]
    contents = "%s = Ints(\"%s\")\n"%(comma_separated, space_separated)
    contents = contents + "Var = [%s]"%(comma_separated)
    f = open("vars.txt", "w")
    f.write(contents)

    #DECLARE-Labs
    l_comma = []
    l_space = []
    for i in range(1, labs+1):
        l_comma.append("l"+str(i))
        l_space.append(str(i))
    l_comma.append("lH")
    l_space.append("?")
    comma_separated = space_separated = ""
    for l in l_comma:
        comma_separated = comma_separated + l + ", "
    for l in l_space:
        space_separated = space_separated + l + " "
    comma_separated = comma_separated[:-2]
    space_separated = space_separated[:-1]
    contents = "%s = Ints(\"%s\")\n"%(comma_separated, space_separated)
    contents = contents + "Lab = [%s]\n"%(comma_separated)
    f = open("labs.txt", "w")
    f.write(contents)

    #DECLARE-BoolVectors
    contents = ""
    for i in range(1, labs+1):
        contents = contents + "en%s = BoolVector(\"en%s\", ln)\n"%(str(i), str(i))
        contents = contents + "ex%s = BoolVector(\"ex%s\", ln)\n"%(str(i), str(i))
    f = open("boolvectors.txt", "w")
    f.write(contents)

    #DECLARE enex
    contents = "enex =  [\n\tNone\n"
    # for i in range(1, labs+1):
    contents = contents + "\n\t]"
    f = open("enex.txt", "w")
    f.write(contents)


    #DECLARE-statements
    #Consider while/if at start
    contents = "#Statements go here!"
    f = open("statements.txt", "w")
    f.write(contents)
