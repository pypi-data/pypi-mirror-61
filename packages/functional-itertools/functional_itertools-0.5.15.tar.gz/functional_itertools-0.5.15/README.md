# functional_itertools
[![PyPI version](https://badge.fury.io/py/functional_itertools.svg)](https://badge.fury.io/py/functional_itertools)
[![Build Status](https://dev.azure.com/baoweiur521/baoweiur521/_apis/build/status/baowei521.functional_itertools?branchName=master)](https://dev.azure.com/baoweiur521/baoweiur521/_build/latest?definitionId=3&branchName=master)
[![codecov](https://codecov.io/gh/baowei521/functional_itertools/branch/master/graph/badge.svg)](https://codecov.io/gh/baowei521/functional_itertools)

## Overview
`functional_itertools` provides a set of classes which make it easy to chain iterables in a functional-programming style. These objects are based on the [`typing`](https://docs.python.org/3/library/typing.html) module:

| class | subclass of |
| --- | --- |
| `CIterable` | [`typing.Iterable`](https://docs.python.org/3/library/typing.html#typing.Iterable) |
| `CList` | [`typing.List`](https://docs.python.org/3/library/typing.html#typing.List) |
| `CSet` | [`typing.Set`](https://docs.python.org/3/library/typing.html#typing.Set) |
| `CFrozenSet` | [`typing.FrozenSet`](https://docs.python.org/3/library/typing.html#typing.FrozenSet) |
| `CDict` | [`typing.Dict`](https://docs.python.org/3/library/typing.html#typing.Dict) |

These classes:
* have access to all Python [built-in](https://docs.python.org/3/library/functions.html) functions relating to iterables, as well as those from [itertools](https://docs.python.org/3/library/itertools.html#module-itertools) and more.
* are [generic](https://docs.python.org/3/library/typing.html#typing.Generic), and thus can be type-checked.
* can be used with third-party iterables (e.g., [more-itertools](https://github.com/erikrose/more-itertools) via the [pipe](https://en.wikipedia.org/wiki/Pipeline_(Unix)) method.
* are easily extensible by virtue of being offered as simple classes (e.g., no multiple-inheritance, no metaclasses, etc).

## Examples

Given code like this:

```python
res = []
for x in range(10):
    y = 2 * x
    if 3 <= y <= 15:
        z = y - 1
        if z >= 6:
            res.append(z)
assert res == [7, 9, 11, 13]
```

You can reduce the complexity by using [generator expressions](https://www.python.org/dev/peps/pep-0289/) and [list comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions) instead of nesting:

```python
x = range(10)
y = (2*i for i in x)
z = (i for i in y if 3 <= i <= 15)
a = (i-1 for i in z)
res = [i for i in a if i >= 6]
```

You can further reduce the number of variables used by adopting a [functional programming](https://en.wikipedia.org/wiki/Functional_programming) style:

```python
x = range(10)
y = map(lambda i: 2*i, x)
z = filter(lambda i: 3 <= i <= 15, y)
a = map(lambda i: i-1, z)
res = list(filter(lambda i: i >= 6, a))
```

Finally, you can further reduce the number of variables used by using `CIterable`:

```python
from functional_itertools import CIterable

res = (
    CIterable.range(10)
    .map(lambda i: 2*i)
    .filter(lambda i: 3 <= i <= 15)
    .map(lambda i: i-1)
    .filter(lambda i: i >= 6)
    .list()
)
```

The edge in clarity scales as the number of operations increase. If you're a fan of this look and way of thinking then, [`functional_itertools`](https://github.com/baowei521/functional_itertools) is for you!

As mentioned, you have access to all functions from [itertools](https://docs.python.org/3/library/itertools.html#module-itertools) as  [functools](https://docs.python.org/3/library/functools.html#module-functools) as well, you can write:

```python
from functional_itertools import CIterable

res = (
    CIterable(["a", "b", "c", "d", "e", "f", "g"])
    .islice(2, 5)
    .map(lambda i: 2*i)
    .reduce(lambda i, j: "_".join([i, j]))
)
assert res == "cc_dd_ee"
```

## API reference (warning: implementation still a WIP!)

Please note that for `CDict` has 3 methods per listing, i.e., instead of `.all()`, it has `.all_keys()`, `.all_values()` and `.all_items()` instead.

| type | method | `CIterable` | `CList` | `CSet` | `CFrozenSet` | `CDict` |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| [built-in](https://docs.python.org/3/library/functions.html#built-in-functions) | [`self.all()`](https://docs.python.org/3/library/functions.html#all) | ☑ | ☑ | ☑ | ☑ | ☑ |
| [built-in](https://docs.python.org/3/library/functions.html#built-in-functions) | [`self.any()`](https://docs.python.org/3/library/functions.html#any) | ☑ | ☑ | ☑ | ☑ | ☑ |
| [built-in](https://docs.python.org/3/library/functions.html#built-in-functions) | [`self.enumerate(start=0)`](https://docs.python.org/3/library/functions.html#enumerate) | ☑ |  ☑ | ☑ | ☑ | ☑ |
| [built-in](https://docs.python.org/3/library/functions.html#built-in-functions) | [`self.filter(function)`](https://docs.python.org/3/library/functions.html#filter) | ☑ |  ☑ | ☑ | ☑ | ☑ |
| [built-in](https://docs.python.org/3/library/functions.html#built-in-functions) | [`self.len()`](https://docs.python.org/3/library/functions.html#len) | | ☑ | ☑ | ☑ | ☑ |
| [built-in](https://docs.python.org/3/library/functions.html#built-in-functions) | [`self.map(function, *iterables)`](https://docs.python.org/3/library/functions.html#map) | ☑ | ☑ | ☑ | ☑ | ☑ |
| [built-in](https://docs.python.org/3/library/functions.html#built-in-functions) | [`self.max(*, key, default)`](https://docs.python.org/3/library/functions.html#max) | ☑ | ☑ | ☑ | ☑ | ☑ |
| [built-in](https://docs.python.org/3/library/functions.html#built-in-functions) | [`self.min(*, key, default)`](https://docs.python.org/3/library/functions.html#min) | ☑ | ☑ | ☑ | ☑ | ☑ |
| [built-in](https://docs.python.org/3/library/functions.html#built-in-functions) | [`cls.range(stop)`  `cls.range(start, stop [,step])`](https://docs.python.org/3/library/functions.html#range) | ☑ | | | | |
| [built-in](https://docs.python.org/3/library/functions.html#built-in-functions) | [`self.reversed()`](https://docs.python.org/3/library/functions.html#reversed) | | ☑ | ☑ | ☑ | ☑ |
| [built-in](https://docs.python.org/3/library/functions.html#built-in-functions) | [`self.sum(/, start=0)`](https://docs.python.org/3/library/functions.html#sum) | | ☑ | ☑ | ☑ | ☑ |
| [built-in](https://docs.python.org/3/library/functions.html#built-in-functions) | [`self.tuple()`](https://docs.python.org/3/library/functions.html#func-tuple) | ☑ | ☑ | ☑ | ☑ | ☑ |
| [built-in](https://docs.python.org/3/library/functions.html#built-in-functions) | [`self.zip(*iterables)`](https://docs.python.org/3/library/functions.html#zip) | ☑ | ☑ | ☑ | ☑ | ☑ |
| [built-in](https://docs.python.org/3/library/functions.html#built-in-functions)<sup>1</sup> | [`self.dict()`](https://docs.python.org/3/library/functions.html#func-dict) | ☑ | ☑ | ☑ | ☑ |  |
| [built-in](https://docs.python.org/3/library/functions.html#built-in-functions)<sup>1</sup> | [`self.frozenset()`](https://docs.python.org/3/library/functions.html#func-frozenset) | ☑ | ☑ | ☑ | | ☑ |
| [built-in](https://docs.python.org/3/library/functions.html#built-in-functions)<sup>1</sup> | [`self.list()`](https://docs.python.org/3/library/functions.html#func-list) | ☑ | | ☑ | ☑ | ☑ |
| [built-in](https://docs.python.org/3/library/functions.html#built-in-functions)<sup>1</sup> | [`self.set()`](https://docs.python.org/3/library/functions.html#func-set) | ☑ | ☑ | | ☑ | ☑ |
| [built-in](https://docs.python.org/3/library/functions.html#built-in-functions)<sup>1</sup> | [`self.sorted(key=None, reverse=False)`](https://docs.python.org/3/library/functions.html#sorted) | ☑ | ☑ | ☑ | ☑ | ☑ |
| [`itertools`](https://docs.python.org/3/library/itertools.html) | [`cls.count(start[, step])`](https://docs.python.org/3/library/itertools.html#itertools.count) | ☑ | | | | |
| [`itertools`](https://docs.python.org/3/library/itertools.html) | [`self.cycle()`](https://docs.python.org/3/library/itertools.html#itertools.cycle) | ☑ | | | | |
| [`itertools`](https://docs.python.org/3/library/itertools.html) | [`cls.repeat(object[, times])`](https://docs.python.org/3/library/itertools.html#itertools.repeat) | ☑ | | | | |
| [`itertools`](https://docs.python.org/3/library/itertools.html) | [`self.accumulate(func)`](https://docs.python.org/3.6/library/itertools.html#itertools.accumulate)  (3.6, 3.7)  [`self.accumulate(func, *, initial=None)`](https://docs.python.org/3/library/itertools.html#itertools.accumulate) (3.8) | ☑ | | | | |
| [`itertools`](https://docs.python.org/3/library/itertools.html) | [`self.chain(*iterables)`](https://docs.python.org/3/library/itertools.html#itertools.chain) | ☑ | | | | |
| [`functools`](https://docs.python.org/3/library/functools.html) | [`self.reduce(function[, initializer])`](https://docs.python.org/3/library/functools.html#functools.reduce) | ☑ | ☑ | | | |
| [`functools`](https://docs.python.org/3/library/functools.html)<sup>2</sup> | [`self.reduce_as_iterable(function[, initializer])`](https://docs.python.org/3/library/functools.html#functools.reduce) | ☑ | ☑ | | | |
| [`pathlib`](https://docs.python.org/3/library/pathlib.html) | [`cls.iterdir(path)`](https://docs.python.org/3/library/pathlib.html#pathlib.Path.iterdir) | ☑ | | | | |

- <sup>1</sup> These methods return the [`functional_itertools`](https://github.com/baowei521/functional_itertools) classes, namely, `CIterable`, `CList`, etc.
- <sup>2</sup> This method wraps an iterable-yielding reduction in a `CIterable`.

## See also

- [Fn.py](https://github.com/kachayev/fn.py)
- [more-itertools](https://github.com/erikrose/more-itertools)
- [PyFunctional](https://github.com/EntilZha/PyFunctional)
- [pyrsistent](https://github.com/tobgu/pyrsistent/)
- [toolz](https://github.com/pytoolz/toolz)
