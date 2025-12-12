from typing import List, Tuple

class VM:
    def __init__(self, code: List[Tuple]):
        self.code = code
        self.stack = []
        self.vars = {}

    def run(self):
        for instr in self.code:
            op = instr[0]
            if op == "PUSH":
                self.stack.append(instr[1])

            elif op == "LOAD":
                name = instr[1]
                if name not in self.vars:
                    raise NameError(f"Undefined variable '{name}'")
                self.stack.append(self.vars[name])

            elif op == "STORE":
                name = instr[1]
                if not self.stack:
                    raise RuntimeError("STORE with empty stack")
                val = self.stack.pop()
                self.vars[name] = val

            elif op == "ADD":
                b = self.stack.pop(); a = self.stack.pop()
                self.stack.append(a + b)

            elif op == "SUB":
                b = self.stack.pop(); a = self.stack.pop()
                self.stack.append(a - b)

            elif op == "MUL":
                b = self.stack.pop(); a = self.stack.pop()
                self.stack.append(a * b)

            elif op == "DIV":
                b = self.stack.pop(); a = self.stack.pop()
                if b == 0:
                    raise ZeroDivisionError("Division by zero")
                self.stack.append(a // b)

            elif op == "PRINT":
                if not self.stack:
                    raise RuntimeError("PRINT with empty stack")
                val = self.stack.pop()
                print(val)

            else:
                raise RuntimeError(f"Unknown instruction: {instr}")
