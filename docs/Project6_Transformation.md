# Project 6 : Transformation

One of the most critical parts of the whole compiler is the data model
that you use to represent programs.  For example, to represent an
expression such as `x + 3 * 4`, you might have a data structure like
this:

```
Add(Name('x'), Mul(Integer(3), Integer(4)))
```

However, executing the code, the compiler might do too much
work.  For example, perhaps the compiler could just precompile the
multiplication and replace the whole operation with a node such as this:

```
Add(Name('x'), Integer(12))
```

This kind of optimization is known as constant-folding.

As another example, sometimes people insert debugging code into
their program like this:

```
if true {
   statements
}
```

They'll then flip the `true` to `false` and back (in their source editor) and
recompile. Instead of literally executing an `if`-statement for such code,
the compiler could be smart enough to remove the `if` altogether and
just execute the statements (although one would still need to be mindful
of scoping rules).

Your task in this project is to see if you can apply transformations
to the model that result in a simplified model like this.

## This project is optional

Applying transformations to the model can result in simplified compiler
output.  However, it's purely optional.  If you're pressed for time
or want to work on other things, you can skip this project.


