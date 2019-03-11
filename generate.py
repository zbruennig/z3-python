from IMP import imp
from copy import deepcopy

def recursive_define(ast, stmts, parent):
    if isinstance(ast, imp.Sequence):
        recursive_define(ast.first, stmts, parent)
        recursive_define(ast.second, stmts, parent)
    elif isinstance(ast, imp.While):
        lab = len(stmts)
        stmts.append((lab, "While", None, parent))
        parent_while = deepcopy(parent)
        parent_while.append(str(lab)+"W")
        recursive_define(ast.body, stmts, parent_while)
    elif isinstance(ast, imp.Ite):
        lab = len(stmts)
        stmts.append((lab, "Ite", None, parent))
        parent_then = deepcopy(parent)
        parent_else = deepcopy(parent)
        parent_then.append(str(lab)+"T")
        parent_else.append(str(lab)+"E")
        recursive_define(ast.true_stmt, stmts, parent_then)
        recursive_define(ast.false_stmt, stmts, parent_else)
    elif isinstance(ast, imp.Assignment):
        lab = len(stmts)
        var = ast.name
        stmts.append((lab, "Assignment", var, parent))

def define_statements(ast):
    # Lists are mutable so this will be updated
    list = [None]
    recursive_define(ast, list, [])
    return list

def labels(filename):
    imp_ast = imp.create_ast(filename)
    #CONSIDER NESTED WHILE/IFS
    statements = define_statements(imp_ast)
    return statements
