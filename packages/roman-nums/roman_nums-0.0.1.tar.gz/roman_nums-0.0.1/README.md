# roman-nums
Python library to work with roman numbers.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install roman-nums.

```bash
pip install roman-nums
```

## Base usage

```python
>>> from roman_nums import to_roman, from_roman
...
>>> to_roman(154)
CLIV
>>> from_roman('MCCCXLVI')
1346
```
## Work with validation

```python
>>> from roman_nums.utils import rn_validator
...
>>> rn_validator('XLIV')
True
>>> rn_validator('XLIVV')
False
```

## Work with texts
Find roman and arabic numbers in text. Convert them.

```python
>>> from roman_nums.utils import RText
...
text = """
In 1066, Norman troops <...>.
In the XII century, England conquered Wales, and at the beginning of the XVIII century <...>.
"""

>>> worker = RText(text)
>>> worker.from_roman()
In 1066, Norman troops <...>.
In the 12 century, England conquered Wales, and at the beginning of the 18 century <...>.

>>> worker.to_roman()
In MLXVI, Norman troops <...>.
In the XII century, England conquered Wales, and at the beginning of the XVIII century <...>.

>>> worker.rnb()    # Will find all roman numbers
['XII', 'XVIII']

>>> worker.nb()     # Will find all arabic numbers
[1066]
```