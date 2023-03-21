### Exercise 2.17
Define a procedure `last_pair` that returns the last element of a given (non-empty) list:

For example:
```
>>> last_pair(mock_lisp_list(23, 72, 149, 34))
34
```

#### Answer:

```
def last_pair(x):
    return mock_lisp_list_ref(x, mock_lisp_list_length(x) - 1)
```
My solution uses the procedures `list_ref` and `length` to "get" the item at the index of length of the list `x` minus 1; i.e. the last element of the list. 