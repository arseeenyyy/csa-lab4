from enum import Enum
from collections import namedtuple

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
    EMIT = "emit"
    KEY = "key"
    # PRINT_STRING = '."'
    # flow control
    IF = "if"
    ELSE = "else"
    THEN = "then"
    DO = "do"
    LOOP = "loop"
    CALL = "call"
    BEGIN = "begin"
    UNTIL = "until"
    # system operations
    LOAD_ADDR = "load_addr",
    RET = ";"
    HALT = "halt"
    NOP = "nop" # just for padding

    def __str__(self): 
        return str(self.value)

opcode_to_binary = {
    Opcode.LIT: 0x01,
    Opcode.DUP: 0x02,
    Opcode.DROP: 0x03,
    Opcode.SWAP: 0x04,
    Opcode.OVER: 0x05,
    Opcode.ADD: 0x10,
    Opcode.SUB: 0x11,
    Opcode.MUL: 0x12,
    Opcode.DIV: 0x13,
    Opcode.MOD: 0x14,
    Opcode.AND: 0x15,
    Opcode.OR: 0x16,
    Opcode.XOR: 0x17,
    Opcode.EQ: 0x18,
    Opcode.LT: 0x19,
    Opcode.GT: 0x1A,
    Opcode.STORE: 0x20,
    Opcode.FETCH: 0x21,
    Opcode.VARIABLE: 0x22,
    Opcode.PRINT_INT: 0x30,
    Opcode.EMIT: 0x31,
    Opcode.KEY: 0x32,
    # Opcode.PRINT_STRING: 0x33,
    Opcode.IF: 0x40,
    Opcode.ELSE: 0x41,
    Opcode.THEN: 0x42,
    Opcode.DO: 0x43,
    Opcode.LOOP: 0x44,
    Opcode.CALL: 0x45,
    Opcode.BEGIN: 0x46,
    Opcode.UNTIL: 0x47,
    Opcode.LOAD_ADDR: 0x50,
    Opcode.RET: 0xFE,
    Opcode.HALT: 0xFF,
    Opcode.NOP: 0x00  
}
binary_to_opcode = {
    0x00: Opcode.NOP,
    0x01: Opcode.LIT,
    0x02: Opcode.DUP,
    0x03: Opcode.DROP,
    0x04: Opcode.SWAP,
    0x05: Opcode.OVER,
    0x10: Opcode.ADD,
    0x11: Opcode.SUB,
    0x12: Opcode.MUL,
    0x13: Opcode.DIV,
    0x14: Opcode.MOD,
    0x15: Opcode.AND,
    0x16: Opcode.OR,
    0x17: Opcode.XOR,
    0x18: Opcode.EQ,
    0x19: Opcode.LT,
    0x1A: Opcode.GT,
    0x20: Opcode.STORE,
    0x21: Opcode.FETCH,
    0x22: Opcode.VARIABLE,
    0x30: Opcode.PRINT_INT,
    0x31: Opcode.EMIT,
    0x32: Opcode.KEY,
    # 0x33: Opcode.PRINT_STRING,
    0x40: Opcode.IF,
    0x41: Opcode.ELSE,
    0x42: Opcode.THEN,
    0x43: Opcode.DO,
    0x44: Opcode.LOOP,
    0x45: Opcode.CALL,
    0x46: Opcode.BEGIN, 
    0x50: Opcode.LOAD_ADDR,
    0x47: Opcode.UNTIL,
    0xFE: Opcode.RET,
    0xFF: Opcode.HALT
}

arg_ops = {Opcode.LIT, Opcode.CALL, Opcode.LOAD_ADDR} 


class Term(namedtuple("Term", "line pos word")): 
    """
    Описание выражения из исходного текста программы
    """


def to_bytes(code): 
    pass 

def to_hex(code): 
    pass

def from_bytes(binary_code): 
    pass 

def main():
    pass
if __name__ == "__main__": 
    main()