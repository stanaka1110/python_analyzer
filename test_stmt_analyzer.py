import unittest
import os
import ast

from analyzer_stmt import analyze_annasign, analyze_assign, analyze_delete, analyze_augassign
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
    
    def test_annassign_stmt1(self):
        tree = ast.parse("c: int")
        child = list(ast.iter_child_nodes(tree))
        self.assertIsInstance(child[0], ast.AnnAssign)
        correct_list = ['c', ':', 'int']
        self.assertListEqual(correct_list, analyze_annasign(child[0]))

    def test_annassign_stmt2(self):
        tree = ast.parse("a.b: int")
        child = list(ast.iter_child_nodes(tree))
        self.assertIsInstance(child[0], ast.AnnAssign)
        correct_list = ['a', '.', 'b', ':', 'int']
        self.assertListEqual(correct_list, analyze_annasign(child[0]))

    def test_augassign_stmt1(self):
        tree = ast.parse("x += 2")
        child = list(ast.iter_child_nodes(tree))
        self.assertIsInstance(child[0], ast.AugAssign)
        correct_list = ['x', '+', '=', '2']
        self.assertListEqual(correct_list, analyze_augassign(child[0]))
    
    def test_augassign_stmt2(self):
        tree = ast.parse("x /= 2")
        child = list(ast.iter_child_nodes(tree))
        self.assertIsInstance(child[0], ast.AugAssign)
        correct_list = ['x', '/', '=', '2']
        self.assertListEqual(correct_list, analyze_augassign(child[0]))