# src/ast.py
from dataclasses import dataclass

@dataclass
class Number:
    value: int

@dataclass
class Var:
    name: str

@dataclass
class BinOp:
    left: object
    op: str   # one of '+', '-', '*', '/'
    right: object

@dataclass
class Assign:
    name: str
    expr: object

@dataclass
class Print:
    expr: object
