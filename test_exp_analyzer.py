

import unittest
import os
import ast

from analyzer_exp import analyze_attribute, analyze_call, analyze_bool_op, analyze_bin_op, analyze_compare, analyze_constant, analyze_dict, analyze_join_str, analyze_list_comp, analyze_set, analyze_lambda, analyze_list, analyze_named_expr, analyze_if_exp, analyze_starred, analyze_subscript, analyze_tuple, analyze_name, analyze_unary_op, analyze_await, analyze_yield, analyze_yield_from

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
        tree = ast.parse("x or y and z")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        self.assertIsInstance(child[0], ast.BoolOp)
        correct_list = ['x', 'or', 'y', 'and', 'z']
        self.assertListEqual(correct_list, analyze_bool_op(child[0]))

    def test_bool_op_exp3(self):
        tree = ast.parse("x or y or z")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        self.assertIsInstance(child[0], ast.BoolOp)
        correct_list = ['x', 'or', 'y', 'or', 'z']
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
    
    def test_bin_op_exp2(self):
        tree = ast.parse("x + y - z")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        correct_list = ['x', '+', 'y', '-', 'z']
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
    
    def test_unary_op_exp1(self):
        tree = ast.parse("-a")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        self.assertIsInstance(child[0], ast.UnaryOp)
        correct_list = ['-', 'a']
        self.assertListEqual(correct_list, analyze_unary_op(child[0]))
    
    def test_unary_op_exp2(self):
        tree = ast.parse("+a")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        self.assertIsInstance(child[0], ast.UnaryOp)
        correct_list = ['+', 'a']
        self.assertListEqual(correct_list, analyze_unary_op(child[0]))

    def test_lambda_exp1(self):
        tree = ast.parse("lambda a, b=1: a + b")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        self.assertIsInstance(child[0], ast.Lambda)
        correct_list = ['lambda', 'a', ',', 'b', '=', '1', ':', 'a', '+', 'b']
        self.assertListEqual(correct_list, analyze_lambda(child[0]))
    def test_lambda_exp2(self):
        tree = ast.parse("lambda a=2, b=1: a + b")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        self.assertIsInstance(child[0], ast.Lambda)
        correct_list = ['lambda', 'a', '=', '2', ',', 'b', '=', '1', ':', 'a', '+', 'b']
        self.assertListEqual(correct_list, analyze_lambda(child[0]))
    
    def test_dict_exp1(self):
        tree = ast.parse("{'a':1, **d}")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        self.assertIsInstance(child[0], ast.Dict)
        correct_list = ['{', '\'', 'a', '\'', ':', '1', ',', '**', 'd', '}']
        self.assertListEqual(correct_list, analyze_dict(child[0]))

    def test_dict_exp2(self):
        tree = ast.parse("{'a':1, 'b':2, **d}")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        self.assertIsInstance(child[0], ast.Dict)
        correct_list = ['{', '\'', 'a', '\'', ':', '1', ',', '\'', 'b', '\'', ':', '2', ',', '**', 'd', '}']
        self.assertListEqual(correct_list, analyze_dict(child[0]))

    def test_constant_exp1(self):
        tree = ast.parse("'a'")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        self.assertIsInstance(child[0], ast.Constant)
        correct_list = ['\'', 'a', '\'']
        self.assertListEqual(correct_list, analyze_constant(child[0]))
    
    def test_constant_exp2(self):
        tree = ast.parse("1")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        self.assertIsInstance(child[0], ast.Constant)
        correct_list = ['1']
        self.assertListEqual(correct_list, analyze_constant(child[0]))
    def test_set_exp1(self):
        tree = ast.parse("{1, 2, 3}")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        self.assertIsInstance(child[0], ast.Set)
        correct_list = ['{', '1', ',', '2', ',', '3', '}']
        self.assertListEqual(correct_list, analyze_set(child[0]))
    
    def test_starred_exp1(self):
        tree = ast.parse("*b")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        self.assertIsInstance(child[0], ast.Starred)
        correct_list = ['*', 'b']
        self.assertListEqual(correct_list, analyze_starred(child[0]))
    def test_list_comp_exp1(self):
        tree = ast.parse("[x for x in numbers]")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        self.assertIsInstance(child[0], ast.ListComp)
        correct_list = ['[', 'x', 'for', 'x', 'in', 'numbers', ']']
        self.assertListEqual(correct_list, analyze_list_comp(child[0]))
    def test_list_comp_exp2(self):
        tree = ast.parse("[i**2 for i in range(5)]")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        self.assertIsInstance(child[0], ast.ListComp)
        correct_list = ['[', 'i', '**', '2', 'for', 'i', 'in', 'range', '(', '5', ')', ']']
        self.assertListEqual(correct_list, analyze_list_comp(child[0]))
    def test_compare_exp1(self):
        tree = ast.parse("1 <= a < 10")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        self.assertIsInstance(child[0], ast.Compare)
        correct_list = ['1', '<=', 'a', '<', '10']
        self.assertListEqual(correct_list, analyze_compare(child[0]))

w        tree = ast.parse("f\"sin({a}) is {sin(a):.3}\"")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        self.assertIsInstance(child[0], ast.JoinedStr)
        correct_list = ['f', ''', 'sin(', '{', 'a', '}', ') is ', '{', 'sin', '(', 'a', ')', ':', '.3', '}', ''']
        self.assertListEqual(correct_list, analyze_join_str(child[0]))
    def test_await_exp1(self):
        tree = ast.parse("await other_func()")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        correct_list = ['await', 'other_func', '(', ')']
        self.assertListEqual(correct_list, analyze_await(child[0]))
    def test_yield_exp1(self):
        tree = ast.parse("yield x")
        child = list(ast.iter_child_nodes(tree))
        child = list(ast.iter_child_nodes(child[0]))
        self.assertIsInstance(child[0], ast.Yield)
        correct_list = ['yield', 'x']
        self.assertListEqual(correct_list, analyze_yield(child[0]))
if __name__ == '__main__':
    unittest.main()