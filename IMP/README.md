### Note about this directory

None of the source code is mine; it is a subset of what is available at:

https://github.com/DrkSephy/python-imp-interpreter

I have made only small modifications to it for it to be more in line with a
reaching analysis tool. Changes made are:

- Prevent evaluation of the AST. Once it creates the AST it simply returns it.

- Rename classes for simplicity and familiarity.
