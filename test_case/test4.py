import ast


tree = ast.parse("del a")
child = list(ast.iter_child_nodes(tree))
print(tree)
correct_list = ['del', 'a']
print(child)
if isinstance(child[0], ast.Del):
    analyze_del(child[0])