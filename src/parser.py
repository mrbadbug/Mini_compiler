from typing import List, Tuple
from ast_n import Number, Var, BinOp, Assign, Print

class Parser:
    def __init__(self, tokens: List[Tuple[str,str]]):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ("EOF","")

    def eat(self, expected_kind=None):
        tok = self.peek()
        if expected_kind and tok[0] != expected_kind:
            raise SyntaxError(f"Expected {expected_kind} but got {tok}")
        self.pos += 1
        return tok

    def parse(self):
        stmts = []
        while True:
            tok = self.peek()
            if tok[0] == "EOF":
                break
            if tok[0] == "NEWLINE":
                self.eat("NEWLINE")
                continue
            stmts.append(self.parse_statement())

            if self.peek()[0] == "NEWLINE":
                self.eat("NEWLINE")
            elif self.peek()[0] == "SEMICOLON":
                self.eat("SEMICOLON")
        return stmts

    def parse_statement(self):
        tok = self.peek()
        if tok[0] == "IDENT" and tok[1] != "print":
            name = self.eat("IDENT")[1]
            self.eat("EQUAL")
            expr = self.parse_expr()
            return Assign(name, expr)
        elif tok[0] == "IDENT" and tok[1] == "print":
            self.eat("IDENT") 
            self.eat("LPAREN")
            expr = self.parse_expr()
            self.eat("RPAREN")
            return Print(expr)
        else:
            raise SyntaxError(f"Unknown statement starting with {tok}")

    def parse_expr(self):
        node = self.parse_term()
        while self.peek()[0] in ("PLUS", "MINUS"):
            op_tok = self.eat()
            op = '+' if op_tok[0] == "PLUS" else '-'
            right = self.parse_term()
            node = BinOp(node, op, right)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.peek()[0] in ("STAR", "SLASH"):
            op_tok = self.eat()
            op = '*' if op_tok[0] == "STAR" else '/'
            right = self.parse_factor()
            node = BinOp(node, op, right)
        return node

    def parse_factor(self):
        tok = self.peek()
        if tok[0] == "NUMBER":
            val = int(self.eat("NUMBER")[1])
            return Number(val)
        if tok[0] == "IDENT":
            return Var(self.eat("IDENT")[1])
        if tok[0] == "LPAREN":
            self.eat("LPAREN")
            node = self.parse_expr()
            self.eat("RPAREN")
            return node
        if tok[0] == "MINUS":
            self.eat("MINUS")
            node = self.parse_factor()

            return BinOp(Number(0), '-', node)
        raise SyntaxError(f"Unexpected token in factor: {tok}")
