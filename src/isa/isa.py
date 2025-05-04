from enum import Enum

class Opcode(str, Enum):
    LIT = "lit"
    DUP = "dup"
    DROP = "drop"
    ADD = "+"
    SUB = "-"
    AND = "and"
    OR = "or"
    SWAP = "swap"
    INVERT = "invert"
    DIVIDE = "/"
    HALT = "halt"

    def __str__(self): 
        return str(self.value)
    
opcode_to_binary = {
    Opcode.DUP: 0x0, 
    Opcode.DROP: 0x1,
    Opcode.ADD: 0x2, 
    Opcode.SUB: 0x3, 
    Opcode.AND: 0x4, 
    Opcode.OR: 0x5,
    Opcode.SWAP: 0x6, 
    Opcode.INVERT: 0x7, 
    Opcode.DIVIDE: 0x8, 
    Opcode.HALT: 0x9
}

binary_to_opcode = {
    0x0: Opcode.DUP, 
    0x1: Opcode.DROP, 
    0x2: Opcode.ADD, 
    0x3: Opcode.SUB, 
    0x4: Opcode.AND, 
    0x5: Opcode.OR, 
    0x6: Opcode.SWAP, 
    0x7: Opcode.INVERT, 
    0x8: Opcode.DIVIDE, 
    0x9: Opcode.HALT
}