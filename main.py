from lexer import Lexer, TokenKind

program : str = """\
main :: () -> int {
    let x: int = 60
    return x
}
"""

def main(prgm):
    lexer = Lexer(prgm)
    for tok in lexer.tokens():
        print(f"{tok.line}:{tok.column}  {tok.kind.name:12}  {tok.lexeme!r}")


if __name__ == '__main__':
    main(prgm=program)