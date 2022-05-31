import ast
from re import I
import warnings

from analyzer_context import  analyze_alias, analyze_op
from analyzer_exp import analyze_call, analyze_value, analyze_expr
def analyze_function_def(node, indent_level=1):
    warnings.warn("function_def deprecation", DeprecationWarning)
    assert(isinstance(node, ast.FunctionDef))
    token_list = []
    token_list.append("def")
    token_list.append(node.name)

    token_list.append("(")
    args_list = node.args.args
    if len(args_list) != 0:
        token_list.append(args_list[0].arg)
        for a in args_list[1:]:
            token_list.append(",")
            token_list.append(a.arg)
    token_list.append(")")

    token_list.append(":")

    body_list = list(node.body)
    for b in body_list:
        token_list.append("\n")
        for _ in range(indent_level):
            token_list.append("\t")
        
        if isinstance(b, ast.For):
            token_list.extend(analyze_for(b, indent_level+1))

        if isinstance(b, ast.Return):
            token_list.extend(analyze_return(b))
    
    return token_list

def analyze_async_function_def(node, indent_level=1):
    warnings.warn("async_function_def deprecation", DeprecationWarning)
    assert(isinstance(node, ast.AsyncFunctionDef))
    token_list = []
    return token_list

def analyze_class_def(node, indent_level=1):
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
    for _ in range(indent_level):
        token_list.append("\t")

    body_list = list(node.body)
    for body in body_list:
        if isinstance(body, ast.FunctionDef):
            token_list.extend(analyze_function_def(body, indent_level=indent_level+1))

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

    # 削除するターゲットがlist，nameの可能性
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
    warnings.warn("for deprecation", DeprecationWarning)
    assert(isinstance(node, ast.For))
    token_list = []
    token_list.append("for")
    token_list.extend(analyze_expr(node.target))
    token_list.append("in")
    token_list.extend(analyze_expr(node.iter))
    for b in node.body:
        token_list.extend(analyze_expr(b))
    
    return token_list

def analyze_async_for(node, indent_level):
    warnings.warn("for_async deprecation", DeprecationWarning)
    assert(isinstance(node, ast.AsyncFor))
    token_list = []
    return token_list

def analyze_while(node, indent_level):
    warnings.warn("while deprecation", DeprecationWarning)
    assert(isinstance(node, ast.While))
    token_list = []
    return token_list

def analyze_if(node, indent_level):
    warnings.warn("if deprecation", DeprecationWarning)
    assert(isinstance(node, ast.If))

    token_list = []
    return token_list

def analyze_with(node, indent_level):
    warnings.warn("with deprecation", DeprecationWarning)
    assert(isinstance(node, ast.With))

    token_list = []
    return token_list

def analyze_async_with(node, indent_level):
    warnings.warn("async with deprecation", DeprecationWarning)
    assert(isinstance(node, ast.AsyncWith))

    token_list = []
    return token_list

def analyze_match(node):
    warnings.warn("match FutureWarning", FutureWarning)
    return []

def analyze_raise(node):
    warnings.warn("'raise deprecation", DeprecationWarning)
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
    return token_list

def analyze_assert(node):
    warnings.warn("assert deprecation", DeprecationWarning)
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
    
    return token_list


