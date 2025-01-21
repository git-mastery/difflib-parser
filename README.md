# diffparser

Parser for Python's difflib. Built on top of https://github.com/yebrahim/difflibparser/blob/master/difflibparser.py

Key changes made to the above library:

1. Using generator pattern instead of using iterator pattern when iterating over diffs
2. Using more `@dataclass` over generic dictionaries to enforce strict typing
3. Using type annotations for strict typing
