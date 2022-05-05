import ast

def analyze_op(node):

    token_list = []

    if isinstance(node, ast.Add):
        token_list.append("+")
    elif isinstance(node, ast.Sub):
        token_list.append("-")
    elif isinstance(node, ast.Mult):
        token_list.append("*")
    elif isinstance(node, ast.Div):
        token_list.append("/")
    elif isinstance(node, ast.FloorDiv):
        token_list.append("/")
        token_list.append("/")
    elif isinstance(node, ast.Mod):
        token_list.append("%")
    elif isinstance(node, ast.Pow):
        token_list.append("*")
        token_list.append("*")
    elif isinstance(node, ast.LShift):
        token_list.append("<")
        token_list.append("<")
    elif isinstance(node, ast.RShift):
        token_list.append(">")
        token_list.append(">")
    elif isinstance(node, ast.BitOr):
        token_list.append("|")
    elif isinstance(node, ast.BitXor):
        token_list.append("^")
    elif isinstance(node, ast.BitAnd):
        token_list.append("&")
    elif isinstance(node, ast.MatMult):
        token_list.append("@")
    elif isinstance(node, ast.Or):
        token_list.append("or")
    elif isinstance(node, ast.And):
        token_list.append("and")
    elif isinstance(node, ast.UAdd):
        token_list.append("+")
    elif isinstance(node, ast.USub):
        token_list.append("-")
    elif isinstance(node, ast.Not):
        token_list.append("not")
    elif isinstance(node, ast.Invert):
        token_list.append("~")
    return token_list

