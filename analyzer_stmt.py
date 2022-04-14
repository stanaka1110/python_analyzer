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