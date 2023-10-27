### Self-Summary: Applicative Vs Normal Order

There are two ways that an interpreter can evaluate an expression; one being applicative order, and the other being normal order.

Take a look at the following code exert:
```
>>> def square(x):
...     return x * x
...
>>> square(square(2) + square(3))
```

If we were to write out our steps for solving the expression on the last line, most of us would usually write out something like this:

```
First, calculate the inside of the outer square method.
= square((2 * 2) + (3 * 3))
= square(4 + 9)
= square(13)
Then, calculate the outer square.
= 13 * 13
= 169
```

This way of solving the expression is called _applicative-order evaluation_. We first evaluate the "lower" arguments and then apply them to the "higher" expressions. The other way to calculate the above problem would look like this:

```
square(square(2) + square(3))
= (square(2) + square(3)) * (square(2) + square(3))
= ((2 * 2)) + (3 * 3)) * ((2 * 2) + (3 * 3))
= (4 + 9) * (4 + 9)
= 13 * 13
= 169
```

This way of evaluating is called _normal-order evaluation_. It fully expands and then reduces a problem. From this example, we can see that the applicative order is more efficient, as the normal order ends up calculating the duplicate expressions multiple times. However, there are some cases when normal-order evaluation becomes extremely useful when calculating logical expressions. 