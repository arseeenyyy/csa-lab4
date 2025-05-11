from enum import Enum

class Opcode(str, Enum):
    # base operations
    LIT = "lit"
    DUP = "dup" 
    DROP = "drop" 
    SWAP = "swap"
    OVER = "over" 
    # arthimetic and logic operations
    ADD = "+"
    SUB = "-" 
    MUL = "*" 
    DIV = "/" 
    MOD = "mod" 
    AND = "and" 
    OR = "or"
    XOR = "xor" 
    EQ = "="
    LT = "<" 
    GT = ">" 
    # memory operations
    STORE = "!" 
    FETCH = "@"
    VARIABLE = "variable"
    # input output
    PRINT_INT = "."
    PRINT_CHAR = "emit"
    KEY = "key"
    PRINT_STRING = '."'
    # flow control
    IF = "if"
    ELSE = "else"
    THEN = "then"
    DO = "do"
    LOOP = "loop"
    # system operations
    HALT = "halt"
    NOP = "nop" # just for padding

    def __str__(self): 
        return str(self.value)
    