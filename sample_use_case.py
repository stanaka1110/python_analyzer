import ast
from analyzer_stmt import analyze_module
def main():
    with open('/workspaces/docker-python/python_analyzer/test.py', 'rb') as f:
        tree = ast.parse(f.read())
    token_list = analyze_module(tree, 0)
    print(token_list)
    test = ast.parse(" ".join(token_list).replace("\n ", "\n"))

if __name__ == '__main__':
    main()
