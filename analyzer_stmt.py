import ast
from lib2to3.pgen2 import token
import warnings

from analyzer_context import  analyze_alias, analyze_op
from analyzer_exp import analyze_call, analyze_value, analyze_expr
def analyze_module(node, indent_level=0):
    assert(isinstance(node, ast.Module))
    token_list = []
    for b in node.body:
        token_list.extend(["\t"]*(indent_level))
        token_list.extend(analyze_stmt(b, indent_level))
        token_list.append("\n")
    return token_list

def analyze_arguments(node):
    assert(isinstance(node, ast.arguments))
    arg_list = list(node.args)
    token_list = []

    for idx, a in enumerate(arg_list):
        if idx != 0:
            token_list.append(",")
        token_list.extend(analyze_arg(a))
    return token_list

def analyze_arg(node):
    assert(isinstance(node, ast.arg))
    token_list = []
    token_list.append(node.arg)
    return token_list

def analyze_function_def(node, indent_level=0):
    assert(isinstance(node, ast.FunctionDef))
    token_list = []
    token_list.append("def")
    token_list.append(node.name)

    token_list.append("(")
    token_list.extend(analyze_arguments(node.args))
    token_list.append(")")

    token_list.append(":")
    token_list.append("\n")
    body_list = list(node.body)
    for b in body_list:
        token_list.extend(["\t"]*(indent_level+1))
        token_list.extend(analyze_stmt(b, indent_level+1))
        token_list.append("\n")
    
    return token_list

def analyze_async_function_def(node, indent_level=0):
    assert(isinstance(node, ast.AsyncFunctionDef))
    token_list = []
    token_list.append("async")
    token_list.append("def")
    token_list.append(node.name)

    token_list.append("(")
    token_list.extend(analyze_arguments(node.args))
    token_list.append(")")

    token_list.append(":")
    token_list.append("\n")
    body_list = list(node.body)
    for b in body_list:
        token_list.extend(["\t"]*(indent_level+1))
        token_list.extend(analyze_stmt(b, indent_level+1))
        token_list.append("\n")
    
    return token_list

def analyze_class_def(node, indent_level=0):
    warnings.warn("class_def deprecation", DeprecationWarning)
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
    body_list = list(node.body)
    for b in body_list:
        token_list.extend(["\t"]*(indent_level+1))
        token_list.extend(analyze_stmt(b, indent_level+1))
        token_list.append("\n")

    return token_list

def analyze_return(node):

    assert(isinstance(node, ast.Return))
    token_list = []

    token_list.append("return")
    token_list.extend(analyze_expr(node.value))

    return token_list

def analyze_delete(node):
    assert(isinstance(node, ast.Delete))
    token_list = []

    token_list.append("del")

    target_list = list(node.targets)

    for idx, t in enumerate(target_list):
        if idx != 0:
            token_list.append(",")
        token_list.extend(analyze_expr(t))
    return token_list

def analyze_assign(node):
    assert(isinstance(node, ast.Assign))

    token_list = []
    target_list = list(node.targets)
    for idx, t in enumerate(target_list):
        if idx != 0:
            token_list.append("=")
        token_list.extend(analyze_expr(t))
    token_list.append("=")
    value = node.value
    token_list.extend(analyze_expr(value))
    
    return token_list

def analyze_ann_assign(node):
    assert(isinstance(node, ast.AnnAssign))
    token_list = []

    target = node.target
    token_list.extend(analyze_value(target))
    token_list.append(":")
    token_list.extend(analyze_value(node.annotation))
    return token_list

def analyze_aug_assign(node):
    assert(isinstance(node, ast.AugAssign))
    token_list = []
    token_list.extend(analyze_value(node.target))
    
    token_list.extend(analyze_op(node.op))
    token_list.append("=")


    token_list.extend(analyze_value(node.value))

    return token_list

