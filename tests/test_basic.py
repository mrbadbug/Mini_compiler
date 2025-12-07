# tests/test_basic.py
import io
import sys
from src.main import compile_and_run

def capture_output(source):
    old = sys.stdout
    try:
        sys.stdout = io.StringIO()
        compile_and_run(source)
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdout = old

def test_example1():
    src = "a = 5 + 3 * 2\nprint(a)\n"
    out = capture_output(src)
    assert out == "11"

def test_example2():
    src = "x = 10\ny = x * 2 + (3 + 1)\nprint(y)\n"
    out = capture_output(src)
    assert out == "24"

if __name__ == "__main__":
    test_example1()
    test_example2()
    print("All tests passed")
