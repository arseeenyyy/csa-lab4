import sys
from typing import Optional, List, Tuple
from isa import Opcode, Instruction, from_bytes, to_bytes


def symbol_2_instruction(symbol: str) -> Optional[List[Instruction]]: 
    """
    Mapping source code operators to opcodes
    """
    try: 
        value = int(symbol) 
        return [Instruction(Opcode.LIT, value)]
    except ValueError: 
        pass
    return {
        "dup": [Instruction(Opcode.DUP)],
        "drop": [Instruction(Opcode.DROP)],
        "swap": [Instruction(Opcode.SWAP)],
        "over": [Instruction(Opcode.OVER)],
        "+": [Instruction(Opcode.ADD)],
        "-": [Instruction(Opcode.SUB)],
        "*": [Instruction(Opcode.MUL)],
        "/": [Instruction(Opcode.DIV)],
        "mod": [Instruction(Opcode.MOD)],
        "and": [Instruction(Opcode.AND)],
        "or": [Instruction(Opcode.OR)],
        "xor": [Instruction(Opcode.XOR)],
        "=": [Instruction(Opcode.EQ)],
        "<": [Instruction(Opcode.LT)],
        ">": [Instruction(Opcode.GT)],
        "!": [Instruction(Opcode.STORE)],
        "@": [Instruction(Opcode.FETCH)],
        "variable": [Instruction(Opcode.VARIABLE)],  
        ".": [Instruction(Opcode.PRINT_INT)],
        "emit": [Instruction(Opcode.EMIT)],
        "key": [Instruction(Opcode.KEY)],
        '."': [Instruction(Opcode.PRINT_STRING)],  
        "if": [Instruction(Opcode.IF)],  
        "else": [Instruction(Opcode.ELSE)],  
        "then": [Instruction(Opcode.THEN)],
        "do": [Instruction(Opcode.DO)],
        "loop": [Instruction(Opcode.LOOP)],  
        "halt": [Instruction(Opcode.HALT)]
    }.get(symbol)

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

def check_closing_brackets(terms: list[str]) -> Tuple[bool, Optional[str]]:
    """
    Checks whether the structures in the token list are closed correctly.
    """
    # TODO update error message
    stack = []
    i = 0
    while i < len(terms):
        token = terms[i]
        if token == ":":
            stack.append((":", i))
            if i + 1 < len(terms) and symbol_2_instruction(terms[i + 1]) is not None:
                return False, f"Error with procedure"
            if i + 1 >= len(terms) or terms[i + 1] == ";":
                return False, f"Error with procedure"
            i += 2
        elif token == Opcode.IF.value:
            stack.append((Opcode.IF.value, i))
            i += 1
        elif token == Opcode.BEGIN.value:
            stack.append((Opcode.BEGIN.value, i))
            i += 1
        elif token == Opcode.DO.value:
            stack.append((Opcode.DO.value, i))
            i += 1
        elif token == ";":
            if not stack or stack[-1][0] != ":":
                return False, f"error with end of procedure"
            stack.pop()
            i += 1
        elif token == Opcode.THEN.value:
            if not stack or stack[-1][0] != Opcode.IF.value:
                return False, f"Error with if then statement"
            stack.pop()
            i += 1
        elif token == Opcode.UNTIL.value:
            if not stack or stack[-1][0] != Opcode.BEGIN.value:
                return False, f"Error with begin until statement"
            stack.pop()
            i += 1
        elif token == Opcode.LOOP.value:
            if not stack or stack[-1][0] != Opcode.DO.value:
                return False, f"Error with do loop statement"
            stack.pop()
            i += 1
        elif token == Opcode.ELSE.value:
            if not stack or stack[-1][0] != "if":
                return False, f"Error with if else then"
            i += 1
        else:
            i += 1
    if stack:
        token, pos = stack[-1]
        return False, f"error with smth else"
    return True, None

# def main(source, target): 
#     with open(source, encoding="utf-8") as file: 
#         text = file.read() 
#     # TODO complete main function

# if __name__ == "__main__":
#     assert(len(sys.argv) == 3, "Wrong arguments, format:\ntranslator.py <input_file> <output_file>")
#     _, source, target = sys.argv 
#     main(source, target)
# def main(source, target): 
#     with open(source, encoding="utf-8") as file: 
#         text = file.read()
#         code = remove_comments(text)
#         print(code)

# if __name__ == "__main__": 
#     _, source, target = sys.argv 
#     main(source, target)