def analyze_for(node, indent_level):
    assert(isinstance(node, ast.For))
    token_list = []
    token_list.append("for")
    token_list.extend(analyze_expr(node.target))
    token_list.append("in")
    token_list.extend(analyze_expr(node.iter))
    token_list.append(":")
    token_list.append("\n")
    for b in node.body:
        token_list.extend(["\t"]*(indent_level+1))
        token_list.extend(analyze_stmt(b, indent_level+1))
        token_list.append("\n")
    if len(node.orelse) != 0:
        token_list.append("else")
        token_list.append(":")
        token_list.append("\n")
        for o in node.orelse:
            token_list.extend(["\t"]*(indent_level+1))
            token_list.extend(analyze_stmt(o, indent_level+1))
            token_list.append("\n")
    return token_list

def analyze_async_for(node, indent_level):
    assert(isinstance(node, ast.AsyncFor))
    token_list = []
    token_list.append("async")
    token_list.append("for")
    token_list.extend(analyze_expr(node.target))
    token_list.append("in")
    token_list.extend(analyze_expr(node.iter))
    token_list.append(":")
    token_list.append("\n")
    for b in node.body:
        token_list.extend(["\t"]*(indent_level+1))
        token_list.extend(analyze_stmt(b, indent_level+1))
        token_list.append("\n")
    if len(node.orelse) != 0:
        token_list.append("else")
        token_list.append(":")
        token_list.append("\n")
        for o in node.orelse:
            token_list.extend(["\t"]*(indent_level+1))
            token_list.extend(analyze_stmt(o, indent_level+1))
            token_list.append("\n")
    return token_list

def analyze_while(node, indent_level):
    assert(isinstance(node, ast.While))
    token_list = []
    token_list.append("while")
    token_list.extend(analyze_expr(node.test))
    token_list.append(":")
    token_list.append("\n")
    for b in node.body:
        token_list.extend(["\t"]*(indent_level+1))
        token_list.extend(analyze_stmt(b, indent_level+1))
        token_list.append("\n")
    if len(node.orelse) != 0:
        token_list.append("else")
        token_list.append(":")
        token_list.append("\n")
        for o in node.orelse:
            token_list.extend(["\t"]*(indent_level+1))
            token_list.extend(analyze_stmt(o, indent_level+1))
            token_list.append("\n")
    return token_list

def analyze_if(node, indent_level):
    assert(isinstance(node, ast.If))
    token_list = []
    token_list.append("if")
    token_list.extend(analyze_expr(node.test))
    token_list.append(":")
    token_list.append("\n")
    for b in node.body:
        token_list.extend(["\t"]*(indent_level+1))
        token_list.extend(analyze_stmt(b, indent_level+1))
        token_list.append("\n")
    if len(node.orelse) != 0:
        token_list.extend(["\t"]*(indent_level))
        token_list.extend(analyze_elif(node.orelse[0], indent_level))
    return token_list

def analyze_elif(node, indent_level):

    token_list = []
    if not isinstance(node, ast.If):
        token_list.append("else")
        token_list.append(":")
        token_list.append("\n")
        if  not isinstance(node, ast.Expr):
            for o in list(node):
                token_list.extend(["\t"]*(indent_level+1))
                token_list.extend(analyze_stmt(o, indent_level+1))
                token_list.append("\n")
        else:
            token_list.extend(["\t"]*(indent_level+1))
            token_list.extend(analyze_stmt(node, indent_level+1))
            token_list.append("\n")
    else:
        token_list.append("elif")
        token_list.extend(analyze_expr(node.test))
        token_list.append(":")
        token_list.append("\n")
        for b in node.body:
            token_list.extend(["\t"]*(indent_level+1))
            token_list.extend(analyze_stmt(b, indent_level+1))
            token_list.append("\n")
        if len(node.orelse) != 0:
            token_list.extend(analyze_elif(node.orelse, indent_level))
    
    return token_list

