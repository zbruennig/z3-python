from z3 import *
import generate
import sys

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
    print stmts

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
    contents = "enex = [\n\tNone"
    for i in range(1, labs+1):
        contents = contents + ",\n\t(en%s, ex%s)"%(str(i), str(i))
    contents = contents + "\n]\n"
    f = open("enex.txt", "w")
    f.write(contents)


    statements = [
        "initialize(en1)",
        "predecessors(l2, 1)",
        "predecessors(l4, 3)",
        "predecessors(l3, 2, 5)",
        "predecessors(l5, 4)",
        "predecessors(l6, 3)",
        "assignment(Y, l1)",
        "assignment(Z, l2)",
        "non_assignment(l3)",
        "assignment(Z, l4)",
        "assignment(Y, l5)",
        "assignment(Y, l6)"
    ]
    #Logic to build statements
    #DECLARE-statements
    #Consider while/if at start
    contents = ""
    for s in statements:
        contents = contents + "%s\n"%(s)
    f = open("statements.txt", "w")
    f.write(contents)
