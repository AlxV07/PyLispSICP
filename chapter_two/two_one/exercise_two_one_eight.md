### Exercise 2.18

Define a procedure `reverse` that takes a list as an argument and returns a list of the same elements in reverse order:
```
>>> reverse(list(1, 4, 9, 16, 25))
25, 16, 9, 4, 1
```

#### Answer:

```
def reverse(l):
    if mock_lisp_list_length(l) == 1:
        return car(l)
    else:
        return cons(reverse(cdr(l)), car(l))
```

My answer uses a simple recursive method to "generate" a list to repeatedly add the first element of the argument list `l` to end of the "result" list. 