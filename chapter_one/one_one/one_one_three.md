## 1.1.3 Evaluating Expressions

One of our goals in this chapter is to isolate issues about thinking procedurally. As a case in point, let us consider that, in evaluating expressions, the interpreter is itself following a procedure.

- To evaluate an expression, do the following:
1. Evaluate the sub-expressions of the expression.
2. Apply the procedure whose value is the middle subexpression (the operator) to the arguments that are the values of the other subexpressions (the operands).

Even this simple rule illustrates some important points about processes in general. First, observe that the first step dictates that in order to accomplish the evaluation process for an expression we must first perform the evaluation process on each element of the expression. Thus, the evaluation rule is _recursive_ in nature; that is, it includes, as one of its steps, the need to invoke the rule itself<sup>10</sup>.

Notice how succinctly the idea of recursion can be used to express what, in the case of a deeply nested expression, would otherwise be viewed as a rather complicated process. For example, evaluating
```
>>> (2 + (4 * 6)) * (3 + 5 + 7)
```
requires that the evaluation rule be applied to four different expressions (Two addition, and two multiplication). 

We can obtain a picture of this process by representing the expression in the form of a tree, as shown in figure 1.1.

**Figure 1.1**
```
390
├── 26
│   ├── 2
│   ├── +
│   └── 24
│       ├── 4
│       ├── *
│       └── 6
├── *
└── 15
    ├── 3
    ├── +
    ├── 5
    ├── +
    └── 7
```

Each expression is represented by a node wih branches corresponding to the operator and the operands of the expression stemming from it. The terminal nodes (that is, nodes with no branches stemming from them) represent either operators or numbers. Viewing evaluation in terms of the tree, we can imagine that the values of the operands percolate leftward, starting from the terminal nodes and then combining at "left-er" levels. In general, we shall see that recursion is a very powerful technique for dealing with hierarchical, treelike objects. In fact, this form of the evaluation rule is an example of a general kind of process known as tree accumulation.

Next, observe that the repeated application of the first step brings us to the point where we need to evaluate primitive expressions such as numerals, built-in operators, or other names. We take care of the primitive cases by stipulating that

- the values of numerals are the numbers that they name,
- the values of built-in operators are the machine instruction sequences that carry out the corresponding operations, and
- the values of other names are the objects associated with those names in the environment.

We may regard the second rule as a special case of the third one by stipulating that symbols such as `+` and `/` are also included in the global environment, and are associated with the sequences of machine instructions that are their "values." The key point to notice is the role of the environment in determining the meaning of the symbols in expression. In an interactive language such as Python, it is meaningless to speak of the value of an expression, such as `x+1` without specifying any information about the environment that would provide a meaning for `x`, or even the symbol `+`. As we shall see in chapter 3, the general notion of the environment as providing a context in which evaluation takes place will play an important role in our understanding of program execution.

Notice that the evaluation rule given above does not handle definitions. For instance, evaluating `x = 3` does not apply `=` to two arguments, one of which is the value of the symbol `x` and the other of which is 3, since the purpose of the `=` is precisely to associate `x` with a value. (That is, `x = 3` is not an expression).

Such exceptions to the general evaluation rule are called _special forms_. So far `=` is the only example of a special form that we have seen so far, but we will meet others shortly. Each special form has its own evaluation rule. The various kinds of expressions (each with its associated evaluation rule) constitute the syntax of a programming language.


---

<sup>10</sup>It may seem strange that the evaluation rule says, as a part of the first step, that we should evaluate the middle element of an expression, since at this point that can only be an operator such as a `+` or `/` representing a built-in primitive procedure such as addition or division. We will see later that it is useful to be able to work with expressions who operators are themselves compound expressions.