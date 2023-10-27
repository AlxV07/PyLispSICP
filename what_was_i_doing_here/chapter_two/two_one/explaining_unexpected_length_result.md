### Problem Reflection: Unexpected List `length` Result

Note: Methods starting with "mock" and the methods `car` & `cdr` were written by me and can be found somewhere in this project. They are imitations of the Scheme Lisp built-in methods, and they work in the same way as the originals.

Let us say we were to construct a Pair `x`, with two lists as its elements:

```
>>> x = cons(list(1, 2), list(3, 4)
>>> print(x)
1, 2, 3, 4
```

And if we were to use the `length` method on `x`:

```
>>> length(x)
3
```

This result at first does not make any sense. When we print out `x`, we can clearly see that four numbers, 1 through 4, are shown. However, when we created `x`, we did not create just one `list` with four elements; we created a Pair with two `list`s. But if we were counting each `list` as an element, the result of `length` should have been 2. So why is the result 3?

If we take a look into the `length` method, we see that it counts the "length" of a list by cdring down the elements and adding 1 for each time it does so. The flaw in this is that it does not check the `car` of the current `list` for any sub-elements when counting. Here is a step by step description of how the error occurred:

```
>>> length(x)
    First, check if cdr(x) is not null:
        cdr(x) != None -> (3, 4) != None -> True
    Its True, so return 1 plus the length of cdr(x):
        return 1 + length(cdr(x)) -> 1 + length((3, 4))
    Now find the length of (3, 4):
        cdr(x) != None -> 4 != None -> True
        return 1 + length(cdr(3, 4) -> 1 + length(4)
    And then find the length of 4:
        cdr(x) != None -> None != None -> False
        x != None -> 4 != None
        return 1
    Sum it up and we get:
        return 1 + 1 + 1 -> 3
3   
```