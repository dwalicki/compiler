# Project 9 - Generating LLVM

In this project, we take Wabbit and turn it into LLVM.  Before
proceeding, you need to work through the [LLVM Tutorial](LLVM-Tutorial.md).

## Overview

The overall strategy here is going to be very similar to how the interpreter
works. Recall, that there was a top-level function like this:

```
def interpret(node, context):
    ...
```

It's going to be almost exactly the same idea here. You'll make a
special LLVMContext class.  Inside that class, you'll include
the usual details such as the environment, but also need to organize
it for LLVM code generation.

## LLVM Details

To create LLVM, there are a few essential elements.  First, you need
make a mapping between Wabbit types and LLVM types.  I suggest
making a type mapping table like this:

```
_typemap = {
    'int': 'i32',
    'float': 'double',
    'bool': 'i1',
    'char': 'i8'
}
```

Any time you need to map a Wabbit type to LLVM, you can consult the
table to get the appropriate type name.   You also may need to carry types
around in your program to figure what to do at different stages.

Second, the general structure of the LLVM output is as follows:

```
; out.ll
;
; External declarations (functions written in C)
declare void @_print_int(i32 %x)

; Global variables (var/const decls in Wabbit)
@pi = global double 3.14159

; Main function (all instructions)
define void main()
{
   ...  ; Various instructions
   ret void
}
```

Because there are multiple "sections" to the output, you may need to
manage the contents of each section separately as you generate code.
You can join them all together at the end to make the final result.

Finally, there is a certain amount of book-keeping involved.
LLVM code involves the creation of many temporary variables.
For example, to compute and print `2 + 3 * 4`, you need to create
instructions like this:

```
%r1 = mul i32 3, 4
%r2 = add i32 2, %r1
call void @_print_int(i32 %r2)
```

You'll need to keep track of the names like `%r1` and `%r2` as you
produce code.  You'll also need to remember their types.

## Testing

To test this part of the project, you should be able to take any of
the scripts in `tests/Programs/` and turn it into LLVM output.  It might
look like this:

```
bash $ wabbit -llvm tests/Programs/12_loop.wb
; out.ll

declare void @_print_int(i32 %x)
declare void @_print_float(double %x)
declare void @_print_bool(i1 %x)
declare void @_print_char(i8 %x) 

@n = global i32 0
@value = global i32 0

define void @main() 
{
entry:
  store i32 1, i32* @n
  store i32 1, i32* @value
  br label %test
test:
  %.5 = load i32, i32* @n
  %.6 = icmp slt i32 %.5, 10
  br i1 %.6, label %body, label %exit
body:
  %.8 = load i32, i32* @value
  %.9 = load i32, i32* @n
  %.10 = mul i32 %.8, %.9
  store i32 %.10, i32* @value
  %.12 = load i32, i32* @value
  call void @_printi(i32 %.12)
  %.14 = load i32, i32* @n
  %.15 = add i32 %.14, 1
  store i32 %.15, i32* @n
  br label %test
exit:
  ret void
}
bash $
```

If you save this output to a file, you can compile it with the `clang`
compiler as long you as you also include the required runtime
functions (see below).  For example:

```
bash $ wabbit -llvm tests/Programs/12_loop.wb >out.ll
bash $ clang out.ll misc/runtime.c
bash $ ./a.out
1
2
6
24
120
720
5040
40320
362880
bash $
```

## Runtime Library

To perform printing, you'll need to include a small C library of print
functions. For example:

```
/* runtime.c */
#include <stdio.h>

void _print_int(int x) {
    printf("%i\n", x);
}
```

A possible `runtime.c` file can be found in the `misc/` directory.

## Tips

In principle, generating LLVM is not much different than the source
formatter you wrote in the first part of the compiler project.  You'll
write code that walks the model and creates a lot of small text
fragments that get put together to form the whole program.

The main difference is that there is a bit more book-keeping involved
(types, names) and some of the output looks a lot more messy.


