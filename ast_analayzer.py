import ast


def analyze_class(node, indent_level=1):
    assert(isinstance(node, ast.ClassDef))

    token_list = []

    token_list.append("class")
    token_list.append(node.name)
    
    if len(node.bases) != 0:
        token_list.append("(")
        token_list.append(node.bases[0].id)
        for base in node.bases[1:]:
            token_list.append(",")
            token_list.append(base.id)
        token_list.append(")")
    
    token_list.append(":")

    token_list.append("\n")
    for _ in range(indent_level):
        token_list.append("\t")

    body_list = list(node.body)
    for body in body_list:
        if isinstance(body, ast.FunctionDef):
            token_list.extend(analyze_func(body, indent_level=2))

    return token_list

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
        
        if isinstance(b, ast.Return):
            token_list.extend(analyze_return(b))
    
    return token_list

def analyze_return(node):
    token_list = []

    token_list.append("return")

    val = node.value.value
    token_list.append(str(val))

    return token_list
    

if __name__ == "__main__":
    with open("test_case/test1.py", "rb") as f:
            src = f.read()
    tree = ast.parse(src)
    for t in ast.walk(tree):
        if isinstance(t, ast.ClassDef):
            print(analyze_class(t))
