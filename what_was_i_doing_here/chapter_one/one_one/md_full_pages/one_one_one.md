## 1.1.1 - Expressions

One easy way to get started at programming is to examine some typical interactions with an interpreter for Python. Imagine that you are sitting at a computer terminal. You type an _expression_, and the interpreter responds by displaying the result of its _evaluating_ that expression.

One kind of primitive expression you might type is a number. (More precisely, the expression that you type consists of the numerals that represent the numbed rin base 10.) If you present Python with a number

```
>>> 486
```

the interpreter will respond by printing<sup>5</sup>

```
486
```

Expressions representing numbers may be combined with an expression representing a  primitive procedure (such as + or *) to form a compound expression that represents the application for the procedure to those numbers. For example: 

```
>>> 137 + 349
486
>>> 1000 - 734
266
>>> 5 * 99
495
>>> 10 / 5
2.0
>>> 2.7 + 10
12.7
```

In Python, mathematical expressions, such as the ones shown above, are written in accordance to the customary mathematical conventions. Compound expressions are done so as well:

```
>>> 1 + 2 + 3
6
>>> 3 - 2 - 1
0
>>> 10 * 2 + 4
24
>>> 12 - (6 / 3)
10
```

When computing mathematical expressions, the Python interpreter observes the conventional Order of Operations.

Even with complex expressions, the interpreter always operates in the same basic cycle: It reads an expression from the terminal, evaluates the expression, and prints the result. This mode of operation is often expressed by saying that the interpreter runs in a _read-eval-print loop_. Observe in particular that it is not necessary to explicitly instruct the interpreter to print the value of the expression.

---

<sup>5</sup>Throughout this book, when we wish to emphasize the distinction between the input typed by the user and the response printed by the interpreter, we will show the former preceded by three greater-than signs. (>>>)