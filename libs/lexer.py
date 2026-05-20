from dataclasses import dataclass
from enum import Enum, auto

# Valid Tokens
class TokenKind(Enum):
    IDENTIFIER  = auto()
    INT_LITERAL = auto()

    LET = auto()        # let
    RETURN = auto()     # return

    DBL_COLON = auto()  # ::
    COLON = auto()      # :
    ARROW = auto()      # ->
    EQUAL = auto()      # =

    PLUS = auto()       # +
    MINUS = auto()      # -
    STAR  = auto()      # *
    SLASH = auto()      # /
    LT = auto()         # <
    GT = auto()         # >
    EQEQ = auto()       # ==

    L_PAREN = auto()    # (
    R_PAREN = auto()    # )
    L_BRACE = auto()    # {
    R_BRACE = auto()    # }

    NEWLINE = auto()    # \n
    EOF = auto()

# Valid Keywords
KEYWORDS = {
    "let":    TokenKind.LET,
    "return": TokenKind.RETURN,
}

# Completed Tokens
@dataclass
class Token:
    kind:       TokenKind
    lexeme:     str     # our program*
    line:       int
    column:     int


# Will take in/tokenize our "program"/lexeme
class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.len = len(source)
        self.pos = 0
        self.line = 1
        self.col = 1

    # Holds our array of Tokens to be accessed from main.py/elsewhere
    def tokens(self):
        toks = []
        while True:
            tok = self._next_token()
            toks.append(tok)
            if tok.kind == TokenKind.EOF:
                break
        return toks

    # If past or at end return '\0', otherwise return the char at self.source[self.pos]
    def _peek(self) -> str:
        if self.pos >= self.len:
            return '\0'
        return self.source[self.pos]

    # Check to see if we can advance or go to NEWLINE
    def _advance(self) -> str:
        ch = self._peek()
        self.pos += 1

        # If NEWLINE, advance line, and return col to 1 (beginning of line)
        if ch == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
            
        # ch contains the return statement from _peek() (self.source[self.pos])
        return ch
        
    def _match(self, expected) -> bool:
        if self._peek() == expected:
            self._advance()
            return True
        return False


    # Token Definer/Eater
    # Should cover the basis for all possible defined Tokens above to return a completed Token
    def _next_token(self) -> Token:
        while True:
            ch = self._peek()

            # EOF
            if ch == '\0':
                return Token(TokenKind.EOF, "", self.line, self.col)
            
            # Newline is slightly different 
            if ch == '\n':
                self._advance()
                return Token(TokenKind.NEWLINE, "\\n", self.line - 1, self.col)
            
            # Skip spaces/tabs
            if ch in (' ', '\t', '\r'):
                self._advance()
                continue

            # Comment detection? --> Possible add later off of the slashes



            # Identifiers and Keywords
            if ch.isalpha() or ch == '_':
                return self._identifier_or_keyword()

            # Numbers (only decimal ints)
            if ch.isdigit():
                return self._int_literal()

            # Operators and Symbols 
            return self._symbol_or_operator()
        
    
    # Returns IDENTIFIER/KEYWORD Token
    def _identifier_or_keyword(self) -> Token:
        start_pos = self.pos
        start_col = self.col
        start_line = self.line

        # While our current char is alphanumeric or _ advance, otherwise that means we have an IDENTIFIER 
        # (all other cases are covered)
        while self._peek().isalnum() or self._peek == '_':
            self._advance()

        # Our program is now our original starting position to our current position
        lexeme = self.source[start_pos:self.pos]
        kind = KEYWORDS.get(lexeme, TokenKind.IDENTIFIER)
        return Token(kind=kind, lexeme=lexeme, line=start_line, column=start_col)


    # Returns INT_LITERAL Token
    def _int_literal(self) -> Token:
        start_pos = self.pos
        start_col = self.col
        start_line = self.line

        while self._peek().isdigit():
            self._advance()
        
        lexeme = self.source[start_pos:self.pos]
        return Token(kind=TokenKind.INT_LITERAL, lexeme=lexeme, line=start_line, column=start_col)

    # Largest part of the lexer (Basically the entire thing)
    def _symbol_or_operator(self) -> Token:
        ch = self._advance()
        line = self.line
        col = self.col - 1

        # Multi-char Tokens
        if ch == ':' and self._peek() == ':':
            self._advance()
            return Token(TokenKind.DBL_COLON, "::", line, col)
        if ch == '-' and self._peek() == '>':
            self._advance()
            return Token(TokenKind.ARROW, "->", line, col)
        if ch == '=' and self._peek() == '=':
            self._advance()
            return Token(TokenKind.EQEQ, "==", line, col)
        
        # Single-char Tokens
        if ch == ':':
            return Token(TokenKind.COLON, ":", line, col)
        if ch == '=':
            return Token(TokenKind.EQUAL, "=", line, col)
        if ch == '+':
            return Token(TokenKind.PLUS, "+", line, col)
        if ch == '-':
            return Token(TokenKind.MINUS, "-", line, col)
        if ch == '*':
            return Token(TokenKind.STAR, "*", line, col)
        if ch == '/':
            return Token(TokenKind.SLASH, "/", line, col)
        if ch == '<':
            return Token(TokenKind.LT, "<", line, col)
        if ch == '>':
            return Token(TokenKind.GT, ">", line, col)
        if ch == '(':
            return Token(TokenKind.L_PAREN, "(", line, col)
        if ch == ')':
            return Token(TokenKind.R_PAREN, ")", line, col)
        if ch == '{':
            return Token(TokenKind.L_BRACE, "{", line, col)
        if ch == '}': 
            return Token(TokenKind.R_BRACE, "}", line, col)
        
        # Unknown Token/Throw error because we haven't defined this char
        raise SyntaxError(f"Unexpected char '{ch}' at {line}:{col}")