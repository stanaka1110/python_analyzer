import ast
from analyzer_func import analyze_func
from analyzer_stmt import analyze_for

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


if __name__ == "__main__":
    with open("test_case/test3.py", "rb") as f:
            src = f.read()
    tree = ast.parse(src)
    for t in ast.walk(tree):
        if isinstance(t, ast.ClassDef):
            print(analyze_class(t))
        elif isinstance(t, ast.FunctionDef):
            print(analyze_func(t))
