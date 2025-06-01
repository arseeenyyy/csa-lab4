import sys, os
from typing import Optional, List, Dict, Tuple
from isa import Opcode, from_bytes, to_bytes, Term
import re

variables_map = {}  
procedures_map = {}  
variables_queue = {}
ADDR_SIZE = 4    
LIT_SIZE = 4     
VAR_SIZE = 4 

hex_number_pattern = r"^0[xX][0-9A-Fa-f]+$"
dec_number_pattern = r"^[0-9]+$"


# def instruction_size(instr: Instruction) -> int:
#     return 4 if instr.opcode in {Opcode.LIT, Opcode.CALL, Opcode.LOAD_ADDR} else 1

def word_2_opcode(symbol: str) -> Opcode:
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
        "else": Opcode.ELSE,
        "then": Opcode.THEN,
        "do": Opcode.DO,
        "loop": Opcode.LOOP,
        "call": Opcode.CALL,
        "begin": Opcode.BEGIN,
        "until": Opcode.UNTIL,
        "load_addr": Opcode.LOAD_ADDR,
        ";": Opcode.RET,
        "halt": Opcode.HALT,
        "nop": Opcode.NOP
    }[symbol]

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
    # TODO (check closing bracket)  
    return terms

def translate_stage_1(text: str):
    global variables_map, procedures_map, variables_queue
    
    terms = text_2_terms(text)
    code = []
    
    variables_map.clear()
    procedures_map.clear()
    variables_queue.clear()
    
    i = 0
    while i < len(terms):
        term = terms[i]
        
        if term.word == ":":  
            proc_name = terms[i+1].word
            procedures_map[proc_name] = i
            i += 2  
            continue
            
        elif term.word == "variable":  
            var_name = terms[i+1].word
            if i+2 < len(terms) and re.fullmatch(dec_number_pattern, terms[i+2].word):
                value = int(terms[i+2].word)
                i += 3
            else:
                value = 0
                i += 2
            variables_queue[var_name] = value
            continue
            
        i += 1
    
    i = 0
    address = 0
    current_procedure = None
    
    while i < len(terms):
        term = terms[i]
        
        if term.word == ":":
            proc_name = terms[i+1].word
            current_procedure = proc_name
            i += 2  
            continue
            
        elif term.word == "variable":
            i += 2
            continue
            
        elif re.fullmatch(hex_number_pattern, term.word):
            arg = int(term.word, 16)
            code.append({
                "address": address,
                "opcode": Opcode.LIT,
                "arg": arg,
                "term": term,
                "size": LIT_SIZE
            })
            address += LIT_SIZE
            
        elif re.fullmatch(dec_number_pattern, term.word):
            arg = int(term.word)
            code.append({
                "address": address,
                "opcode": Opcode.LIT,
                "arg": arg,
                "term": term,
                "size": LIT_SIZE
            })
            address += LIT_SIZE
            
        elif term.word == 'S"':
            i += 1
            string = terms[i].word.strip('"')
            code.append({
                "address": address,
                "opcode": Opcode.LIT,
                "arg": string,
                "term": term,
                "size": LIT_SIZE
            })
            address += LIT_SIZE
            i += 1
            
        elif term.word in procedures_map and term.word != current_procedure:
            code.append({
                "address": address,
                "opcode": Opcode.CALL,
                "arg": procedures_map[term.word],
                "term": term,
                "size": ADDR_SIZE
            })
            address += ADDR_SIZE
            
        elif term.word in variables_queue:
            code.append({
                "address": address,
                "opcode": Opcode.LOAD_ADDR,
                "arg": term.word,  
                "term": term,
                "size": ADDR_SIZE
            })
            address += ADDR_SIZE
            
        elif term.word == ";":
            if current_procedure:
                code.append({
                    "address": address,
                    "opcode": Opcode.RET,
                    "term": term,
                    "size": 1
                })
                address += 1
                current_procedure = None
            else:
                raise ValueError("RET without procedure definition")
            
        elif term.word in all_opcodes:
            try:
                opcode = word_2_opcode(term.word)
                
                if opcode == Opcode.HALT:
                    code.append({
                        "address": address,
                        "opcode": Opcode.HALT,
                        "term": term,
                        "size": 1
                    })
                    address += 1
                    
                    for var_name, value in variables_queue.items():
                        variables_map[var_name] = address
                        code.append({
                            "address": address,
                            "arg": value,
                            "term": None,
                            "size": VAR_SIZE
                        })
                        address += VAR_SIZE
                else:
                    code.append({
                        "address": address,
                        "opcode": opcode,
                        "term": term,
                        "size": 1
                    })
                    address += 1
            except KeyError:
                raise ValueError(f"Unknown opcode: {term.word}")
                
        i += 1
    
    return code

def main(source: str):
    with open(source, encoding="utf-8") as file:
        text = file.read()
        code = translate_stage_1(text)
        print(variables_map) 
        print(procedures_map)
        print(variables_queue)
        for term in code: 
            print(term)
        # final = translate_stage_2(code)
        # for tr in final: 
        #     print(tr)

if __name__ == "__main__": 
    main("examples/test.fth")


