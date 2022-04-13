import unittest
import os
import ast
from ast_analayzer import analyze_class

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


    def test_sample(self):
        path = os.path.join(dir_path, "test_case/test1.py")
        with open(path, "rb") as f:
            src = f.read()
        tree = ast.parse(src)
        correct_list = ['class', 'Base', ':', '\n', '\t', 'def', 'main', '(', ')', ':', '\n', '\t', '\t', 'return', '0']
        for t in ast.walk(tree):
            if isinstance(t, ast.ClassDef):
                self.assertListEqual(correct_list, analyze_class(t))

if __name__ == '__main__':
    unittest.main()