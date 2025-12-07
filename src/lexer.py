# src/lexer.py
import re
from typing import Iterator, Tuple

TOKEN_SPEC = [
    ("NUMBER",  r"\d+"),
    ("IDENT",   r"[A-Za-z_]\w*"),
    ("PLUS",    r"\+"),
    ("MINUS",   r"-"),
    ("STAR",    r"\*"),
    ("SLASH",   r"/"),
    ("EQUAL",   r"="),
    ("LPAREN",  r"\("),
    ("RPAREN",  r"\)"),
    ("SEMICOLON", r";"),
    ("NEWLINE", r"\n"),
    ("SKIP",    r"[ \t\r]+"),
    ("COMMENT", r"#.*"),
]

_token_re = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC))

def tokenize(text: str) -> Iterator[Tuple[str,str]]:
    pos = 0
    while pos < len(text):
        m = _token_re.match(text, pos)
        if not m:
            raise SyntaxError(f"Unexpected character: {text[pos]!r} at position {pos}")
        kind = m.lastgroup
        value = m.group()
        pos = m.end()
        if kind == "SKIP" or kind == "COMMENT":
            continue
        if kind == "NEWLINE":
            yield ("NEWLINE", "\\n")
            continue
        yield (kind, value)
    yield ("EOF", "")
