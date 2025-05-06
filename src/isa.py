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
    0x0: Opcode.LIT,    
    0x1: Opcode.DUP, 
    0x2: Opcode.DROP, 
    0x3: Opcode.ADD, 
    0x4: Opcode.SUB, 
    0x5: Opcode.AND, 
    0x6: Opcode.OR, 
    0x7: Opcode.SWAP, 
    0x8: Opcode.INVERT, 
    0x9: Opcode.DIVIDE, 
    0xA: Opcode.HALT
}

class Instruction: 
    def __init__(self, opcode: Opcode, arg: int = 0):
        self.opcode = opcode
        self.arg = arg

    def __str__(self):
        arg_ops = {Opcode.LIT}  
        
        if self.opcode in arg_ops:
            return f"{self.opcode.value} {self.arg}"
        return f"{self.opcode.value}"
    
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

def from_bytes(binary: bytes) -> list[Instruction]:
    instructions = []
    
    for i in range(0, len(binary), 4):
        if i + 3 >= len(binary):
            break
        word = (binary[i] << 24) | (binary[i+1] << 16) | (binary[i+2] << 8) | binary[i+3]
        opcode_bin = (word >> 28) & 0xF
        arg = word & 0x0FFFFFFF
        
        opcode = binary_to_opcode[opcode_bin]

        
        instructions.append(Instruction(opcode, arg))
    
    return instructions

def main(): 
    program = [
        Instruction(Opcode.LIT, 42),
        Instruction(Opcode.DUP),
        Instruction(Opcode.ADD),
        Instruction(Opcode.HALT)
    ]
    binary = to_bytes(program)
    print(binary.hex(' '))
    
    decompiled = from_bytes(binary)
    for instr in decompiled:
        print(f"  {instr}")

if __name__ == "__main__": 
    main()