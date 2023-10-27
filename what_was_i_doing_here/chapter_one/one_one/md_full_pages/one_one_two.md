## 1.1.2 Naming and the Environment

A critical aspect of a programming language is the means it provides for using names to refer to computational objects. We say that the name identifies a _variable_ whose _value_ is the object.

In Python, when we wish to name a thing, we simply type what we want its name to be, followed by an equals sign, followed by a value. For example, typing
```
>>> size = 2
```
would assign the integer 2 to the variable `size`. Once a variable has been assigned, we can get its value by referring to its name:
```
>>> size
2
>>> size * 5
10
```
Here are some more examples of assigning and using variables:
```
>>> pi = 3.14159
>>> radius = 10
>>> pi * (radius * radius)
314.159
>>> circumference = pi * radius * 2
>>> circumference
62.8318
```
Variables are our language's simplest means of abstraction, for they allow us to use simple names to refer to the results of compound operations, such as the `circumference` computed above. In general, computational objects may have very complex structures, and it would be extremely inconvenient to have to remember and repeat their details each time we want to use them. Indeed, complex programs are constructed by building, step by step, computational objects of increasing complexity. The interpreter makes this step-by-step program construction particularly convenient because name-object associations can be created incrementally in successive interactions.

It should be clear that the possibility of associating values with symbols and later retrieving them means that the interpreter must maintain some sort of memory that keeps track of the name-object pairs. This memory is called the _environment_ (more precisely the _global environment_, since we will see later that a computation may involve a number of different environments)<sup>9</sup>.

---

<sup>9</sup>Chapter 3 will show that this notion of environment is crucial, both for understanding how the interpreter works and for implementing interpreters.