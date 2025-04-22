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
  - `prob1`: todo
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
- *This section will be filled later...*
### Semantics
- *This section will be filled later...*

## Memory Organization
### CPU Memory Model
  - *todo later...*
## ISA 
  - **Literal**
    - syntax: `lit <value>`
    - descrp: push an immediate value onto the data stack.
    - operation: `stack.push(<value>)`
  - **Dup**
    - syntax: `dup`
    - descrp: duplicate top value of stack
    - operation: `stack.push(stack.top())`
  - **Drop**
    - syntax: `drop`
    - descrp: drop top value of stack
    - operation: `stack.pop()`
  - **Add**
    - syntax: `+`
    - descrp: add the top two values on the stack
    - operation: `stack.push(stack.pop() + stack.pop())`
  - **And**
    - syntax: `and`
    - descrp: perform a bitwise AND on top two values of stack
    - operation: `stack.push(stack.pop() && stack.pop())`
  - **Or**
    - syntax: `or`
    - descrp: perform a bitwise OR on top two values of stack
    - operation: `stack.push(stack.pop() || stack.pop())`
  - **For loop**
    - syntax: `do loop`
    - descrp: --
    - operation: --
  - **Not**
    - syntax: `invert`
    - descrp: perform bitwise invertion on top value of stack
    - operation: `stack.push(not(stack.pop))`
## Translator
  - *todo*
## CPU Model
  - *todo*
## Testing
  - *todo*

