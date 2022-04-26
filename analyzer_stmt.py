import ast
import token
import warnings
from analyzer_exp import analyze_call, analyze_subscript
from analyzer_context import analyze_attribute, analyze_constant, analyze_name, analyze_op, analyze_tuple

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

    warnings.warn("return deprecation", DeprecationWarning)
    assert(isinstance(node, ast.Return))
    token_list = []

    token_list.append("return")

    val = node.value.value
    token_list.append(str(val))

    return token_list

def analyze_delete(node):
    warnings.warn("delete deprecation", DeprecationWarning)
    assert(isinstance(node, ast.Delete))
    token_list = []

    token_list.append("del")

    target_list = list(node.targets)

    # 削除するターゲットがlist，nameの可能性
    for idx, t in enumerate(target_list):
        if idx != 0:
            token_list.append(",")
        token_list.extend(analyze_name(t))
    return token_list

def analyze_assign(node):
    assert(isinstance(node, ast.Assign))

    token_list = []
    target_list = list(node.targets)

    if isinstance(target_list[0], ast.Name):
        for idx, t in enumerate(target_list):
            if idx != 0:
                token_list.append("=")
            token_list.extend(analyze_name(t))
    elif isinstance(target_list[0], ast.Tuple):
        token_list.extend(analyze_tuple(target_list[0]))
    elif isinstance(target_list[0], ast.Subscript):
        token_list.extend(analyze_subscript(target_list[0]))
    token_list.append("=")
    value = node.value
    if isinstance(value, ast.Constant):
        token_list.append(str(value.value))
    elif isinstance(value, ast.Name):
        token_list.extend(analyze_name(value))
    elif isinstance(value, ast.Subscript):
        token_list.extend(analyze_subscript(value))
    
    return token_list

def analyze_annasign(node):
    assert(isinstance(node, ast.AnnAssign))
    token_list = []

    target = node.target
    if isinstance(target, ast.Name):
        token_list.extend(analyze_name(target))
    elif isinstance(target, ast.Attribute):
        token_list.extend(analyze_attribute(target))
    token_list.append(":")
    token_list.extend(analyze_name(node.annotation))
    return token_list

def analyze_augassign(node):
    assert(isinstance(node, ast.AugAssign))
    token_list = []
    if isinstance(node.target, ast.Name):
        token_list.extend(analyze_name(node.target))
    
    token_list.extend(analyze_op(node.op))
    token_list.append("=")

    if isinstance(node.value, ast.Constant):
        token_list.extend(analyze_constant(node.value))

    return token_list

def analyze_for(node, indent_level):
    warnings.warn("for deprecation", DeprecationWarning)
    assert(isinstance(node, ast.For))
    token_list = []
    token_list.append("for")
    target = node.target
    if isinstance(target, ast.Name):
        token_list.extend(analyze_name(target))
    elif isinstance(target, ast.Tuple):
        child = list(target.elts)
        token_list.extend(analyze_tuple(child))
    elif isinstance(target, ast.List):
        token_list.append("[")

        child = list(target.elts)
        for c in child[1:]:
            token_list.append(",")
            token_list.append(c.id)
        token_list.append("]")

    token_list.append("in")
    if isinstance(node.iter, ast.Call):
        token_list.extend(analyze_call(node.iter))
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
    return token_list

def analyze_import(node):
    warnings.warn("import deprecation", DeprecationWarning)
    assert(isinstance(node, ast.Import))
    token_list = []
    return token_list

def analyze_import_from(node):
    warnings.warn("import from deprecation", DeprecationWarning)
    assert(isinstance(node, ast.ImportFrom))
    token_list = []
    return token_list

def analyze_global(node):
    warnings.warn("global deprecation", DeprecationWarning)
    assert(isinstance(node, ast.Global))
    token_list = []
    return token_list

def analyze_nonlocal(node):
    warnings.warn("nonlocal deprecation", DeprecationWarning)
    assert(isinstance(node, ast.Nonlocal))
    token_list = []
    return token_list

def analyze_expr(node):
    warnings.wanr("expr deprecation", DeprecationWarning)
    assert(isinstance(node, ast.Expr))
    token_list = []
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



