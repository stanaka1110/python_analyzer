import ast

import warnings


from analyzer_context import analyze_op

def analyze_bool_op(node):
    warnings.warn("bool op deprecation", DeprecationWarning)
    assert(isinstance(node, ast.BoolOp))
    token_list = []
    values = node.values
    for idx, v in enumerate(values):

        token_list.extend(analyze_value(v))
        token_list.extend(analyze_op(node.op))
    
    return token_list

def analyze_named_expr(node):
    assert(isinstance(node, ast.NamedExpr))
    token_list = []
    token_list.append("(")
    token_list.extend(analyze_value(node.target))
    token_list.append(":")
    token_list.append("=")
    token_list.extend(analyze_value(node.value))
    token_list.append(")")
    return token_list

def analyze_bin_op(node):
    warnings.warn("bin op deprecation", DeprecationWarning)
    assert(isinstance(node, ast.BinOp))
    child = list(ast.iter_child_nodes(node))
    token_list = []
    if isinstance(child[0], ast.BinOp):
        token_list.extend(analyze_bin_op(child[0]))
    else:
        token_list.extend(analyze_value(node.left))
    token_list.extend(analyze_op(node.op))
    token_list.extend(analyze_value(node.right))
    return token_list

def analyze_unary_op(node):
    assert(isinstance(node, ast.UnaryOp))
    token_list = []
    token_list.extend(analyze_op(node.op))
    token_list.extend(analyze_value(node.operand))
    return token_list

def analyze_lambda(node):
    warnings.warn("lambda deprecation", DeprecationWarning)
    assert(isinstance(node, ast.Lambda))
    token_list = []

    token_list.append("lambda")
    # どの位置にイコールが入るかわからないため放置
    args_list = node.args.args
    defalut_list = node.args.defaults
    if len(args_list) != 0:
        token_list.append(args_list[0].arg)
        for a, d in zip(args_list[1:], defalut_list):
            token_list.append(",")
            token_list.append(a.arg)
            token_list.append("=")
            token_list.extend(analyze_value(d))
            
    token_list.append(":")
    token_list.extend(analyze_expr(node.body))
    return token_list

def analyze_if_exp(node):
    warnings.warn("if exp deprecation", DeprecationWarning)
    assert(isinstance(node, ast.IfExp))
    token_list = []
    test = node.test
    body = node.body
    orelse = node.orelse
    token_list.extend(analyze_name(test))
    token_list.extend(analyze_name(body))
    token_list.extend(analyze_name(orelse))
    return token_list

def analyze_dict(node):
    assert(isinstance(node, ast.Dict))
    token_list = []
    value_list = node.values
    token_list.append("{")
    for idx, key in enumerate(node.keys):
        if idx != 0:
            token_list.append(",")
        if key != None:
            token_list.extend(analyze_value(key))
            token_list.append(":")
            token_list.extend(analyze_value(value_list[idx]))
        elif key == None:
            token_list.append("**")
            token_list.extend(analyze_value(value_list[idx]))

    token_list.append("}")
    return token_list

def analyze_set(node):
    assert(isinstance(node, ast.Set))
    token_list = []
    token_list.append("{")
    for idx, v in enumerate(node.elts):
        if idx != 0:
            token_list.append(",")
        token_list.extend(analyze_value(v))
    token_list.append("}")
    return token_list

def analyze_list_comp(node):
    warnings.warn("list comp deprecation", DeprecationWarning)
    assert(isinstance(node, ast.ListComp))
    token_list = []
    token_list.append("[")
    token_list.extend(analyze_expr(node.elt))
    token_list.extend(analyze_comprehension(node.generators[0]))
    token_list.append("]")
    return token_list

def analyze_set_comp(node):
    warnings.warn("set comp deprecation", DeprecationWarning)
    assert(isinstance(node, ast.SetComp))
    token_list = []
    return token_list

def analyze_dict_comp(node):
    warnings.warn("dict comp deprecation", DeprecationWarning)
    assert(isinstance(node, ast.DictComp))
    token_list = []
    return token_list

def analyze_generator_exp(node):
    warnings.warn("generator exp deprecation", DeprecationWarning)
    assert(isinstance(node, ast.GeneratorExp))
    token_list = []
    return token_list

def analyze_comprehension(node):
    assert(isinstance(node, ast.comprehension))
    token_list = []
    token_list.append("for")
    token_list.extend(analyze_expr(node.target))
    token_list.append("in")
    token_list.extend(analyze_expr(node.iter))
    return token_list

