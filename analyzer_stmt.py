import ast
from analyzer_exp import analyze_call
from analyzer_context import analyze_attribute, analyze_name, analyze_tuple

def analyze_for(node, indent_level):

    assert(isinstance(node, ast.For))
    token_list = []
    token_list.append("for")
    target = node.target
    if isinstance(target, ast.Name):
        token_list.extend(analyze_name(target))
    elif isinstance(target, ast.Tuple):
        child = list(target.elts)
        token_list.extend(analyze_tuple(child))
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
        token_list.extend(analyze_name(t))
    return token_list

def analyze_assign(node):
    assert(isinstance(node, ast.Assign))

    token_list = []
    target_list = list(node.targets)

    if isinstance(target_list[0], ast.Name):
        for idx, t in enumerate(target_list):
            if idx != 0:
                token_list.append("=")
            token_list.extend(analyze_name(t))
    elif isinstance(target_list[0], ast.Tuple):
        token_list.extend(analyze_tuple(target_list[0]))
    token_list.append("=")
    value = node.value
    if isinstance(value, ast.Constant):
        token_list.append(str(value.value))
    elif isinstance(value, ast.Name):
        token_list.extend(analyze_name(value))
    
    return token_list

def analyze_annasign(node):
    assert(isinstance(node, ast.AnnAssign))
    token_list = []

    target = node.target
    if isinstance(target, ast.Name):
        token_list.extend(analyze_name(target))
    elif isinstance(target, ast.Attribute):
        token_list.extend(analyze_attribute(target))
    token_list.append(":")
    token_list.extend(analyze_name(node.annotation))
    return token_list