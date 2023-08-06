# PyExecutable

## builder

### Executable(name : str, autosave : bool = True)

Executable file.

#### save()

Save an executable

#### close()

Close an executable

#### addInstruction(instruction)

Add instruction to executable

#### getAssembler()

Get assembler code of executable

#### getInstructions()

Get instructions of executable

### instructions

#### output(string)

Output string

##### newline()

Output newline

#### exit()

Exit from executable

## assemmbler

### compile()

Compile assembler code


## Examples

### Hello world!

```python
from PyExecutable.builder import Executable, instructions

with Executable('helloworld.exe') as exe:
	exe.addInstruction(instructions.output('hello world'))
```

### Visit card

```python
from PyExecutable.builder import Executable, instructions

exe = Executable('hippo.exe')
exe.addInstruction(instructions.output('Hello world!'))
exe.addInstruction(instructions.output.newline())
exe.addInstruction(instructions.output("I'm simple program. My name is \"hippo.exe\"."))
```
