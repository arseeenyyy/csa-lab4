import sys
from typing import Optional, List 
from isa import Opcode, Instruction, from_bytes, to_bytes

def symbol_2_instruction(symbol: str) -> Optional[List[Instruction]]: 
    return {
        "+": [Instruction(Opcode.ADD)], 
        "-": [Instruction(Opcode.SUB)], 
        "and": [Instruction(Opcode.AND)], 
        "or": [Instruction(Opcode.OR)], 
        "swap": [Instruction(Opcode.SWAP)], 
        "dup": [Instruction(Opcode.DUP)], 
        "drop": [Instruction(Opcode.DROP)], 
        "/": [Instruction(Opcode.DIVIDE)], 
        "invert": [Instruction(Opcode.INVERT)], 
        "halt": [Instruction(Opcode.HALT)]
    }.get(symbol)

def remove_comments(text: str) -> str:
    result = []
    i = 0
    n = len(text)
    
    while i < n:
        if text[i] == '(':
            while i < n and text[i] != ')':
                i += 1
            if i < n:
                i += 1  
            continue
        
        if text[i] == '\\':
            while i < n and text[i] != '\n':
                i += 1
            continue
        
        if i < n:
            result.append(text[i])
            i += 1
    
    return ''.join(result)

def main(source, target): 
    with open(source, encoding="utf-8") as file: 
        text = file.read() 
    # TODO complete main function

if __name__ == "__main__":
    assert(len(sys.argv) == 3, "Wrong arguments, format:\ntranslator.py <input_file> <output_file>")
    _, source, target = sys.argv 
    main(source, target)
# def main(source, target): 
#     with open(source, encoding="utf-8") as file: 
#         text = file.read()
#         code = remove_comments(text)
#         print(code)

# if __name__ == "__main__": 
#     _, source, target = sys.argv 
#     main(source, target)