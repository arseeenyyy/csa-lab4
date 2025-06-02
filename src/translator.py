import sys, os
from typing import Optional, List, Dict, Tuple
from isa import Opcode, from_bytes, to_bytes, Term
import re

variables_map = {}  
procedures_map = {}  
variables_queue = {}
labels = {}
ADDR_SIZE = 4    
LIT_SIZE = 4     
VAR_SIZE = 4 

hex_number_pattern = r"^0[xX][0-9A-Fa-f]+$"
dec_number_pattern = r"^-?[0-9]+$"

def word_2_opcode(symbol: str) -> Opcode:
    try:
        return {
            "dup": Opcode.DUP,
            "drop": Opcode.DROP,
            "swap": Opcode.SWAP,
            "over": Opcode.OVER,
            "lit": Opcode.LIT,
            "+": Opcode.ADD,
            "-": Opcode.SUB,
            "*": Opcode.MUL,
            "/": Opcode.DIV,
            "mod": Opcode.MOD,
            "and": Opcode.AND,
            "or": Opcode.OR,
            "xor": Opcode.XOR,
            "=": Opcode.EQ,
            "<": Opcode.LT,
            ">": Opcode.GT,
            "!": Opcode.STORE,
            "@": Opcode.FETCH,
            "variable": Opcode.VARIABLE,
            ".": Opcode.PRINT_INT,
            "emit": Opcode.EMIT,
            "key": Opcode.KEY,
            "if": Opcode.IF,
            # "else": Opcode.ELSE,
            # "then": Opcode.THEN,
            "call": Opcode.CALL,
            "begin": Opcode.BEGIN,
            "until": Opcode.UNTIL,
            "load_addr": Opcode.LOAD_ADDR,
            ";": Opcode.RET,
            "halt": Opcode.HALT,
            "nop": Opcode.NOP
        }[symbol]
    except KeyError: 
        return None

all_opcodes = {opcode.value for opcode in Opcode}


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

def text_2_terms(text: str):
    text = remove_comments(text) 
    terms = []
    for line_num, line in enumerate(text.split(), 1): 
        words = line.strip().split()
        for pos, word in enumerate(words, 1): 
            terms.append(Term(line_num, pos, word))  
    
    stack = []
    i = 0
    while i < len(terms): 
        token = terms[i].word
        if token == ":": 
            stack.append((":", i)) 
            if i + 1 < len(terms) and word_2_opcode(terms[i + 1].word) is not None: 
                raise SyntaxError(f"Invalid procedure name: '{terms[i + 1].word}'")  
            i += 2
        elif token == Opcode.IF.value: 
            stack.append((Opcode.IF.value, i)) 
            i += 1
        elif token == Opcode.BEGIN.value: 
            stack.append((Opcode.BEGIN.value, i)) 
            i += 1
        elif token == Opcode.RET.value: 
            if not stack or stack[-1][0] != ":": 
                raise SyntaxError(f"Unbalanced procedure (missing ':' for ';')")
            stack.pop()
            i += 1
        elif token == Opcode.THEN.value: 
            if not stack or stack[-1][0] != Opcode.IF.value:  
                raise SyntaxError(f"Unbalanced if-then statement at line {terms[i].line}") 
            stack.pop()
            i += 1
        elif token == Opcode.UNTIL.value:
            if not stack or stack[-1][0] != Opcode.BEGIN.value:
                raise SyntaxError(f"Unbalanced begin-until statement at line {terms[i].line}") 
            stack.pop()
            i += 1
        # elif token == Opcode.ELSE.value: 
        #     if not stack or stack[-1][0] != Opcode.IF.value:  
        #         raise SyntaxError(f"Unbalanced if-else statement at line {terms[i].line}") 
        #     i += 1
        else: 
            i += 1
    
    if stack: 
        token, pos = stack[-1] 
        raise SyntaxError(f"Unbalanced '{token}' at line {terms[pos].line}")

    return terms

