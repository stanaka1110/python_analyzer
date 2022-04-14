import ast


import ast

def analyze_return(node):
    token_list = []

    token_list.append("return")

    val = node.value.value
    token_list.append(str(val))

    return token_list