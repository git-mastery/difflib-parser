# difflib-parser

Parser for Python's `difflib` output.

Built on top of <https://github.com/yebrahim/difflibparser/blob/master/difflibparser.py>

Key changes from above library:

1. Using generator pattern instead of using iterator pattern when iterating over diffs
2. Using `@dataclass` over generic dictionaries to enforce strict typing
3. Using type annotations for strict typing

## Getting started

```sh
pip install difflib-parser
```

```py
from difflib_parser import difflib_parser

parser = difflib_parser.DiffParser(["hello world"], ["hello world!"])
for diff in parser.iter_diffs():
  print(diff)
```

### `Diff` structure

```py
class DiffCode(Enum):
    SAME = 0
    RIGHT_ONLY = 1
    LEFT_ONLY = 2
    CHANGED = 3


@dataclass
class Diff:
    code: DiffCode
    line: str
    left_changes: List[int] | None = None
    right_changes: List[int] | None = None
    newline: str | None = None
```

## What is `difflib`?

A `difflib` output might look something like this:

```python
>>> import difflib
>>> print("\n".join(list(difflib.ndiff(["hello world"], ["hola world"]))))
- hello world
?  ^ ^^

+ hola world
?  ^ ^
```

The specifics of diff interpretation can be found in the [documentation](https://docs.python.org/3/library/difflib.html).

## Parsing `difflib`

There are concretely four types of changes we are interested in:

1. No change
2. A new line is added
3. An existing line is removed
4. An existing line is edited

Given that the last two cases operate on existing lines, they will always be preceded by `- `. As such, we need to handle them delicately.

If an existing line is removed, it will not have any follow-up lines.

If an existing line is edited, it will have several follow-up lines that provide details on the values that have been changed.

From these follow-up lines, we can further case the changes made to a line:

1. Only additions made (i.e. `"Hello world"` -> `"Hello world!"`)
2. Only removals made (i.e. `"Hello world"` -> `"Hllo world"`)
3. Both additions and removals made (i.e. `"Hello world"` -> `"Hola world!"`)

Each of them have their unique follow-up lines:

1. `-`, `+`, `?`

```python
>>> print("\n".join(list(difflib.ndiff(["hello world"], ["hello world!"]))))
- hello world
+ hello world!
?            +
```

2. `-`, `?`, `+`

```python
>>> print("\n".join(list(difflib.ndiff(["hello world"], ["hllo world"]))))
- hello world
?  -

+ hllo world
```

3. `-`, `?`, `+`, `?`

```python
>>> print("\n".join(list(difflib.ndiff(["hello world"], ["helo world!"]))))
- hello world
?    -

+ helo world!
?           +
```

As such, we have included them as separate patterns to process.
