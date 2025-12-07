# src/main.py
import sys
from lexer import tokenize
from parser import Parser
from codegen import CodeGen
from vm import VM

def compile_and_run(source: str):
    tokens = list(tokenize(source))
    parser = Parser(tokens)
    stmts = parser.parse()
    cg = CodeGen()
    bytecode = cg.compile_program(stmts)
    vm = VM(bytecode)
    vm.run()

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m src.main <source-file>")
        print("Or run with no args to execute a demo.")
        demo = """
# demo
a = 5 + 3 * 2
b = (a - 4) / 2
print(a)
print(b)
"""
        compile_and_run(demo)
    else:
        fname = sys.argv[1]
        with open(fname, "r") as f:
            src = f.read()
        compile_and_run(src)

if __name__ == "__main__":
    main()
