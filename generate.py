from IMP import imp
from copy import deepcopy

def recursive_define(ast, stmts, parent):
    # Parent is a stack of nested statements for the label, Ites and Whiles
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
    elif isinstance(ast, imp.Skip):
        lab = len(stmts)
        stmts.append((lab, "Skip", None, parent))

def add_from_aexp(expr, vars):
    if isinstance(expr, imp.IntAexp):
        pass
    elif isinstance(expr, imp.VarAexp):
        if expr.name not in vars:
            vars.append(expr.name)
    elif isinstance(expr, imp.BinopAexp):
        add_from_aexp(expr.left, vars)
        add_from_aexp(expr.right, vars)

def add_from_bexp(expr, vars):
    if isinstance(expr, imp.RelopBexp):
        add_from_aexp(expr.left, vars)
        add_from_aexp(expr.right, vars)
    elif isinstance(expr, imp.AndBexp):
        add_from_bexp(expr.left, vars)
        add_from_bexp(expr.right, vars)
    elif isinstance(expr, imp.OrBexp):
        add_from_bexp(expr.left, vars)
        add_from_bexp(expr.right, vars)
    elif isinstance(expr, imp.NotBexp):
        add_from_bexp(expr.exp, vars)

def recursive_add(ast, vars):
    if isinstance(ast, imp.Sequence):
        recursive_add(ast.first, vars)
        recursive_add(ast.second, vars)
    elif isinstance(ast, imp.While):
        add_from_bexp(ast.condition, vars)
        recursive_add(ast.body, vars)
    elif isinstance(ast, imp.Ite):
        add_from_bexp(ast.condition, vars)
        recursive_add(ast.true_stmt, vars)
        recursive_add(ast.false_stmt, vars)
    elif isinstance(ast, imp.Assignment):
        add_from_aexp(ast.aexp, vars)
    elif isinstance(ast, imp.Skip):
        pass

def define_variables(ast):
    vars = []
    recursive_add(ast, vars)
    return vars

def define_statements(ast):
    # Lists are mutable so this will be updated
    list = [None]
    recursive_define(ast, list, [])
    return list

def process_tree(filename):
    imp_ast = imp.create_ast(filename)
    statements = define_statements(imp_ast)
    vars = define_variables(imp_ast)
    return vars, statements