def analyze_with(node, indent_level):
    assert(isinstance(node, ast.With))
    token_list = []
    token_list.append("with")
    for idx, i in enumerate(node.items):
        if idx != 0:
            token_list.append(",")
        token_list.extend(analyze_expr(i.context_expr))
        token_list.append("as")
        token_list.extend(analyze_expr(i.optional_vars))
    token_list.append(":")
    token_list.append("\n")
    for b in node.body:
        token_list.extend(["\t"]*(indent_level+1))
        token_list.extend(analyze_stmt(b, indent_level))
        token_list.append("\n")
    
    return token_list

def analyze_async_with(node, indent_level):
    assert(isinstance(node, ast.AsyncWith))
    token_list = []
    token_list.append("async")
    token_list.append("with")
    for idx, i in enumerate(node.items):
        if idx != 0:
            token_list.append(",")
        token_list.extend(analyze_expr(i.context_expr))
        token_list.append("as")
        token_list.extend(analyze_expr(i.optional_vars))
    token_list.append(":")
    token_list.append("\n")
    for b in node.body:
        token_list.extend(["\t"]*(indent_level+1))
        token_list.extend(analyze_stmt(b, indent_level))
        token_list.append("\n")
    
    return token_list

def analyze_raise(node):
    assert(isinstance(node, ast.Raise))
    token_list = []
    token_list.append("raise")
    token_list.extend(analyze_expr(node.exc))
    if node.cause != None:
        token_list.append("from")
        token_list.extend(analyze_expr(node.cause))
    return token_list

def analyze_try(node, indent_level):
    warnings.warn("try deprecation", DeprecationWarning)
    assert(isinstance(node, ast.Try))
    token_list = []
    token_list.append("try")
    token_list.append(":")
    token_list.append("\n")
    for b in node.body:
        token_list.extend(["\t"]*(indent_level+1))
        token_list.extend(analyze_stmt(b, indent_level))
    token_list.append("\n")
    if len(node.handlers) != 0:
        for e in node.handlers:
            token_list.extend(["\t"]*(indent_level)) 
            token_list.extend(analyze_except_handler(e, indent_level))
    
    if len(node.orelse) != 0:
        token_list.extend(["\t"]*(indent_level)) 
        token_list.append("else")
        token_list.append(":")
        token_list.append("\n")
        for o in node.orelse:
            token_list.extend(["\t"]*(indent_level+1))
            token_list.extend(analyze_stmt(o, indent_level))
            token_list.append("\n")
    if len(node.finalbody) != 0:
        token_list.extend(["\t"]*(indent_level)) 
        token_list.append("finally")
        token_list.append(":")
        token_list.append("\n")
        for f in node.finalbody:
            token_list.extend(["\t"]*(indent_level+1))
            token_list.extend(analyze_stmt(f, indent_level))
            token_list.append("\n")
        
    return token_list

def analyze_except_handler(node, indent_level):
    assert(isinstance(node, ast.ExceptHandler))
    token_list = []
    token_list.append("except")
    token_list.extend(analyze_expr(node.type))
    if node.name != None:
        token_list.append("as")
        token_list.append(node.name)
    token_list.append(":")
    token_list.append("\n")
    for b in node.body:
        token_list.extend(["\t"]*(indent_level+1))
        token_list.extend(analyze_stmt(b, indent_level))
        token_list.append("\n")
    return token_list

def analyze_assert(node):
    assert(isinstance(node, ast.Assert))
    token_list = []
    token_list.append("assert")
    token_list.extend(analyze_expr(node.test))
    if node.msg != None:
        token_list.append(",")
        token_list.extend(analyze_expr(node.msg))

    return token_list

def analyze_import(node):
    assert(isinstance(node, ast.Import))
    token_list = []
    token_list.append("import")
    for idx, n in enumerate(node.names):
        if idx != 0:
            token_list.append(",")
        token_list.extend(analyze_alias(n))
    return token_list

