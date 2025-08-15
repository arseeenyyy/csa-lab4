# Laboratory work № 4. Experiment
- Rubtsov Arsenii Dmitrievich, P3206
- Variant: `alg -> forth | stack | neum | mc | tick | binary | stream | port | cstr | prob1 | vector`
- Variant stand for:
  - `forth`: forth-like stack-based syntax with Reverse Polish Notation (RPN)
  - `stack`: stack-based CPU architecture
  - `neum`: Von Neumann architecture
  - `mc`: microcoded control unit
  - `tick`: cycle-accurate simulation 
  - `binary`: true binary machine code
  - `stream`: stream based I/O
  - `port`: port-mapped I/O
  - `cstr`: c-style null terminated strings
  - `prob1`: [Euler problem 4](https://projecteuler.net/problem=4)  
  - `vector`: vector operations (parallel data processing)

## Contents
1. [Programming Language](#programming-language)  
   - [Syntax](#syntax)  
   - [Semantics](#semantics)
2. [Memory Organization](#memory-organization)
   - [CPU Memory Model](#cpu-memory-model)
4. [ISA](#isa)
5. [Translator](#translator)
6. [CPU Model](#cpu-model)
7. [Testing](#testing)

## Programming Language

### Syntax
```ebnf
<program> ::= <instruction>* 
            | <definition>*

<instruction> ::= <stack_op> 
                | <math_op> 
                | <logic_op>
                | <memory_op> 
                | <control_op> 
                | <literal> 
                | <variable> 
                | <call>  

<definition> ::= ":" <name> <instruction>* ";"

<stack_op> ::= "dup" 
             | "drop" 
             | "swap" 
             | "over"
             | <number>

<math_op> ::= "+" 
            | "-" 
            | "*" 
            | "/" 
            | "mod"

<logic_op> ::= "and" 
             | "xor" 
             | "or" 
             | "=" 
             | ">" 
             | "<"

<memory_op> ::= "!" 
              | "@" 
              | "variable"

<control_op> ::= "if" 
               | "else" 
               | "then" 
               | "do" 
               | "loop" 
               | "begin" 
               | "until"

<number> ::= "-"? <digit>+

<name> ::= <letter> (<letter> | <digit>)*

<digit> ::= [0-9]

<letter> ::= [a-zA-Z]
```

### Semantics
- *This section will be filled later...*

## Memory Organization
### CPU Memory Model
  - *todo later...*
## ISA 
  - `lit <value>` - push an immediate value onto the stack
  - `dup` - duplicate top value of the stack
  - `drop` - drop top value of the stack
  - `+` - add top two values on the stack
  - `-` - substact top two values on the stack
  - `*` - multiply top two values on the stack
  - `/` - divide top two values on the stack
  - `and`
  - `or`
  - `swap`
  - `invert`
  - `=`
  - `do loop`
  - `!` - store the second value of the stack by address on the top of the stack
  - `@`- push the value on the stack from address on the top of the stack
  - `in <port>` - print top value of the stack
  - `.`
  - `." <str>"`
  - `emit` 
  - `variable <var_name>` - define variable
  - todo later
## Translator
  - *todo*
## CPU Model
  - *todo*
## Testing
  - *todo*

