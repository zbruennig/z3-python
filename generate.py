from IMP import imp

def recursive_define(ast, stmts, parent):
    if isinstance(ast, imp.Sequence):
        recursive_define(ast.first, stmts, parent)
        recursive_define(ast.second, stmts, parent)
    elif isinstance(ast, imp.While):
        lab = len(stmts)
        stmts.append((lab, "While", None, parent))
        recursive_define(ast.body, stmts, lab)
    elif isinstance(ast, imp.Ite):
        lab = len(stmts)
        stmts.append((lab, "Ite", None, parent))
        recursive_define(ast.true_stmt, stmts, str(lab)+"T")
        recursive_define(ast.false_stmt, stmts, str(lab)+"E")
    elif isinstance(ast, imp.Assignment):
        lab = len(stmts)
        var = ast.name
        stmts.append((lab, "Assignment", var, parent))

def define_statements(ast):
    # Lists are mutable so this will be updated
    list = [None]
    recursive_define(ast, list, None)
    return list

def labels(filename):
    imp_ast = imp.create_ast(filename)
    #CONSIDER NESTED WHILE/IFS
    statements = define_statements(imp_ast)
    return statements