def translate_stage_1(text: str):
    global variables_map, procedures_map, variables_queue, labels
    
    terms = text_2_terms(text)
    code = []
    proc_code = []  
    
    variables_map.clear()
    procedures_map.clear()
    variables_queue.clear()
    
    i = 0
    while i < len(terms):
        term = terms[i]
        
        if term.word == ":":
            proc_name = terms[i+1].word
            procedures_map[proc_name] = None  
            i += 2
            continue
            
        elif term.word == "variable":
            var_name = terms[i+1].word
            value = 0
            i += 2
            variables_queue[var_name] = value
            continue
            
        i += 1
    
    i = 0
    proc_address = 0  
    current_procedure = None
    
    while i < len(terms):
        term = terms[i]
        
        if term.word == ":":
            proc_name = terms[i+1].word
            current_procedure = proc_name
            procedures_map[proc_name] = proc_address  
            i += 2
            continue
            
        elif term.word == "variable":
            i += 2
            continue
            
        if current_procedure is not None:
            if re.fullmatch(hex_number_pattern, term.word):
                arg = int(term.word, 16)
                proc_code.append({
                    "address": proc_address,
                    "opcode": Opcode.LIT,
                    "arg": arg,
                    "term": term,
                    "size": LIT_SIZE
                })
                proc_address += LIT_SIZE
            elif re.fullmatch(dec_number_pattern, term.word):
                arg = int(term.word)
                proc_code.append({
                    "address": proc_address,
                    "opcode": Opcode.LIT,
                    "arg": arg,
                    "term": term,
                    "size": LIT_SIZE
                })
                proc_address += LIT_SIZE
                
            # elif term.word == 'S"':
            #     i += 1
            #     string = terms[i].word.strip('"')
            #     proc_code.append({
            #         "address": proc_address,
            #         "opcode": Opcode.LIT,
            #         "arg": string,
            #         "term": term,
            #         "size": LIT_SIZE
            #     })
            #     proc_address += LIT_SIZE
            #     i += 1
                
            elif term.word == ";":
                proc_code.append({
                    "address": proc_address,
                    "opcode": Opcode.RET,
                    "term": term,
                    "size": 1
                })
                proc_address += 1
                current_procedure = None
                
            elif term.word in all_opcodes:
                try:
                    opcode = word_2_opcode(term.word)
                    proc_code.append({
                        "address": proc_address,
                        "opcode": opcode,
                        "term": term,
                        "size": 1
                    })
                    proc_address += 1
                except KeyError:
                    raise ValueError(f"Unknown opcode: {term.word}")
            
            i += 1
        else:
            i += 1
    i = 0
    main_address = proc_address  
    current_procedure = None
    
    while i < len(terms):
        term = terms[i]
        
        if term.word == ":":
            i += 2  
            continue
            
        elif term.word == "variable":
            i += 2
            continue
            
        if any(t["term"] == term for t in proc_code if "term" in t):
            i += 1
            continue
            
        if re.fullmatch(hex_number_pattern, term.word):
            arg = int(term.word, 16)
            code.append({
                "address": main_address,
                "opcode": Opcode.LIT,
                "arg": arg,
                "term": term,
                "size": LIT_SIZE
            })
            main_address += LIT_SIZE
            
        elif re.fullmatch(dec_number_pattern, term.word):
            arg = int(term.word)
            code.append({
                "address": main_address,
                "opcode": Opcode.LIT,
                "arg": arg,
                "term": term,
                "size": LIT_SIZE
            })
            main_address += LIT_SIZE
            
        elif term.word == 'S"':
            i += 1
            string = terms[i].word.strip('"')
            code.append({
                "address": main_address,
                "opcode": Opcode.LIT,
                "arg": string,
                "term": term,
                "size": LIT_SIZE
            })
            main_address += LIT_SIZE
            i += 1
            
        elif term.word in procedures_map:
            code.append({
                "address": main_address,
                "opcode": Opcode.CALL,
                "arg": term.word,
                "term": term,
                "size": ADDR_SIZE
            })
            main_address += ADDR_SIZE
            
        elif term.word in variables_queue:
            code.append({
                "address": main_address,
                "opcode": Opcode.LOAD_ADDR,
                "arg": term.word,
                "term": term,
                "size": ADDR_SIZE
            })
            main_address += ADDR_SIZE
            
        elif term.word == "halt":
            code.append({
                "address": main_address,
                "opcode": Opcode.HALT,
                "term": term,
                "size": 1
            })
            main_address += 1
            
            for var_name, value in variables_queue.items():
                variables_map[var_name] = main_address
                code.append({
                    "address": main_address,
                    "opcode": Opcode.VARIABLE,
                    "arg": value,
                    "term": None,
                    "size": VAR_SIZE
                })
                main_address += VAR_SIZE
                
        elif term.word in all_opcodes:
            try:
                opcode = word_2_opcode(term.word)
                code.append({
                    "address": main_address,
                    "opcode": opcode,
                    "term": term,
                    "size": 1
                })
                main_address += 1
            except KeyError:
                raise ValueError(f"Unknown opcode: {term.word}")
        
        i += 1
    
    full_code = proc_code + code
    return full_code

def translate_stage_2(code): 
    for instruction in code: 
        if instruction["opcode"] == Opcode.LOAD_ADDR: 
            instruction["arg"] = variables_map[instruction["arg"]]
        elif instruction["opcode"] == Opcode.CALL: 
            instruction["arg"] = procedures_map[instruction["arg"]] 
    return code

def get_first_executable(code): 
    addr = 0
    for instr in code: 
        if instr["opcode"] == Opcode.RET: 
            addr = instr["address"] + 1
    return addr

def main(source: str):
    with open(source, encoding="utf-8") as file:
        text = file.read()
        code = translate_stage_1(text)
        print(variables_map) 
        print(procedures_map)
        print(variables_queue)

        code = translate_stage_2(code)
        for tr in code: 
            print(tr)
        print(get_first_executable(code))

if __name__ == "__main__": 
    main("examples/test2.fth")

