from enum import Enum
from typing import Union

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
    LOAD_MEM = "load_mem",
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
    Opcode.LOAD_MEM: 0x50,
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
    0x50: Opcode.LOAD_MEM,
    0x47: Opcode.UNTIL,
    0xFE: Opcode.RET,
    0xFF: Opcode.HALT
}

arg_ops = {Opcode.LIT, Opcode.CALL, Opcode.LOAD_MEM} 


class Instruction: 
    def __init__(self, opcode: Opcode, arg: Union[int, str] = None): 
        self.opcode = opcode 
        self.arg = arg
    def __str__(self): 
        if self.arg is None: 
            return f"{self.opcode.value}"
        return f"{self.opcode.value} {self.arg}"

def to_bytes(instructions: list[Instruction]) -> bytes: 
    binary = bytearray()
    for instr in instructions: 
        opcode_byte = opcode_to_binary[instr.opcode] 

        if instr.opcode in arg_ops: 
            arg = instr.arg
            binary.extend([
                opcode_byte, 
                (arg >> 16) & 0xFF, 
                (arg >> 8) & 0xFF, 
                arg & 0xFF
            ])
        else: 
            binary.append(opcode_byte)
    return bytes(binary)

def from_bytes(binary: bytes) -> list[Instruction]: 
    instructions = []
    i = 0
    while i < len(binary): 
        opcode_byte = binary[i]
        opcode = binary_to_opcode.get(opcode_byte) 

        if opcode in arg_ops: 
            if i + 3 >= len(binary): 
                break
            arg = (binary[i + 1] << 16) | (binary[i + 2] << 8) | binary[i + 3]
            instructions.append(Instruction(opcode, arg))
            i += 4
        else: 
            instructions.append(Instruction(opcode))
            i += 1
    return instructions

def main():
    instructions = [Instruction(Opcode.DUP), Instruction(Opcode.LIT, 42), Instruction(Opcode.DUP), Instruction(Opcode.DUP)]
    byt = to_bytes(instructions)
    instr2 = from_bytes(byt) 
    for i in range(len(instr2)): 
        if (instr2[i].opcode in arg_ops): 
            print(f"{instr2[i].opcode} {instr2[i].arg}")
        else: print(instr2[i].opcode)
if __name__ == "__main__": 
    main()