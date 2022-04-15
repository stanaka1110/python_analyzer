import ast
from analyzer_context import analyze_name
def analyze_call(node):
    assert(isinstance(node, ast.Call))
    token_list = []

    token_list.append(node.func.id)
    token_list.append("(")

    arg_list = list(node.args)
    print(arg_list)

    tmp_list = []
    for idx, a in enumerate(arg_list):
        if idx != 0:
            token_list.append(",")
        
        if isinstance(a, ast.Attribute):
            token_list.append(a.value.id)
            token_list.append(".")
            token_list.append(a.attr)
        
        elif isinstance(a, ast.Name):
            token_list.extend(analyze_name(a))
        
        elif isinstance(a, ast.Starred):
            token_list.pop(-1)
            tmp_list.append("*")
            tmp_list.append(a.value.id)
    
    keyword_list = node.keywords
    if len(keyword_list) != 0:
        token_list.append(",")
    else:
        token_list.extend(tmp_list)
    for idx, k in enumerate(keyword_list):

        if idx != 0:
            token_list.append(",")
        
        if k.arg != None:
            token_list.append(k.arg)
            token_list.append("=")
            if isinstance(k.value, ast.Name):
                token_list.extend(analyze_name(k.value))
            elif isinstance(k.value, ast.Constant):
                token_list.append(str(k.value.value))
        else:
            token_list.extend(tmp_list)
            token_list.append(",")
            token_list.append("**")
            token_list.append(k.value.id)
    
    token_list.append(")")

    return token_list

