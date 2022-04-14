import ast
from analyzer_stmt import analyze_for
from analyzer_exp import analyze_return

def analyze_func(node, indent_level=1):
    assert(isinstance(node, ast.FunctionDef))

    token_list = []
    token_list.append("def")
    token_list.append(node.name)

    token_list.append("(")
    args_list = node.args.args
    if len(args_list) != 0:
        token_list.append(args_list[0].arg)
        for a in args_list[1:]:
            token_list.append(",")
            token_list.append(a.arg)
    token_list.append(")")

    token_list.append(":")

    body_list = list(node.body)
    for b in body_list:
        token_list.append("\n")
        for _ in range(indent_level):
            token_list.append("\t")
        
        if isinstance(b, ast.For):
            token_list.extend(analyze_for(b, indent_level+1))

        if isinstance(b, ast.Return):
            token_list.extend(analyze_return(b))
    
    return token_list