def analyze_await(node):
    warnings.warn("await deprecation", DeprecationWarning)
    assert(isinstance(node, ast.Await))
    token_list = []
    return token_list

def analyze_yield(node):
    warnings.warn("yield deprecation", DeprecationWarning)
    assert(isinstance(node, ast.Yield))
    token_list = []
    return token_list

def analyze_yield_from(node):
    warnings.warn("yield from deprecation", DeprecationWarning)
    assert(isinstance(node, ast.YieldFrom))
    token_list = []
    return token_list

def analyze_compare(node):
    warnings.warn("compare deprecation", DeprecationWarning)
    assert(isinstance(node, ast.Compare))
    token_list = []
    return token_list

def analyze_call(node):
    warnings.warn("call deprecation", DeprecationWarning)
    assert(isinstance(node, ast.Call))
    token_list = []

    token_list.append(node.func.id)
    token_list.append("(")

    arg_list = list(node.args)
    print(arg_list)

    tmp_list = []
    for idx, a in enumerate(arg_list):
        if idx != 0:
            token_list.append(",")
        
        token_list.extend(analyze_value(a))
        
    
    keyword_list = node.keywords
    if len(keyword_list) != 0:
        token_list.append(",")
    else:
        token_list.extend(tmp_list)
    for idx, k in enumerate(keyword_list):

        if idx != 0:
            token_list.append(",")
        
        if k.arg != None:
            token_list.append(k.arg)
            token_list.append("=")
            if isinstance(k.value, ast.Name):
                token_list.extend(analyze_name(k.value))
            elif isinstance(k.value, ast.Constant):
                token_list.extend(analyze_constant(k.value))
        else:
            token_list.extend(tmp_list)
            token_list.append(",")
            token_list.append("**")
            token_list.append(k.value.id)
    
    token_list.append(")")

    return token_list

def analyze_formatted_value(node):
    warnings.warn("formatted value deprecation", DeprecationWarning)
    assert(isinstance(node, ast.FormattedValue))
    token_list = []
    return token_list

def analyze_join_str(node):
    warnings.warn("join str deprecation", DeprecationWarning)
    assert(isinstance(node, ast.JoinedStr))
    token_list = []
    return token_list

def analyze_constant(node):
    #strの処理部分，数値or文字列の処理を実装
    assert(isinstance(node, ast.Constant))
    if type(node.value) == int:
        token_list = [str(node.value)]
    elif type(node.value) == str:
        token_list = ['\'', str(node.value), '\'']
    return token_list

def analyze_attribute(node):
    assert(isinstance(node, ast.Attribute))
    token_list = []
    if isinstance(node.value, ast.Name):
        token_list.extend(analyze_name(node.value))
    elif isinstance(node.value, ast.Attribute):
        token_list.extend(analyze_attribute(node.value))
    token_list.append(".")
    token_list.append(node.attr)
    return token_list

def analyze_subscript(node):
    assert(isinstance(node, ast.Subscript))
    token_list = []
    token_list.extend(analyze_name(node.value))
    token_list.append("[")
    if isinstance(node.slice, ast.Index):
        slice_list = list(ast.iter_child_nodes(node.slice))
        for idx, s in enumerate(slice_list):
            if idx != 0:
                token_list.append(",")
            
            if isinstance(s, ast.Constant):
                token_list.extend(analyze_constant(s))
            elif isinstance(s, ast.Tuple):
                token_list.extend(analyze_tuple(s))
            elif isinstance(s, ast.Slice):
                token_list.extend(analyze_slice(s))
    elif isinstance(node.slice, ast.Slice):
        token_list.extend(analyze_slice(node.slice))
    token_list.append("]")
    return token_list

def analyze_starred(node):
    warnings.warn("starred deprecation", DeprecationWarning)
    assert(isinstance(node, ast.Starred))
    token_list = []
    token_list.append("*")
    token_list.extend(analyze_value(node.value))
    return token_list

def analyze_name(node):
    assert(isinstance(node, ast.Name))
    token_list = []
    token_list.append(node.id)
    return token_list

def analyze_list(node):
    assert(isinstance(node, ast.List))

    token_list = []
    token_list.append("[")
    elts_list = node.elts
    for idx, e in enumerate(elts_list):
        if idx != 0:
            token_list.append(",")
        if isinstance(e, ast.Name):
            token_list.extend(analyze_name(e))
        elif isinstance(e, ast.Constant):
            token_list.extend(analyze_constant(e))
    
    token_list.append("]")
    return token_list

