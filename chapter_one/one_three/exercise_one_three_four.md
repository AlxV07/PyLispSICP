### Exercise 1.3.4
Suppose we define the procedure
```
>>> def f(g):
...    return g(2)
```
Then we have
```
>>> def square(x)
...     return x * x
...
>>> f(square())
4
>>> f(lambda x: x * (x + 1)
6 
```
What happens if we (perversely) ask the interpreter to evaluate the expression `f(f)`? Explain.

#### Answer:

```
f(f())
f( f(2) )
f( f( 2(2) ))
TypeError: 'int' object is not callable
```
First, the outer function `f` will call its argument (the inner `f`), and pass the argument of `2` to it. Then, the inner `f` function will attempt to call its argument (the `int` `2`), but will find that an integer cannot be called; resulting in an error.

