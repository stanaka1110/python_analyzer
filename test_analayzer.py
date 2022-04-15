import unittest
import os
import ast
import astor
from analyzer_cls import analyze_class
from analyzer_func import analyze_func
from analyzer_exp import analyze_call
from analyzer_stmt import analyze_annasign, analyze_delete, analyze_assign


dir_path = os.path.dirname(os.path.realpath(__file__))
class TestAnalayzer(unittest.TestCase):

    def test_class(self):
        path = os.path.join(dir_path, "test_case/test2.py")
        with open(path, "rb") as f:
            src = f.read()
        correct_list = ['class', 'Base1', ':', '\n', '\t','def', 'func1', '(', 'self', ')', ':', '\n', '\t', '\t', 'print', '(', '\'', 'func1', '\'', ')', '\n',
                'class', 'Sub', '(', 'Base1', ')', ':', '\n', '\t', 'def', 'func', '(', 'self', ')', ':', '\n', '\t', '\t', 'super', '(', ')', '.', 'func1', '(', ')']
        tree = ast.parse(src)
        for t in ast.walk(tree):
            if isinstance(t, ast.ClassDef):
                self.assertListEqual(analyze_class(t), correct_list)     

    def test_class_sample(self):
        path = os.path.join(dir_path, "test_case/test1.py")
        with open(path, "rb") as f:
            src = f.read()
        tree = ast.parse(src)
        correct_list = ['class', 'Base', ':', '\n', '\t', 'def', 'test', '(', ')', ':', '\n', '\t', '\t', 'return', '0']
        for t in ast.walk(tree):
            if isinstance(t, ast.ClassDef):
                self.assertListEqual(correct_list, analyze_class(t))
    
    def test_func_sample(self):
        path = os.path.join(dir_path, "test_case/test3.py")

        with open(path, "rb") as f:
            src = f.read()
        
        tree = ast.parse(src)
        correct_list = ['def', 'main', '(', ')', ':', '\n', '\t', 'for', 'line', 'in', 'sys', '.', 'stdin', ':', '\n', '\t', '\t', 'a', ',', 'b', '=', 'map', '(', 'int', ',', 'line', '.', 'split', '(', ')', ')', '\n', '\t', '\t', 'print', '(', 'len', '(', 'str', '(', 'a', '+', 'b', ')', ')', ')']

        for t in ast.walk(tree):
            if isinstance(t, ast.FunctionDef):
                self.assertListEqual(correct_list, analyze_func(t))
    def test_call_exp1(self):
        tree = ast.parse("func(a)")
        child = list(ast.iter_child_nodes(tree))
        call = list(ast.iter_child_nodes(child[0]))

        correct_list = ['func', '(', 'a', ')']
        if isinstance(call[0], ast.Call):
            self.assertListEqual(correct_list, analyze_call(call[0]))
    

    def test_call_exp2(self):
        tree = ast.parse("func(a, b=c, *d, **e)")
        child = list(ast.iter_child_nodes(tree))
        call = list(ast.iter_child_nodes(child[0]))

        correct_list = ['func', '(', 'a', ',', 'b', '=', 'c', ',', '*', 'd', ',', '**', 'e', ')']
        if isinstance(call[0], ast.Call):
            self.assertListEqual(correct_list, analyze_call(call[0]))
    
    def test_call_exp3(self):
        tree = ast.parse("func(a, b)")
        child = list(ast.iter_child_nodes(tree))
        call = list(ast.iter_child_nodes(child[0]))

        correct_list = ['func', '(', 'a', ',', 'b', ')']
        if isinstance(call[0], ast.Call):
            self.assertListEqual(correct_list, analyze_call(call[0]))
    
    def test_call_exp4(self):
        tree = ast.parse("func(a, b=1)")
        child = list(ast.iter_child_nodes(tree))
        call = list(ast.iter_child_nodes(child[0]))

        correct_list = ['func', '(', 'a', ',', 'b', '=', '1',')']
        if isinstance(call[0], ast.Call):
            self.assertListEqual(correct_list, analyze_call(call[0]))
      
    def test_call_exp5(self):
        tree = ast.parse("func(a, *args, **kwargs)")
        child = list(ast.iter_child_nodes(tree))
        call = list(ast.iter_child_nodes(child[0]))

        correct_list = ['func', '(', 'a', ',', '*', 'args', ',','**', 'kwargs', ')']
        if isinstance(call[0], ast.Call):
            self.assertListEqual(correct_list, analyze_call(call[0]))  
        
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
    
    def test_annassign_stmt1(self):
        tree = ast.parse("c: int")
        child = list(ast.iter_child_nodes(tree))
        self.assertIsInstance(child[0], ast.AnnAssign)
        correct_list = ['c', ':', 'int']
        self.assertListEqual(correct_list, analyze_annasign(child[0]))

if __name__ == '__main__':
    unittest.main()