import warnings
import ast

def analyze_module(node):
    warnings.warn("module deprecated", DeprecationWarning)

    assert(isinstance(node, ast.Module))
    token_list = []
    return token_list

def analyze_expression(node):
    warnings.warn("expression deprecated", DeprecationWarning)

    assert(isinstance(node, ast.Expression))
    token_list = []
    return token_list

def analyze_function_type(node):
    warnings.warn("functiontype deprecated", DeprecationWarning)
    assert(isinstance(node, ast.FunctionType))
    token_list = []
    return token_list
