import sys, os
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

def split_programm(text: str) -> List[str]:
    text = remove_comments(text)
    
    words = []
    for line in text.splitlines():
        line = line.strip()
        if not line:  
            continue
        words.extend(token for token in line.split() if token)
    
    return words

def text_2_terms(program: list[str]) -> tuple[list[dict], dict]:
    terms = []
    labels = {}  
    instruction_count = 0

    for i, token in enumerate(program):
        if token == ":":
            if i + 1 < len(program):
                label = program[i + 1]
                labels[label] = instruction_count
                terms.append({"symbol": token, "index": i, "type": "label_def"})
                terms.append({"symbol": label, "index": i + 1, "type":
                "label_name"})
    
    
    for i, token in enumerate(program):
        if token == ":":
            i += 1  
            continue
        if token in labels or token == ";":
            term_type = "label_ref" if token in labels else "end_label"
            terms.append({"symbol": token, "index": i, "type": term_type})
        elif symbol_2_instruction(token):
            terms.append({"symbol": token, "index": i, "type": "instruction"})
            instruction_count += len(symbol_2_instruction(token))
        else:
            try:
                int(token)
                terms.append({"symbol": token, "index": i, "type": "number"})
                instruction_count += 1  
            except ValueError:
                pass  

    return terms, labels

def translate(text: str) -> list[Instruction]:
    program = split_programm(text)
    is_valid, error = check_closing_brackets(program)
    if not is_valid:
        raise ValueError(error)

    terms, labels = text_2_terms(program)
    instructions = []
    i = 0

    while i < len(terms):
        term = terms[i]
        symbol = term["symbol"]

        if term["type"] == "instruction":
            instrs = symbol_2_instruction(symbol)
            if not instrs:
                raise ValueError(f"Unknown instruction: {symbol}")
            instructions.extend(instrs)
            i += 1
        elif term["type"] == "number":
            instructions.append(Instruction(Opcode.LIT, int(symbol)))
            i += 1
        elif term["type"] == "label_ref":
            if symbol not in labels:
                raise ValueError(f"Undefined label: {symbol}")
            instructions.append(Instruction(Opcode.CALL, labels[symbol]))
            i += 1
        elif term["type"] in {"label_def", "label_name", "end_label"}:
            i += 1  
        else:
            i += 1  

    if not instructions or instructions[-1].opcode != Opcode.HALT:
        instructions.append(Instruction(Opcode.HALT))

    return instructions

def main(source: str, target: str):
    with open(source, encoding="utf-8") as file:
        text = file.read()
    instructions = translate(text)
    binary = to_bytes(instructions)
    
    for instr in instructions:
        print(f"  {instr}")
    
    print(binary.hex(' '))
    
    decoded_instructions = from_bytes(binary)
    for instr in decoded_instructions:
        print(f"  {instr}")
    
    os.makedirs(os.path.dirname(target) or ".", exist_ok=True)
    with open(target, "wb") as f:
        f.write(binary)

if __name__ == "__main__":
    main("examples/cat.fth", "bin/test")