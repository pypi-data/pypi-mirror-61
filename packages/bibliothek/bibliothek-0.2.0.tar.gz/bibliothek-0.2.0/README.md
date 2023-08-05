# Bibliothek

[![Build Status](https://travis-ci.org/ereyue/Bibliothek.svg?branch=master)](https://travis-ci.org/ereyue/Bibliothek) [![codecov](https://codecov.io/gh/ereyue/Bibliothek/branch/master/graph/badge.svg)](https://codecov.io/gh/ereyue/Bibliothek)

> 🏛 Managing Markup Files

## Example

```python
from typing import Tuple

from bibliothek.toc import ToC, Note

t = ToC(base='path/to/dir', file_pattern=r'^.+\.md')

@t.on_sort('path', 'to')
def _(note: Note):
    return note['created date']

@t.on_sort('path')
def _(note: Note):
    return note['last updated date']

@t.before_generate
def _() -> str:
    return '# ToC'

@t.after_generate
def _() -> str:
    return '_Generate by Bibliothek_'

@t.before_dir
def _(curr_dir: Tuple[str]) -> str:
    return f'## {curr_dir[-1]}' if len(curr_dir) > 0 else None

@t.after_dir
def _(curr_dir: Tuple[str]) -> str:
    return '\n'

@t.on_note
def _(note: Note) -> str:
    # path would be inserted into front matter and auto escaped
    return f'- [{note["title"]}]({note["path"]})'

print(t)
```
