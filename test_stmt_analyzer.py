import ast
import os
import unittest

from analyzer_stmt import (analyze_ann_assign, analyze_assert, analyze_assign,
                           analyze_aug_assign, analyze_class_def, analyze_delete, analyze_function_def, analyze_global,
                           analyze_import, analyze_import_from,
                           analyze_nonlocal, analyze_try, analyze_while, analyze_with, analyze_for, analyze_if)

dir_path = os.path.dirname(os.path.realpath(__file__))

class TestAnalyzer(unittest.TestCase):

    def test_delete_stmt1(self):
        tree = ast.parse("del a")
        child = list(ast.iter_child_nodes(tree))
        correct_list = ['del', 'a']
        if isinstance(child[0], ast.Delete):
            self.assertListEqual(correct_list, analyze_delete(child[0]))
    
    def test_delete_stmt2(self):
        tree = ast.parse("del a, b, c")
        child = list(ast.iter_child_nodes(tree))
        correct_list = ['del', 'a', ',', 'b', ',', 'c']
        if isinstance(child[0], ast.Delete):
            self.assertListEqual(correct_list, analyze_delete(child[0]))
            
    def test_assign_stmt1(self):
        tree = ast.parse("a = b = 1")
        child = list(ast.iter_child_nodes(tree))
        correct_list = ['a', '=', 'b', '=', '1']
        if isinstance(child[0], ast.Assign):
            self.assertListEqual(correct_list, analyze_assign(child[0]))
    
    def test_assign_stmt2(self):
        tree = ast.parse("a = b = c")
        child = list(ast.iter_child_nodes(tree))
        correct_list = ['a', '=', 'b', '=', 'c']
        if isinstance(child[0], ast.Assign):
            self.assertListEqual(correct_list, analyze_assign(child[0]))
    
    def test_assign_stmt3(self):
        tree = ast.parse("a = 1")
        child = list(ast.iter_child_nodes(tree))
        correct_list = ['a', '=', '1']
        if isinstance(child[0], ast.Assign):
            self.assertListEqual(correct_list, analyze_assign(child[0]))
    
    def test_assign_stmt4(self):
        tree = ast.parse("a , b = c")
        child = list(ast.iter_child_nodes(tree))
        correct_list = ['a', ',', 'b', '=', 'c']
        if isinstance(child[0], ast.Assign):
            self.assertListEqual(correct_list, analyze_assign(child[0]))
    
    def test_assign_stmt5(self):
        tree = ast.parse("a , b, d = 3")
        child = list(ast.iter_child_nodes(tree))
        correct_list = ['a', ',', 'b', ',', 'd', '=', '3']
        if isinstance(child[0], ast.Assign):
            self.assertListEqual(correct_list, analyze_assign(child[0]))
    
    def test_assign_stmt6(self):
        tree = ast.parse("a[6] = 3")
        child = list(ast.iter_child_nodes(tree))
        correct_list = ['a', '[', '6', ']', '=', '3']
        if isinstance(child[0], ast.Assign):
            self.assertListEqual(correct_list, analyze_assign(child[0]))
    
    def test_assign_stmt7(self):
        tree = ast.parse("c = a[b:5]")
        child = list(ast.iter_child_nodes(tree))
        correct_list = ['c', '=', 'a', '[', 'b', ':', '5', ']']
        if isinstance(child[0], ast.Assign):
            self.assertListEqual(correct_list, analyze_assign(child[0]))
    
    def test_ann_assign_stmt1(self):
        tree = ast.parse("c: int")
        child = list(ast.iter_child_nodes(tree))
        self.assertIsInstance(child[0], ast.AnnAssign)
        correct_list = ['c', ':', 'int']
        self.assertListEqual(correct_list, analyze_ann_assign(child[0]))

    def test_ann_assign_stmt2(self):
        tree = ast.parse("a.b: int")
        child = list(ast.iter_child_nodes(tree))
        self.assertIsInstance(child[0], ast.AnnAssign)
        correct_list = ['a', '.', 'b', ':', 'int']
        self.assertListEqual(correct_list, analyze_ann_assign(child[0]))

    def test_aug_assign_stmt1(self):
        tree = ast.parse("x += 2")
        child = list(ast.iter_child_nodes(tree))
        self.assertIsInstance(child[0], ast.AugAssign)
        correct_list = ['x', '+', '=', '2']
        self.assertListEqual(correct_list, analyze_aug_assign(child[0]))
    
    def test_aug_assign_stmt2(self):
        tree = ast.parse("x /= 2")
        child = list(ast.iter_child_nodes(tree))
        self.assertIsInstance(child[0], ast.AugAssign)
        correct_list = ['x', '/', '=', '2']
        self.assertListEqual(correct_list, analyze_aug_assign(child[0]))
    def test_import_stmt1(self):
        tree = ast.parse("import a, b as c")
        child = list(ast.iter_child_nodes(tree))
        self.assertIsInstance(child[0], ast.Import)
        correct_list = ['import', 'a', ',', 'b', 'as', 'c']
        self.assertListEqual(correct_list, analyze_import(child[0]))

    def test_import_from_stmt2(self):
        tree = ast.parse("from ..d import a, b as c")
        child = list(ast.iter_child_nodes(tree))
        self.assertIsInstance(child[0], ast.ImportFrom)
        correct_list = ['from', '.', '.', 'd', 'import', 'a', ',', 'b', 'as', 'c']
        self.assertListEqual(correct_list, analyze_import_from(child[0]))

    def test_global_stmt1(self):
        tree = ast.parse("global x,y,z")
        child = list(ast.iter_child_nodes(tree))
        self.assertIsInstance(child[0], ast.Global)
        correct_list = ['global', 'x', ',', 'y', ',', 'z']
        self.assertListEqual(correct_list, analyze_global(child[0]))
        
    def test_nonlocal_stmt1(self):
        tree = ast.parse("nonlocal x,y,z")
        child = list(ast.iter_child_nodes(tree))
        self.assertIsInstance(child[0], ast. Nonlocal)
        correct_list = ['nonlocal', 'x', ',', 'y', ',', 'z']
        self.assertListEqual(correct_list, analyze_nonlocal(child[0]))

    def test_assert_stmt1(self):
        tree = ast.parse("assert x,y")
        child = list(ast.iter_child_nodes(tree))
        self.assertIsInstance(child[0], ast.Assert)
        correct_list = ['assert', 'x', ',', 'y']
        self.assertListEqual(correct_list, analyze_assert(child[0]))

    def test_assert_stmt1(self):
        tree = ast.parse("assert(isinstance(x,y))")
        child = list(ast.iter_child_nodes(tree))
        self.assertIsInstance(child[0], ast.Assert)
        correct_list = ['assert',  'isinstance', '(', 'x', ',', 'y', ')']
        self.assertListEqual(correct_list, analyze_assert(child[0]))
    
    def test_try_stmt1(self):
        tree = ast.parse(
            """
try:
    print(1 / 0)
except ZeroDivisionError:
    print('Error')
""")
        child = list(ast.iter_child_nodes(tree))
        self.assertIsInstance(child[0], ast.Try)
        correct_list = ['try', ':', '\n', '\t', '\t', 'print', '(', '1', '/', '0', ')', '\n', 'except', 'ZeroDivisionError', ':', '\n', '\t', '\t', 'print', '(', "'", 'Error', "'", ')', '\n']
        self.assertListEqual(correct_list, analyze_try(child[0], indent_level=1))

    def test_try_stmt2(self):
        tree = ast.parse(
            """
try:
    print(1 / 0)
except ZeroDivisionError:
    print('Error')
else:
    print('Error')
finally :
    print('Error')
""")
        child = list(ast.iter_child_nodes(tree))
        self.assertIsInstance(child[0], ast.Try)
        correct_list = ['try', ':', '\n', '\t', 'print', '(', '1', '/', '0', ')', '\n', 'except', 'ZeroDivisionError', ':', '\n', '\t', 'print', '(', "'", 'Error', "'", ')', '\n', 'else', ':', '\n', '\t', 'print', '(', "'", 'Error', "'", ')', '\n', 'finally', ':', '\n', '\t', 'print', '(', "'", 'Error', "'", ')', '\n']
        self.assertListEqual(correct_list, analyze_try(child[0], indent_level=0))
        #test_parse = ast.parse(" ".join(correct_list).replace("\n ", "\n"))
    def test_with_stmt1(self):
        tree = ast.parse(
            """
with a as b, c as d:
    something(b, d)    
            """)
        child = list(ast.iter_child_nodes(tree))
        self.assertIsInstance(child[0], ast.With)
        correct_list = ['with', 'a', 'as', 'b', ',', 'c', 'as', 'd', ':', '\n', '\t', 'something', '(', 'b', ',', 'd', ')', '\n']
        self.assertListEqual(correct_list, analyze_with(child[0], 0))
        # test_parse = ast.parse(" ".join(correct_list).replace("\n ", "\n"))

    def test_with_stmt2(self):
        tree = ast.parse(
            """
with open("test.txt", "r") as fileread:
    print(fileread.read())  
            """)
        child = list(ast.iter_child_nodes(tree))
        self.assertIsInstance(child[0], ast.With)
        correct_list = ['with', 'open', '(', "'", 'test.txt', "'", ',', "'", 'r', "'", ')', 'as', 'fileread', ':', '\n', '\t', 'print', '(', 'fileread', '.', 'read', '(', ')', ')', '\n']
        self.assertListEqual(correct_list, analyze_with(child[0], 0))
        # test_parse = ast.parse(" ".join(correct_list).replace("\n ", "\n"))
    
    def test_for_stmt1(self):
        tree = ast.parse(
            """
for num in range(5):
    print(num)
            """
        )
        child = list(ast.iter_child_nodes(tree))
        self.assertIsInstance(child[0], ast.For)
        correct_list = ['for', 'num', 'in', 'range', '(', '5', ')', ':', '\n', '\t', 'print', '(', 'num', ')', '\n']
        self.assertListEqual(correct_list, analyze_for(child[0], 0))
    
    def test_if_stmt1(self):
        tree = ast.parse(
            """
if old < 20:
    print("not")
            """
        )
        child = list(ast.iter_child_nodes(tree))
        self.assertIsInstance(child[0], ast.If)
        correct_list = ['if', 'old', '<', '20', ':', '\n', '\t', 'print', '(', "'", 'not', "'", ')', '\n']
        self.assertListEqual(correct_list, analyze_if(child[0], 0))

    def test_if_stmt2(self):
        tree = ast.parse(
            """
if old < 20:
    print("not")
else :
    print("yes")
            """
        )
        child = list(ast.iter_child_nodes(tree))
        self.assertIsInstance(child[0], ast.If)
        correct_list = ['if', 'old', '<', '20', ':', '\n', '\t', 'print', '(', "'", 'not', "'", ')', '\n', 'else', ':', '\n', '\t', 'print', '(', "'", 'yes', "'", ')', '\n']
        self.assertListEqual(correct_list, analyze_if(child[0], 0))

    def test_if_stmt3(self):
        tree = ast.parse(
            """
if old < 20:
    print("not")
elif old > 20:
    print("yes")
else :
    print("no")
            """
        )
        child = list(ast.iter_child_nodes(tree))
        self.assertIsInstance(child[0], ast.If)
        correct_list = ['if', 'old', '<', '20', ':', '\n', '\t', 'print', '(', "'", 'not', "'", ')', '\n', 'elif', 'old', '>', '20', ':', '\n', '\t', 'print', '(', "'", 'yes', "'", ')', '\n', 'else', ':', '\n', '\t', 'print', '(', "'", 'no', "'", ')', '\n']
        self.assertListEqual(correct_list, analyze_if(child[0], 0))

    def test_while_stmt1(self):
        tree = ast.parse(
            """
while num < 2:
    print(str(num))
    num += 1
            """
        )
        child = list(ast.iter_child_nodes(tree))
        self.assertIsInstance(child[0], ast.While)
        correct_list = ['while', 'num', '<', '2', ':', '\n', '\t', 'print', '(', 'str', '(', 'num', ')', ')', '\n', '\t', 'num', '+', '=', '1', '\n']
        self.assertListEqual(correct_list, analyze_while(child[0], 0))
    
    def test_function_def_stmt1(self):
        tree = ast.parse(
            """
def add(a, b):
    x = a + b
    return x
            """
        )
        child = list(ast.iter_child_nodes(tree))
        self.assertIsInstance(child[0], ast.FunctionDef)
        correct_list = ['def', 'add', '(', 'a',',', 'b', ')', ':', '\n', '\t', 'x', '=', 'a', '+', 'b', '\n', '\t', 'return', 'x', '\n']
        self.assertListEqual(correct_list, analyze_function_def(child[0], 0))
    
    def test_class_def_stmt1(self):
        with open('/workspaces/docker-python/python_analyzer/test_case/test2.py', 'rb') as f:
            tree = ast.parse(f.read())
        child = list(ast.iter_child_nodes(tree))
        self.assertIsInstance(child[0], ast.ClassDef)
        token_list = analyze_class_def(child[0], 0)
        test_parse = ast.parse(" ".join(token_list).replace("\n ", "\n"))
