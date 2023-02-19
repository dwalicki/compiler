# Project 7 - Creating a Wabbit VM

Sometimes programming languages are compiled to run on an abstract
virtual machine (e.g., Python, Java JVM, etc.).  A virtual
machine is low level like an actual CPU, but is also simplified
in many ways.   For example, the machine could provide support
for high-level operations like printing.  Similarly, a machine
might simplify the use of memory and CPU registers.

## Overview

The basic idea of this project is as follows. Wabbit programs
are represented by a model.  For example, if you write this:

```
print 2 + 3 * 4;
```

There is an abstract syntax tree such as this:

```
PrintStatement(Add(Integer(2), Mul(Integer(3), Integer(4))))
```

In an earlier project, you wrote an interpreter that directly executed
the model.  This project is somewhat similar except that you're going
to turn the model into instructions that run on a simple stack
machine.  Here's an example of a basic stack machine:

```
class StackMachine:
    def __init__(self):
        self.stack = [ ]

    def PUSH(self, value):
        self.stack.append(value)

    def POP(self):
        return self.stack.pop()

    def ADD(self):
        right = self.POP()
        left = self.POP()
        self.PUSH(left + right)

    def MUL(self):
        right = self.POP()
        left = self.POP()
        self.PUSH(left * right)

    def PRINT(self):
        print(self.POP())
```

Here's an example of instructions that carry out the above Wabbit
program on this machine:

```
code = [ ('PUSH', 2),
         ('PUSH', 3),
         ('PUSH', 4),
         ('MUL',),
         ('ADD',),
         ('PRINT',) ]
```

To generate such code, you can write a function that's somewhat
similar to your code formatter.  Here's an example:

```
def generate_code(node, instructions):
    if isinstance(node, Integer):
        instructions.append(('PUSH', node.value))
    elif isinstance(node, Add):
        generate_code(node.left, instructions)
        generate_code(node.right, instructions)
        instructions.append(('ADD',))
    elif isinstance(node, Mul):
        generate_code(node.left, instructions)
        generate_code(node.right, instructions)
        instructions.append(('MUL',))
    elif isinstance(node, PrintStatement):
        generate_code(node.value, instructions)
        instructions.append(('PRINT',))
    ...
```

## How to proceed

You will be implementing both the virtual machine and the associated
code generator.  The easiest way to approach this project is to work
on it in stages.

### Step 1: Expression Evaluation

To start out, you should focus on getting simple expressions to evaluate.
For example, can you run programs such as the print statement shown
earlier:

```
print 2 + 3 * 4;
```

The example show in the overview can serve as a useful starting point.


### Step 2: Variables

The second step of the project should focus on global variables and
constants.  You'll need to extend your virtual machine with operations
related to load and storing of variables.  When you're done, you
should be able to run code for Wabbit programs such as this:

```
const pi = 3.14159;
var tau float;
tau = 2.0 * pi;
print tau;
```

### Step 3: Control Flow

After you have variables working, move on to control flow.  Consider
the following program with a conditional:

```
var a = 2;
var b = 3;
var maxval int;

if a < b {
   maxval = b;
} else {
   maxval = a;
}
print a;
```

Or this program with a loop:

```
var n = 10;
while n > 0 {
    print n;
    n = n - 1;
}
```

To handle control flow, you need to decompose the control flow into
branches and gotos.  First, you'll need to add some special
instructions to your VM for this:

```
('LABEL', name)      # Declare a label that's the target of a jump
('GOTO', name)       # Unconditionally jump to label name
('BZ', name)         # Jump to label name if top of the int stack is zero
```

You'll then need to figure out how to decompose `if` and `while` statements
into gotos.  For example, here is some pseudocode for the above programs
using `goto`.

```
var a = 2;
var b = 3;
var maxval int;

var t1 = a < b;
if t1 == 0: GOTO L2

L1:
   maxval = b;
   GOTO L3;
L2:
   maxval = a;
   GOTO L3;

L3:
print a;
```

Or this:

```
var n = 10;
L1:
    t1 = n > 0;
    if t1 == 0: GOTO L3
L2:
    print n;
    n = n - 1;
    GOTO L1;
L3:
    # Done
```

## Tips

One hurdle is internalizing the operation of a stack machine.  It
might help to work through a few examples.  Suppose you wanted to
compute `2 + 3 * 4`.  It can help to work through each operation one
at a time and write down the stack state:

```
PUSH 2         # Stack = [ 2 ]
PUSH 3         # Stack = [ 2, 3 ]
PUSH 4         # Stack = [ 2, 3, 4 ]
MUL            # Stack = [ 2, 12 ]
ADD            # Stack = [ 14 ]
```

You can make any machine instructions that you wish.  It's a virtual
machine.  As a virtual machine, you can design it in a way that tries
to make code generation easy.

For this stage of the project, you usually do NOT worry about the
possibility of incorrect programs.  That's the purpose of a
type-checking. If there were mistakes, you assume that they were
caught earlier.

