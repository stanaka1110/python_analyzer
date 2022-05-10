
import unittest
import os
import ast

from analyzer_exp import analyze_attribute, analyze_call, analyze_bool_op, analyze_bin_op, analyze_constant, analyze_list, analyze_named_expr, analyze_if_exp, analyze_subscript, analyze_tuple, analyze_name

dir_path = os.path.dirname(os.path.realpath(__file__))

class TestExpAnalyzer(unittest.TestCase):

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

    def test_bool_op_exp1(self):
        tree = ast.parse("x or y")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        self.assertIsInstance(child[0], ast.BoolOp)
        correct_list = ['x', 'or', 'y']
        self.assertListEqual(correct_list, analyze_bool_op(child[0]))
    
    def test_bool_op_exp2(self):
        tree = ast.parse("x or y or z")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        self.assertIsInstance(child[0], ast.BoolOp)
        correct_list = ['x', 'or', 'y', 'and', 'z']
        self.assertListEqual(correct_list, analyze_bool_op(child[0]))
    
    def test_named_expr_exp1(self):
        tree = ast.parse("(x := 4)")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        correct_list = ['(', 'x', ':', '=', '4', ')']
        self.assertListEqual(correct_list, analyze_named_expr(child[0]))
    
    def test_bin_op_exp1(self):
        tree = ast.parse("x + y")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        correct_list = ['x', '+', 'y']
        self.assertListEqual(correct_list, analyze_bin_op(child[0]))
    
    def test_if_exp_exp1(self):
        tree = ast.parse("a if b else c")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        correct_list = ['a', 'if', 'b', 'else', 'c']
        self.assertListEqual(correct_list, analyze_if_exp(child[0]))

    def test_attribute_exp1(self):
        tree = ast.parse("snake.colour")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        self.assertIsInstance(child[0], ast.Attribute)
        correct_list = ['snake', '.', 'colour']
        self.assertListEqual(correct_list, analyze_attribute(child[0]))

    def test_attribute_exp2(self):
        tree = ast.parse("snake.colour.red")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        self.assertIsInstance(child[0], ast.Attribute)
        correct_list = ['snake', '.', 'colour', '.', 'red']
        self.assertListEqual(correct_list, analyze_attribute(child[0]))
    
    def test_constant_exp1(self):
        tree = ast.parse("1")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        self.assertIsInstance(child[0], ast.Constant)
        correct_list = ['1']
        self.assertListEqual(correct_list, analyze_constant(child[0]))

    def test_tuple_exp1(self):
        tree = ast.parse("(1, 2, 3)")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        self.assertIsInstance(child[0], ast.Tuple)
        correct_list = ['1', ',', '2', ',', '3']
        self.assertListEqual(correct_list, analyze_tuple(child[0]))
    
    def test_list_exp1(self):
        tree = ast.parse("[1, 2]")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))

        self.assertIsInstance(child[0], ast.List)
        correct_list = ['[', '1', ',', '2', ']']
        self.assertListEqual(correct_list, analyze_list(child[0]))
    
    def test_list_exp2(self):
        tree = ast.parse("[a, 2]")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))

        self.assertIsInstance(child[0], ast.List)
        correct_list = ['[', 'a', ',', '2', ']']
        self.assertListEqual(correct_list, analyze_list(child[0]))

    def test_subscript_exp1(self):
        tree = ast.parse("a[0]")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        self.assertIsInstance(child[0], ast.Subscript)
        correct_list = ['a', '[', '0', ']']
        self.assertListEqual(correct_list, analyze_subscript(child[0]))
    
    def test_subscript_exp2(self):
        tree = ast.parse("a[1, 3]")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        self.assertIsInstance(child[0], ast.Subscript)
        correct_list = ['a', '[', '1', ',', '3', ']']
        self.assertListEqual(correct_list, analyze_subscript(child[0]))
    
    def test_subscript_exp3(self):
        tree = ast.parse("a[1:3]")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        self.assertIsInstance(child[0], ast.Subscript)
        correct_list = ['a', '[', '1', ':', '3', ']']
        self.assertListEqual(correct_list, analyze_subscript(child[0]))

if __name__ == '__main__':
    unittest.main()