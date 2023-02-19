# Project 8 - Compiling to C

We often think about compilers targeting machine code.  However, a
very common target for new languages is C.  There are many reasons for this:

* C can be programmed in a low-level way like machine code.
* C compilers are available for virtually every kind of machine.
* C code is easier to inspect and debug.
* C provides access to system interfaces, I/O, memory management and other features that might be useful.

## Setup

Before you begin, you might want to look at the short [C Programming
Tutorial](C-Programming-Tutorial.md). This is not an exhaustive
reference, but should give you enough information to write simple
programs.

## Your Task

Your goal is to transform Wabbit code to C, using it as a kind of
low-level machine language.  To do this, we're going to use a highly
restricted subset of C features.  As described below:

### Mapping Wabbit datatypes to C datatypes

You should define the following typenames that correspond to Wabbit
types

```
typedef int  w_int;
typedef double w_float;
typedef unsigned char w_char;
typedef int w_bool;
```

All of the code that you generate should only use the Wabbit types
such as `w_int`, `w_float`, etc.

### Variables

You can only declare uninitialized variables.  For example:

```
w_int x;
w_float y;
w_int z = 2 + 3;     // NO!!!!!!!!
```

All variables must be declared before use, at the top of the file or
function. Reminder: they are declared as uninitialized.

### Mathematical operations

You can only perform ONE operation at a time. Operations can
only involve constants and variables.  The result of an
operation must always be immediately stored in a variable.  For
example, to compute 2 + 3 * 4, you might do something like this:

```
w_int _t1;      /* Temporary variables */
w_int _t2;

_t1 = 3 * 4;
_t2 = 2 + t1;
```

### Control Flow

The only allowed control flow constucts are the following statements:

```
goto Label;
if (_variable) goto Label;

Label:
    ... code ...
```

No, you don't get `else` or `while`. 

### Printing

You may print things with printf().

## An Example

It probably feels weird to code in such a weird style.  Here's a
concrete example of what the output code might look like:

```
/* Sample Wabbit Code */
/* Print the first 10 factorials */

var result = 1;
var n = 1;

while n <= 10 {
    result = result * n;
    print result;
    n = n + 1;
}
```

Here's what the corresponding C code might look like (it can vary
as long as you observe the general rules above):

```
#include <stdio.h>

typedef int  w_int;
typedef double w_float;
typedef unsigned char w_char;
typedef int w_bool;

 w_int result;
 w_int n;

 int main() {
    w_bool _t1;
    w_int _t2;
    w_int _t3;

    result = 1;
    n = 1;
L1:
    _t1 = (n <= 10);
    if (_t1) goto L2;
    goto L3;
L2:
    _t2 = result * n;
    result = _t2;
    printf("%i\n", result);
    _t3 = n + 1;
    n = _t3;
    goto L1;
L3:
    return 0;
}
```

One thing to keep in mind... the goal is NOT to produce code for
humans to read.  Instead, it's to produce code that is minimal and
which can be reasoned about. There is very little actually happening
in the above code.  It has calculations and gotos. That is basically
it.  There is no unseen high-level magic going on. What you see
it what it is.

## Tips

Implementing this project might not be that much different that the
source formatter you wrote in `format.py`.  Instead of producing
Wabbit code, you'll be producing C code instead.  There's just a bit
more structure to how it looks.

You'll then compile that C code with the normal C compiler:

```
bash $ wabbit -c tests/Programs/12_loop.wb > out.c
bash $ cc out.c
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
