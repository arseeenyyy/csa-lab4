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
    EMIT = "emit"
    KEY = "key"
    PRINT_STRING = '."'
    # flow control
    IF = "if"
    ELSE = "else"
    THEN = "then"
    DO = "do"
    LOOP = "loop"
    CALL = "call"
    # system operations
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
    Opcode.PRINT_STRING: 0x33,
    Opcode.IF: 0x40,
    Opcode.ELSE: 0x41,
    Opcode.THEN: 0x42,
    Opcode.DO: 0x43,
    Opcode.LOOP: 0x44,
    Opcode.CALL: 0x45,
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
    0x33: Opcode.PRINT_STRING,
    0x40: Opcode.IF,
    0x41: Opcode.ELSE,
    0x42: Opcode.THEN,
    0x43: Opcode.DO,
    0x44: Opcode.LOOP,
    0x45: Opcode.CALL,
    0xFF: Opcode.HALT
}

arg_ops = {Opcode.LIT, Opcode.CALL, Opcode.PRINT_STRING}

class Instruction: 
    def __init__(self, opcode: Opcode, arg: int = 0): 
        self.opcode = opcode 
        self.arg = arg
    def __str__(self): 
        if self.opcode not in arg_ops: 
            return f"{self.opcode.value}"
        return f"{self.opcode.value} {self.arg}"

def to_bytes(instructions: list[Instruction]) -> bytes:
    binary_bytes = bytearray()
    i = 0
    while i < len(instructions):
        if instructions[i].opcode in arg_ops:
            opcode = opcode_to_binary[instructions[i].opcode]
            arg = instructions[i].arg & 0xFFFFFF  
            word = (opcode << 24) | arg
            binary_bytes.extend(
                ((word >> 24) & 0xFF, (word >> 16) & 0xFF, (word >> 8) & 0xFF, word & 0xFF)
            )
            i += 1
        else:
            
            word = 0
            for j in range(4):
                if i + j < len(instructions) and instructions[i + j].opcode not in arg_ops:
                    opcode = opcode_to_binary[instructions[i + j].opcode]  
                    word |= opcode << (24 - j * 8)
                else:
                    word |= 0x00 << (24 - j * 8)  
            binary_bytes.extend(
                ((word >> 24) & 0xFF, (word >> 16) & 0xFF, (word >> 8) & 0xFF, word & 0xFF)
            )
            i += min(4, len(instructions) - i)

    return bytes(binary_bytes)

def from_bytes(binary: bytes) -> list[Instruction]:
    instructions = []

    for i in range(0, len(binary), 4):
        if i + 3 >= len(binary):
            break
        word = (binary[i] << 24) | (binary[i + 1] << 16) | (binary[i + 2] << 8) | binary[i + 3]
        
        first_opcode = binary_to_opcode.get((word >> 24) & 0xFF, Opcode.NOP)
        if first_opcode in arg_ops:
            arg = word & 0xFFFFFF
            instructions.append(Instruction(first_opcode, arg))
        else:
            for j in range(4):
                opcode_bin = (word >> (24 - j * 8)) & 0xFF
                if opcode_bin == 0x00:  
                    continue
                opcode = binary_to_opcode.get(opcode_bin, Opcode.NOP)
                instructions.append(Instruction(opcode))

    return instructions

def main():
    program = [
        Instruction(Opcode.LIT, 42),    
        Instruction(Opcode.DUP),        
        Instruction(Opcode.DUP),        
        Instruction(Opcode.ADD),        
        Instruction(Opcode.PRINT_INT),  
        Instruction(Opcode.HALT)        
    ]
    binary = to_bytes(program)
    print("Бинарный код (hex):", binary.hex(' '))
    
    decompiled = from_bytes(binary)
    print("Декомпилировано:")
    for instr in decompiled:
        print(f"  {instr}")

if __name__ == "__main__":
    main()