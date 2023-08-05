# what-the-diff
*"What the diff???"*

unix diff implementation in python

## Usage
```python
from what_the_diff import diff
old = "Hello world\nHello hell"

new = "Hello Heaven\nHello world\nHello hall\nHello waddldo"

lines_new = new.split('\n')
lines_old = old.split('\n')


removed, added, updated = diff(old, new)

for i in removed:
    print(i.format())
for i in added:
    print(i.format())
for i in updated:
    print(i.format())

#prints
#0,1d1
#< Hello hell
#0a1,1
#> Hello Heaven
#2a3,4
#> Hello hall
#> Hello waddldo
#1c2
#< Hello hell
#---
#> Hello hall
#### With colors

```


## Install

```bash
pip install what-the-diff
```