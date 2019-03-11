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

def parents_changed(l1, l2):
    # Determines which parents have changed, from l1 to l2, in that order
    if len(l1) == len(l2) and len(l1) > 0:
        # Either nothing changed or a Then became an Else
        end1 = l1[-1]
        end2 = l2[-1]
        type1 = end1[-1:]
        type2 = end2[-1:]
        if type1 == "T" and type2 == "E":
            return [end1[:-1] + "T"], "%"
    elif len(l1) < len(l2):
        # Stack gained exactly one parent, entered an Ite or While
        return [l2[-1]], "+"
    elif len(l1) > len(l2):
        # One or more parents have dropped from stack,
        # They are of type While or Else, never Then
        return l1[len(l2):], "-"
    return [], "="

def things_before(s, i):
    curr = s[i]
    prev = s[i-1]
    diff, action = parents_changed(prev[3], curr[3])
    if action == "%":
        # Start of an Else block, before is the If conditional
        # Label is located at the end of Parent stack
        return [int(curr[3][-1][:-1])]
    elif action == "+":
        # Previous statement was a While or Ite, this is the first
        # Statement in the block, Label is simply i-1
        return [i-1]
    elif action == "=":
        # In same context as previous statement, this is the basic default
        # Case of just a sequence of statements, no larger structure
        return [i-1]
    elif action == "-":
        print diff, "-"
        # One or more parents were popped from the stack.
        # If this includes a While, then we need to add the condition label
        # Of the while. However if this includes an Ite, we need to add
        # Both branches, and we read the Parents list left to right,
        # Starting with the outermost structure.
        before = []

        def find_t_e(start, cond, rest):
            cond_t = str(cond)+"T"
            cond_e = str(cond)+"E"
            state = 0
            search = else_loc = i-1
            then_loc = -1
            while search > 0:
                stmt = s[search]
                parents = stmt[3]
                if cond_t in parents:
                    then_loc = search
                    break
                search = search - 1
            # Once we have the locations of the last statement in the Then and
            # Else branches, we check to see if those are within a While loop
            # or in a nested Ite statement, and deal with them accordingly
            then_parents = s[then_loc][3]
            then_index = then_parents.index(cond_t)
            then_after = then_parents[then_index+1:]
            if then_after == []:
                before.append(then_loc)
            elif then_after[0][-1:] == "W":
                before.append(int(then_after[0][:-1]))
            else:
                find_t_e(then_loc+1, int(then_after[0][:-1]), then_after[1:])
            else_parents = s[else_loc][3]
            else_index = else_parents.index(cond_e)
            else_after = else_parents[else_index+1:]
            if else_after == []:
                before.append(else_loc)
            elif else_after[0][-1:] == "W":
                before.append(int(else_after[0][:-1]))
            else:
                find_t_e(else_loc+1, int(else_after[0][:-1]), else_after[1:])

        if diff[0][-1:] == "W":
            before.append(int(diff[0][:-1]))
        else:
            find_t_e(i, int(diff[0][:-1]), diff[1:])
        print before
        return before

    # The above block should cover all cases
    # Reaching this line should be an error
    sys.stderr.write("Unknown symbol %s parsed in things_before"%action)
    sys.exit(1)

def ends_of_while(s, i):
    curr = s[i]
    return [1]

def make_predecessors(l, s, i):
    #curr = (Lab-0, Type-1, Var-2 [unused], Parents-3)
    if i > len(s) - 1:
        return
    curr = s[i]
    predecessors = []
    if i==1 and curr[1] != "While":
        make_predecessors(l, s, i+1)
        return
    if i!=1:
        before = things_before(s, i)
        for e in before:
            predecessors.append(e)
    if curr[1] == "While":
        ends = ends_of_while(s, i)
        for e in ends:
            predecessors.append(e)
    command = "predecessors(l%s"%(str(i))
    for p in predecessors:
        command = command + ", %s"%(str(p))
    command = command+")"
    l.append(command)
    make_predecessors(l, s, i+1)


def build_statements(l, s):
    # EN_i definitions
    l.append("initialize(en1)")
    # Work through predecessors for:
    # Ite, While, Nested Statements, and Assignment
    make_predecessors(l, s, 1)
    # EX_i definitions
    for i in range(1, len(s)):
        cur = s[i]
        if cur[1] == "Assignment":
            l.append("assignment(%s, l%s)"%(cur[2], str(cur[0])))
        else:
            l.append("non_assignment(l%s)"%(str(cur[0])))

stmts = generate.labels(sys.argv[1])
labs = len(stmts) - 1
vars = []
for i in range(1, len(stmts)):
    stmt = stmts[i]
    var = stmt[2]
    if var != None and var not in vars:
        vars.append(var)

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

#DECLARE-statements
lst = []
build_statements(lst, stmts)
contents = ""
for s in lst:
    contents = contents + "%s\n"%(s)
f = open("statements.txt", "w")
f.write(contents)
