import sys, os
from typing import Optional, List, Dict, Tuple
from isa import Opcode, Instruction, from_bytes, to_bytes

variables_map: Dict[str, int] = {}  
procedures_map: Dict[str, int] = {}  
variables_queue: Dict[str, int] = {}
def symbol_2_instruction(symbol: str) -> Optional[Instruction]:
    try: 
        value = int(symbol) 
        return Instruction(Opcode.LIT, value)
    except ValueError: 
        pass
    return {
        "dup": Instruction(Opcode.DUP),
        "drop": Instruction(Opcode.DROP),
        "swap": Instruction(Opcode.SWAP),
        "over": Instruction(Opcode.OVER),
        "+": Instruction(Opcode.ADD),
        "-": Instruction(Opcode.SUB),
        "*": Instruction(Opcode.MUL),
        "/": Instruction(Opcode.DIV),
        "mod": Instruction(Opcode.MOD),
        "and": Instruction(Opcode.AND),
        "or": Instruction(Opcode.OR),
        "xor": Instruction(Opcode.XOR),
        "=": Instruction(Opcode.EQ),
        "<": Instruction(Opcode.LT),
        ">": Instruction(Opcode.GT),
        "!": Instruction(Opcode.STORE),
        "@": Instruction(Opcode.FETCH),
        "variable": Instruction(Opcode.VARIABLE),
        ".": Instruction(Opcode.PRINT_INT),
        "emit": Instruction(Opcode.EMIT),
        "begin": Instruction(Opcode.BEGIN),
        "until": Instruction(Opcode.UNTIL),
        "key": Instruction(Opcode.KEY),
        "if": Instruction(Opcode.IF),
        "else": Instruction(Opcode.ELSE),
        "then": Instruction(Opcode.THEN),
        "do": Instruction(Opcode.DO),
        "loop": Instruction(Opcode.LOOP),
        ";": Instruction(Opcode.RET),
        "halt": Instruction(Opcode.HALT)
    }.get(symbol.lower())  

def remove_comments(text: str) -> str:
    """
    Remove comments from the whole programm
    """
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

def instruction_size(instr: Instruction) -> int:
    return 4 if instr.opcode in {Opcode.LIT, Opcode.CALL} else 1

def split_program(text: str) -> List[str]:
    text = remove_comments(text)
    tokens = []
    current_token = []
    in_string = False
    
    for char in text:
        if char == '"':
            if in_string:
                current_token.append(char)
                tokens.append(''.join(current_token))
                current_token = []
                in_string = False
            else:
                if current_token:
                    tokens.append(''.join(current_token))
                    current_token = []
                current_token.append(char)
                in_string = True
        elif in_string:
            current_token.append(char)
        elif char.isspace():
            if current_token:
                tokens.append(''.join(current_token))
                current_token = []
        else:
            current_token.append(char)
    
    if current_token:
        tokens.append(''.join(current_token))
    
    return [token for token in tokens if token]

def main(source: str):
    with open(source, encoding="utf-8") as file:
        text = file.read()

if __name__ == "__main__": 
    main("examples/test.fth")


