import ast

def analyze_name(node):
    assert(isinstance(node, ast.Name))
    token_list = []
    token_list.append(node.id)
    return token_list