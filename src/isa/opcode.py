from enum import StrEnum, unique

@unique
class Opcode(StrEnum): 
    ADD = "+" 
    SUB = "-"
    DUP = "dup"