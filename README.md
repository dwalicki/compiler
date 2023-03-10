# Write a Compiler : 2023

Hello! This is the course project repo for the "Write a Compiler"
course.  This project will serve as the central point of discussion, code
sharing, debugging, and other matters related to the compiler project.

Although each person will work on their own compiler, it is requested
that all participants work from this central project, but in a separate
branch.   You'll perform these setup steps:

    bash % git clone https://github.com/dabeaz-course/compilers_2023_01
    bash % cd compilers_2023_01
    bash % git checkout -b yourname
    bash % git push -u origin yourname

There are a couple of thoughts on this approach. First, it makes it
easier for me to look at your code and answer questions (you can 
point me at your code, raise an issue, etc.).   It also makes it easier
for everyone else to look at your code and to get ideas.  Writing a
compiler is difficult. Everyone is going to have different ideas about
the implementation, testing, and other matters.  By having all of the
code in one place and in different branches, it will be better.

I will also be using the repo to commit materials, solutions, and 
other things as the course nears and during the course.

Finally, the repo serves as a good historical record for everything
that happened during the course after the fact.

Best,
Dave

## Preparation

To prepare for writing a compiler, there are certain background topics
that you might want to review.  First, as a general overview, you
might look at the first part of the excellent book [Crafting Interpreters](https://craftinginterpreters.com).
Writing a compiler is similar to an interpreter (in fact, we'll even be writing an
interpreter as part of the project).   As for specific topics, here
are some important facets of the project:

* Trees and recursion.  Most of the data structures in a compiler are
  based on trees and recursively defined data structures. As such,
  much of the data processing also involves recursive functions.
  Recursion is often not a part of day-to-day coding so it's something
  that you might want to review in advance.  I strongly advise
  working the [Warmup Exercise](docs/Warmup-Exercises.md) to see examples of
  the kind of recursion used in a compilers project.  If you are
  using a statically typed language (e.g., Rust, C++, etc.), it
  is STRONGLY advised that you review techniques for representing trees.

* Computer architecture.  A compiler translates high-level programs
  into low-level "machine code" that's typically based on the von Neumann architecture
  (https://en.wikipedia.org/wiki/Von_Neumann_architecture).  I don't
  assume prior experience writing machine language, but you should
  know that computers work by executing simple arithmetic instructions,
  loading and storing values from memory, and making "goto" jumps.

* Programming language semantics.  Writing a compiler also means that
  you're implementing a programming language.  That means knowing a
  lot of the fine details about how programming languages work. This
  includes rules for variables, expression evaluation (e.g., precedence),
  function calls, control flow, type checking, and other matters.
  In this course, we're creating a very simple language.  However,
  there are still many opportunities for confusion.  One such area
  is understanding the difference between an "expression" and a
  "statement."  In Python, that can be studied further by exploring
  the difference between the `eval()` and the `exec()` built-in
  functions.  Why are these functions different?

* Working interactively from the command line. The compiler project
  is a command-line based application.  You should be able to navigate
  the file-system, write command-line based scripts, and interactively
  debug programs from the command-line.   The `python -i` option
  may be especially useful.

* String processing. Part of the project involves writing a
  parser.  This involves a certain amount of text processing.
  You should be comfortable iterating over characters, splitting
  strings apart, and performing other common string operations.

## Warmup work

If you're looking to get started, here are some starting projects.  The course starts
by working on Project 0.

* [Warmup Exercises](docs/Warmup-Exercises.md)
* [Implementing an Interpreter (PyCon India)](https://www.youtube.com/watch?v=VUT386_GKI8)

## The Project

We are writing a compiler for the language [Wabbit](docs/Wabbit-Specification.md).
The following links provide more information on specific project stages.

### Week 1 - The Structure of Programs

* [Project 0 - The Metal](docs/Project0_The_Metal.md)
* [Project 0.5 - SillyWabbit](docs/Project0_5_SillyWabbit.md)
* [Project 1 - The Model](docs/Project1_The_Model.md)

### Week 2 - The Semantics of Programs

* [Project 2 - The Interpreter](docs/Project2_The_Interpreter.md)
* [Project 5 - Type Checking](docs/Project5_Type_Checking.md)
* [Project 6 - Transformations](docs/Project6_Transformation.md)

### Week 3 - The Syntax of Programs

* [Project 3 - The Lexer](docs/Project3_Tokenizing.md)
* [Project 4 - The Parser](docs/Project4_Parsing.md)

### Week 4 - The Translation of Programs

One of the following code generation projects is usually completed.

* [Project 7 - Wabbit VM](docs/Project7_WVM.md)
* [Project 8 - Compiling to C](docs/Project8_C.md)
* [Project 9 - LLVM](docs/Project9_LLVM.md)
* [Project 10 - Web Assembly](docs/Project10_WASM.md)

## Resources

* [Documents & Knowledge Base](docs/README.md)

## Live Session Recordings

Videos from the live sessions will be posted here.

**Day 1 (January 3)**

* [Part 0, Introduction, Project overview](https://vimeo.com/786122275/33f1729c68) (84 min)
* [Part 1, Model/AST, Project 1](https://vimeo.com/786122481/ee581ffb8c) (81 min)
