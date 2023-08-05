# intflags

Simplest way to create bit-flags.

```console
$ pip install intflags
```

## Usage

Create any number of intflags by using `intflags.get()`. You can create a union of any amount using the pipe (`|`) operator.

```python
>>> import intflags

>>> a, b, c = intflags.get(3)
>>> flags = a | b
>>> a in flags
True
>>> c in flags
False
```

Flags can be subtracted.

```python
# ...
>>> new_flags = flags - b
>>> b in new_flags
False
>>> new_flags == a
True
```

You could use classes as a pseudo-namespace.

```python
>>> class RegexFlags:
...     I, L, M, S, U, X = intflags.get(6)
```

Flags share an internal "namespace" ID to prevent accidental conflicts between sets. This allows multiple sets of flags to exist within the same class or module, without risk of accidentally creating a union between them.

```python
>>> x = intflags.get(1)
>>> y = intflags.get(1)
>>> x | y
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  ...
ValueError: Flags must share a namespace to create a union.
```
