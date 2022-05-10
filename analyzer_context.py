import ast

from analyzer_exp import analyze_attribute, analyze_constant, analyze_list, analyze_name, analyze_subscript, analyze_tuple

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

def analyze_value(node):
    token_list = []
    if isinstance(node, ast.Attribute):
        token_list.extend(analyze_attribute(node))
    elif isinstance(node, ast.Constant):
        token_list.extend(analyze_constant(node))
    elif isinstance(node, ast.Name):
        token_list.extend(analyze_name(node))
    elif isinstance(node, ast.Tuple):
        token_list.extend(analyze_tuple(node))
    elif isinstance(node, ast.List):
        token_list.extend(analyze_list(node))
    elif isinstance(node, ast.Subscript):
        token_list.extend(analyze_subscript(node))
    else:
        print("error")
        exit()
    
    return token_list