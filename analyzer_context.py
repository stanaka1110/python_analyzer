import ast
import enum
from lib2to3.pgen2 import token

def analyze_name(node):
    assert(isinstance(node, ast.Name))
    token_list = []
    token_list.append(node.id)
    return token_list

def analyze_attribute(node):
    assert(isinstance(node, ast.Attribute))
    token_list = []
    if isinstance(node.value, ast.Name):
        token_list.extend(analyze_name(node.value))
    elif isinstance(node.value, ast.Attribute):
        token_list.extend(analyze_attribute(node.value))
    token_list.append(".")
    token_list.append(node.attr)
    return token_list

def analyze_constant(node):
    assert(isinstance(node, ast.Constant))
    token_list = [str(node.value)]
    return token_list

def analyze_tuple(node):
    assert(isinstance(node, ast.Tuple))
    token_list = []
    elts_list = node.elts
    for idx, e in enumerate(elts_list):
        if idx != 0:
            token_list.append(",")
        if isinstance(e, ast.Constant):
            token_list.extend(analyze_constant(e))
        elif isinstance(e, ast.Name):
            token_list.extend(analyze_name(e))
        
    
    return token_list

def analyze_list(node):
    assert(isinstance(node, ast.List))

    token_list = []
    token_list.append("[")
    elts_list = node.elts
    for idx, e in enumerate(elts_list):
        if idx != 0:
            token_list.append(",")
        if isinstance(e, ast.Name):
            token_list.extend(analyze_name(e))
        elif isinstance(e, ast.Constant):
            token_list.extend(analyze_constant(e))
    
    token_list.append("]")
    return token_list

def analyze_slice(node):
    assert(node, ast.Slice)
    token_list = []
    l = node.lower
    u = node.upper
    if isinstance(l, ast.Name):
        token_list.extend(analyze_name(l))
    elif isinstance(l, ast.Constant):
        token_list.extend(analyze_constant(l))
    token_list.append(":")
    if isinstance(u, ast.Name):
        token_list.extend(analyze_name(u))
    
    elif isinstance(u, ast.Constant):
        token_list.extend(analyze_constant(u))
    return token_list