def analyze_tuple(node):
    assert(isinstance(node, ast.Tuple))
    token_list = []
    elts_list = node.elts
    for idx, e in enumerate(elts_list):
        if idx != 0:
            token_list.append(",")
        if isinstance(e, ast.Constant):
            token_list.extend(analyze_constant(e))
        elif isinstance(e, ast.Name):
            token_list.extend(analyze_name(e))
        
    
    return token_list

def analyze_slice(node):
    assert(isinstance(node, ast.Slice))
    token_list = []
    l = node.lower
    u = node.upper
    if isinstance(l, ast.Name):
        token_list.extend(analyze_name(l))
    elif isinstance(l, ast.Constant):
        token_list.extend(analyze_constant(l))
    token_list.append(":")
    if isinstance(u, ast.Name):
        token_list.extend(analyze_name(u))
    
    elif isinstance(u, ast.Constant):
        token_list.extend(analyze_constant(u))
    return token_list


def analyze_value(node):
    token_list = []
    if isinstance(node, ast.Attribute):
        token_list.extend(analyze_attribute(node))
    elif isinstance(node, ast.Constant):
        token_list.extend(analyze_constant(node))
    elif isinstance(node, ast.Name):
        token_list.extend(analyze_name(node))
    elif isinstance(node, ast.Tuple):
        token_list.extend(analyze_tuple(node))
    elif isinstance(node, ast.List):
        token_list.extend(analyze_list(node))
    elif isinstance(node, ast.Subscript):
        token_list.extend(analyze_subscript(node))
    elif isinstance(node, ast.Dict):
        token_list.extend(analyze_dict(node))
    elif isinstance(node, ast.Set):
        token_list.extend(analyze_set(node))
    else:
        print("error")
        exit()
    
    return token_list

def analyze_expr(node):
    token_list = []

    if isinstance(node, ast.BoolOp):
        token_list.extend(analyze_bool_op(node))
    elif isinstance(node, ast.NamedExpr):
        token_list.extend(analyze_named_expr(node))
    elif isinstance(node, ast.BinOp):
        token_list.extend(analyze_bin_op(node))        
    elif isinstance(node, ast.UnaryOp):
        token_list.extend(analyze_unary_op(node))
    elif isinstance(node, ast.Lambda):
        token_list.extend(analyze_lambda(node))
    elif isinstance(node, ast.IfExp):
        token_list.extend(analyze_if_exp(node))
    elif isinstance(node, ast.Dict):
        token_list.extend(analyze_dict(node))
    elif isinstance(node, ast.Set):
        token_list.extend(analyze_set(node))
    elif isinstance(node, ast.ListComp):
        token_list.extend(analyze_list_comp(node))
    elif isinstance(node, ast.SetComp):
        token_list.extend(analyze_set_comp(node))
    elif isinstance(node, ast.DictComp):
        token_list.extend(analyze_dict_comp(node))
    elif isinstance(node, ast.GeneratorExp):
        token_list.extend(analyze_generator_exp(node))
    elif isinstance(node, ast.Await):
        token_list.extend(analyze_await(node))
    elif isinstance(node, ast.Yield):
        token_list.extend(analyze_yield(node))
    elif isinstance(node, ast.YieldFrom):
        token_list.extend(analyze_yield_from(node))
    elif isinstance(node, ast.Compare):
        token_list.extend(analyze_compare(node))
    elif isinstance(node, ast.Call):
        token_list.extend(analyze_call(node))
    elif isinstance(node, ast.FormattedValue):
        token_list.extend(analyze_formatted_value(node))
    elif isinstance(node, ast.JoinedStr):
        token_list.extend(analyze_formatted_value(node))
    elif isinstance(node, ast.Constant):
        token_list.extend(analyze_constant(node))
    elif isinstance(node, ast.Attribute):
        token_list.extend(analyze_attribute(node))
    elif isinstance(node, ast.Subscript):
        token_list.extend(analyze_subscript(node))
    elif isinstance(node, ast.Starred):
        token_list.extend(analyze_starred(node))
    elif isinstance(node, ast.Name):
        token_list.extend(analyze_name(node))
    elif isinstance(node, ast.List):
        token_list.extend(analyze_list(node))
    elif isinstance(node, ast.Tuple):
        token_list.extend(analyze_tuple(node))
    elif isinstance(node, ast.Slice):
        token_list.extend(analyze_slice(node))
    return token_list