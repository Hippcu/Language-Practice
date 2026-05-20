# Building Expr into Stmts into Funcs 
# Yet to be implemented/used for anything, no parser yet

from dataclasses import dataclass
from typing import List

# Types
@dataclass
class TypeName:
    name: str   # ex. "int"


# Expressions 
class Expr:
    pass

@dataclass
class IntLiteral(Expr):
    value: int

@dataclass
class VarRef(Expr):
    name: str

@dataclass
class Operator(Expr):
    op: str     # ex. '+', '-', '=', etc.
    left: Expr
    right: Expr

@dataclass
class CallExpr(Expr):
    callee: str
    args: List[Expr]


# Statements 
class Stmt:
    pass

# Let (name, of type, with value) -- Essentially what a variable is
class LetStmt(Stmt):
    name: str
    type_name: TypeName
    value: Expr


# Functions/Methods
@dataclass
class Param:
    name: str
    type_name: TypeName

@dataclass
class FuncDecl:
    name: str
    params: List[Param]
    return_type: TypeName
    body: List[Stmt]


# Full Program assembled from everything prior
@dataclass
class Program:
    functions: List[FuncDecl]