# src/codegen.py
from ast_n import Number, Var, BinOp, Assign, Print
from typing import List, Tuple

# Instruction tuples: ("PUSH", value), ("LOAD", name), ("STORE", name),
# ("ADD",), ("SUB",), ("MUL",), ("DIV",), ("PRINT",)

class CodeGen:
    def __init__(self):
        self.code: List[Tuple] = []

    def generate(self, node):
        if isinstance(node, Number):
            self.code.append(("PUSH", node.value))

        elif isinstance(node, Var):
            self.code.append(("LOAD", node.name))

        elif isinstance(node, BinOp):
            self.generate(node.left)
            self.generate(node.right)
            op_map = {'+': "ADD", '-': "SUB", '*': "MUL", '/': "DIV"}
            self.code.append((op_map[node.op],))

        elif isinstance(node, Assign):
            self.generate(node.expr)
            self.code.append(("STORE", node.name))

        elif isinstance(node, Print):
            self.generate(node.expr)
            self.code.append(("PRINT",))

        else:
            raise TypeError(f"Unknown AST node type: {type(node)}")

        return self.code

    def compile_program(self, stmts):
        self.code = []
        for s in stmts:
            self.generate(s)
        return self.code
