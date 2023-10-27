## 1.1.4 - Compound Procedures

We have identified in Python some of the elements that must appear in any powerful programming language:

- Numbers and arithmetic operations are primitive data and procedures.
- Nesting of combinations provides a means of combining operations.
- Definitions that associate names with values provide a limited means of abstraction.

Now we will learn about _functions_, a much more powerful abstraction technique by which a compound operation can be given a name and then referred to as a unit.

We begin by examining how to express the idea of "squaring." We might say, "To square something, multiply it by itself." This is expressed in our language as<sup>13</sup>

```
>>> def square(x):
...     return x * x
```

We can understand this in the following way:

```
  To  square something,
   |    |    |
   v    v    v
  def square(x):
      return x * x
             ^ ^ ^
  multiply __|_| |
        it __|   |
 by itself.______|
```

We have here a function which has been given the name `square`. The function represents the operation of multiplying something by itself. The thing to be multiplied is given a local name, `x`, which plays the same  role that a pronoun plays in natural language. Evaluating the definition creates this function and associates it with the name `square`.

The general form of a function definition is

```
def <name>(<paramenters>):
    <body>
```

The <name> is a symbol to be associated with the function definition in the environment. The <parameters> are the names used within the body of the function to refer to the corresponding arguments of the function. The <body> is the code to be evaluated and executed. The <name> is followed by the <parameters>, which are grouped in parentheses and separated by commas, followed by a colon.

Having defined `square`, we can now use it:

```
>>> square(21)
441
>>> square(1 + 1)
4
>>> square(square(2))
16
```

We can also use square as a building block in defining other functions. For example, _x<sup>2</sup>+ y<sup>2</sup>_ can be expressed as

```
>>> square(x) + square(y)
```

We can easily define a function `sum-of-squares` that, given any two numbers as arguments, produces the sum of their squares:

```
>>> def sum-of-squares(x, y):
...     return square(x) + square(y)
...
>>> sum-of-squares(3, 4)
25
```

Now we can use `sum-of-squares` as a building block in constructing more functions:

```
>>> def f(a):
...     return sum-of-squares(a+1, a+2)
...
>>> f(5)
136
```

Functions are used in a similar fashion as built-in operators like `+` and `*`. For example, if we did something a bit silly and created a function that added two numbers, using `+`, it would look something like this:

```
>>> def add(x, y):
...     return x + y
```

Now, if we were to use this function, it would produce the same result as `+` would:

```
>>> 1 + 1
2
>>> add(1, 1)
2
>>> 5 - (1 + 1)
3
>>> 5 - add(1, 1)
3
```

---

<sup>13</sup>In the Python shell, a line that "builds" upon the previous line is represented by `...`.