# z3-python
EECS 742 (Static Analysis) - Code analysis done in z3py!

### What do I do to run the program?
```
./Reaching <imp-file-to-evaluate>
```

Sample input:  
```
./Reaching examples/fibonacci.imp
```

Output:  
```
    EN1: [(A, ?), (B, ?), (C, ?), (N, ?)]
    EX1: [(A, ?), (B, ?), (C, ?), (N, 1)]
    EN2: [(A, ?), (B, ?), (C, ?), (N, 1)]
    EX2: [(A, 2), (B, ?), (C, ?), (N, 1)]
    EN3: [(A, 2), (B, ?), (C, ?), (N, 1)]
    EX3: [(A, 2), (B, 3), (C, ?), (N, 1)]
    EN4: [(A, 2), (B, 3), (C, ?), (N, 1)]
    EX4: [(A, 2), (B, 3), (C, 4), (N, 1)]
    EN5: [(A, 2), (A, 7), (B, 3), (B, 8), (C, 4), (C, 6), (N, 1), (N, 9)]
    EX5: [(A, 2), (A, 7), (B, 3), (B, 8), (C, 4), (C, 6), (N, 1), (N, 9)]
    EN6: [(A, 2), (A, 7), (B, 3), (B, 8), (C, 4), (C, 6), (N, 1), (N, 9)]
    EX6: [(A, 2), (A, 7), (B, 3), (B, 8), (C, 6), (N, 1), (N, 9)]
    EN7: [(A, 2), (A, 7), (B, 3), (B, 8), (C, 6), (N, 1), (N, 9)]
    EX7: [(A, 7), (B, 3), (B, 8), (C, 6), (N, 1), (N, 9)]
    EN8: [(A, 7), (B, 3), (B, 8), (C, 6), (N, 1), (N, 9)]
    EX8: [(A, 7), (B, 8), (C, 6), (N, 1), (N, 9)]
    EN9: [(A, 7), (B, 8), (C, 6), (N, 1), (N, 9)]
    EX9: [(A, 7), (B, 8), (C, 6), (N, 9)]
    EN10: [(A, 2), (A, 7), (B, 3), (B, 8), (C, 4), (C, 6), (N, 1), (N, 9)]
    EX10: [(A, 2), (A, 7), (B, 3), (B, 8), (C, 4), (C, 6), (N, 10)]
```

Additionally, a file named model.txt will be created with this output in the main directory.

*Note: The .imp extension on the file is not necessary; this program can be run on plaintext files, or any other type of file with readable characters. The examples in this repo use the .imp extension purely for distinguishing reasons; there is no special benefits beyond that.*

### What is static analysis?
Static program analysis is the analysis of computer software that is performed without actually executing programs, in contrast with dynamic analysis, which is analysis performed on programs while they are executing.
(Wikipedia)

### What is z3?
z3 is a theorem proving language. Essentially it tries to reason about logic or mathematical proofs in a procedural manner. Though this is not possible all of the time (thanks to Gödel), in many situations we can reason about or brute force some sort of decision procedure to prove something. I am using z3 to solve variations of SAT problems, an NP-complete problem in computing. Thus I am using z3 as a SAT solver. While z3 has a language of its own, the code in this repo uses Python bindings.

### What is a SAT solver?
A program which can take arbitrary input to a [Boolean satisfiability problem](https://en.wikipedia.org/wiki/Boolean_satisfiability_problem) (SAT) and outputs if the input is satisfiable (sat), unsatisfiable (unsat), or if it cannot be determined. If it can find a satisfiable solution, it may also output the model it used. This has many applications, and can be transformed into a solution for many other problems, such as liveness analysis or graph colorability, using a bit of clever conversions.

### So what am I trying to do?
Often it's very nice to know things about a program before they're even executed, such as whether it can actually run. As programmers we see this in the form of compiler errors; your compiler or interpreter runs static analysis to validate many properties of your code, along the process to converting it to machine language. This process can include multiple stages and many optimizations. For example, liveness analysis may be used to check the usage of different variables in a program, and your compiler may use that analysis to allocate memory in an efficient manner. Reaching analysis can determine at certain points in the code, where the values of variables were declared. This could be used, for example, to prove that at some point, a variable was declared, therefore it has a value and is non-null.

So knowing that static analysis is important to the validity of programs, my aim is to create some of these tools. Often these are created using functional languages such as Haskell, so the use of a theorem prover may seem like an odd choice. But the big picture looks like this:

We can analyze a program, line by line. Using a parser we can rip out all the details about each statement, and transform it into a form we're familiar and can use like a data structure. Compilers do exactly that. From that data structure, we can build up a system of equations to solve simultaneously, based on the properties of the progam. These equations model the control flow of the program, the declaration, usage, and overriding of variables, or the side effects of our program. And depending on what we're trying to do, we will find certain properties from these equations, build up a series of statements, then tell z3 we want them all to be true at the same time. Thus, z3 will run its SAT techniques on it and report that it can or cannot be done. Often, we can use this result to instantly generate some mathematic result we desire.

That's the big idea. If I can map a program to a series of equations, then I can simply hand those equations over to z3, which will promptly determine if the problem has a solution. I do not care how it does it (that's the hard part anyways), only the result. So in theory, my task should be a lot easier than directly proving the property of the language. And in more theory, trying to write a program to prove it in a general case is an extremely large amount of work. So, if I can convert the data to a form which can be proved using z3, I make my own life a lot easier!

### Where can I download z3, and the associated Python bindings?
All relevant z3 files may be found [here](https://github.com/Z3Prover/z3). The source files are directly available and free to edit however you please.
