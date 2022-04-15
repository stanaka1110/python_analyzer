import ast
from analyzer_exp import analyze_call


def analyze_for(node, indent_level):

    assert(isinstance(node, ast.For))
    token_list = []
    token_list.append("for")
    target = node.target
    if isinstance(target, ast.Name):
        token_list.append(target.id)
    elif isinstance(target, ast.Tuple):
        child = list(target.elts)
        token_list.append(child[0].id)
        for c in child[1:]:
            token_list.append(",")
            token_list.append(c.id)
    elif isinstance(target, ast.List):
        token_list.append("[")

        child = list(target.elts)
        for c in child[1:]:
            token_list.append(",")
            token_list.append(c.id)
        token_list.append("]")

    token_list.append("in")
    if isinstance(node.iter, ast.Call):
        token_list.extend(analyze_call(node.iter))
    return token_list

def analyze_return(node):
    assert(isinstance(node, ast.Return))
    token_list = []

    token_list.append("return")

    val = node.value.value
    token_list.append(str(val))

    return token_list

def analyze_delete(node):
    assert(isinstance(node, ast.Delete))
    token_list = []

    token_list.append("del")

    target_list = list(node.targets)

    for idx, t in enumerate(target_list):
        if idx != 0:
            token_list.append(",")
        token_list.append(t.id)
    return token_list

def analyze_assign(node):
    assert(isinstance(node, ast.Assign))

    token_list = []
    target_list = list(node.targets)

    if isinstance(target_list[0], ast.Name):
        for idx, t in enumerate(target_list):
            if idx != 0:
                token_list.append("=")
            token_list.append(t.id)
    elif isinstance(target_list[0], ast.Tuple):
        target_list = list(target_list[0].elts)
        for idx, t in enumerate(target_list):
            if idx != 0:
                token_list.append(",")
            token_list.append(t.id)
    token_list.append("=")
    value = node.value
    if isinstance(value, ast.Constant):
        token_list.append(str(value.value))
    elif isinstance(value, ast.Name):
        token_list.append(value.id)
    
    return token_list

def analyze_annasign(node):
    assert(isinstance(node, ast.AnnAssign))
    token_list = []
    return token_list