def analyze_import_from(node):
    assert(isinstance(node, ast.ImportFrom))
    token_list = []
    token_list.append("from")
    for _ in range(node.level):
        token_list.append(".")
    token_list.append(node.module)
    token_list.append("import")
    for idx, n in enumerate(node.names):
        if idx != 0:
            token_list.append(",")
        token_list.extend(analyze_alias(n))
    return token_list

def analyze_global(node):
    assert(isinstance(node, ast.Global))
    token_list = []
    token_list.append("global")
    for idx, n in enumerate(node.names):
        if idx != 0:
            token_list.append(",")
        token_list.append(n)
    return token_list
def analyze_wait(node):
    assert(isinstance(node, ast.Await))
    token_list = []
    token_list.append("await")
    token_list.extend(analyze_exp(node.value))
def analyze_nonlocal(node):
    token_list = []
    token_list.append("nonlocal")
    for idx, n in enumerate(node.names):
        if idx != 0:
            token_list.append(",")
        token_list.append(n)
    return token_list

def analyze_pass(node):
    assert(isinstance(node, ast.Pass))
    return ["pass"]

def analyze_break(node):
    assert(isinstance(node, ast.Break))
    return ["break"]

def analyze_continue(node):
    assert(isinstance(node, ast.Continue))
    return ["continue"]

def analyze_exp(node):
    assert(isinstance(node, ast.Expr))
    token_list = []
    token_list.extend(analyze_expr(node.value))
    return token_list

def analyze_stmt(node, indent_level=1):
    token_list = []
    if isinstance(node, ast.FunctionDef):
        token_list.extend(analyze_function_def(node, indent_level))
    elif isinstance(node, ast.AsyncFunctionDef):
        token_list.extend(analyze_async_function_def(node, indent_level))
    elif isinstance(node, ast.ClassDef):
        token_list.extend(analyze_class_def(node, indent_level))
    elif isinstance(node, ast.Return):
        token_list.extend(analyze_return(node))
    elif isinstance(node, ast.Delete):
        token_list.extend(analyze_delete(node))
    elif isinstance(node, ast.Assign):
        token_list.extend(analyze_assign(node))
    elif isinstance(node, ast.AugAssign):
        token_list.extend(analyze_aug_assign(node))
    elif isinstance(node, ast.AnnAssign):
        token_list.extend(analyze_ann_assign(node))
    elif isinstance(node, ast.For):
        token_list.extend(analyze_for(node, indent_level))
    elif isinstance(node, ast.AsyncFor):
        token_list.extend(analyze_async_for(node, indent_level))
    elif isinstance(node, ast.While):
        token_list.extend(analyze_while(node, indent_level))
    elif isinstance(node, ast.If):
        token_list.extend(analyze_if(node, indent_level))
    elif isinstance(node, ast.With):
        token_list.extend(analyze_with(node, indent_level))
    elif isinstance(node, ast.AsyncWith):
        token_list.extend(analyze_async_with(node, indent_level))
    elif isinstance(node, ast.Raise):
        token_list.extend(analyze_raise(node))
    elif isinstance(node, ast.Try):
        token_list.extend(analyze_try(node, indent_level))
    elif isinstance(node, ast.Assert):
        token_list.extend(analyze_assert(node))
    elif isinstance(node, ast.Import):
        token_list.extend(analyze_import(node))
    elif isinstance(node, ast.ImportFrom):
        token_list.extend(analyze_import_from(node))
    elif isinstance(node, ast.Global):
        token_list.extend(analyze_global(node))
    elif isinstance(node, ast.Nonlocal):
        token_list.extend(analyze_nonlocal(node))
    elif isinstance(node, ast.Expr):
        token_list.extend(analyze_exp(node))
    elif isinstance(node, ast.Pass):
        token_list.extend(analyze_pass(node))
    elif isinstance(node, ast.Break):
        token_list.extend(analyze_break(node))
    elif isinstance(node, ast.Continue):
        token_list.extend(analyze_break(node))
    return token_list


