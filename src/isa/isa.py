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
    Opcode.LIT: 0x0,
    Opcode.DUP: 0x1, 
    Opcode.DROP: 0x2,
    Opcode.ADD: 0x3, 
    Opcode.SUB: 0x4, 
    Opcode.AND: 0x5, 
    Opcode.OR: 0x6,
    Opcode.SWAP: 0x7, 
    Opcode.INVERT: 0x8, 
    Opcode.DIVIDE: 0x9, 
    Opcode.HALT: 0xA
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

class Instruction: 
    def __init__(self, opcode: Opcode, arg: int): 
        self.opcode: Opcode = opcode 
        self.arg: int = arg

    def __str__(self): 
        return f"({self.opcode} {self.arg})" 

def to_bytes(instructions: list[Instruction]) -> bytes: 
    binary_bytes = bytearray()
    for instr in instructions:
        opcode_bin = opcode_to_binary[instr.opcode] << 28

        arg = instr.arg

        binary_instr = opcode_bin | (arg & 0x0FFFFFFF)

        binary_bytes.extend(
            ((binary_instr >> 24) & 0xFF, (binary_instr >> 16) & 0xFF, (binary_instr >> 8) & 0xFF, binary_instr & 0xFF)
        )

    return bytes(binary_bytes)


# def main(): 
#     program = [
#         Instruction(Opcode.LIT, 42),
#         Instruction(Opcode.DUP, 0),
#         Instruction(Opcode.ADD, 0),
#         Instruction(Opcode.HALT, 0)
#     ]
#     binary = to_bytes(program)
#     print(binary.hex(' '))


# if __name__ == "__main__": 
#     main()