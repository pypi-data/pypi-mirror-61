
choba
=====

Wrapper to simplify calls to python `unittest`,
[`coverage`](https://pypi.org/project/coverage/) and
[`webtest`](https://pypi.org/project/WebTest/).

## Installation

```sh
$ pip install choba
$ choba -h
Usage: choba [-hl] [-s <submodule>] [-f <filter>] <dir>
```

## Usage

```sh
$ export PYTHONPATH=`pwd`/src
$ choba <your_test_directory>
```

The call will internally process `./.coveragerc`. HTML and
Cobertura-compatible XML code coverage report are automatically
generated.


##### sample configuration `.coveragerc`:

```txt
[run]
source = src
omit =
    src/myproject/__init__.py
    src/myproject/daemon.py
    */__main__.py

[html]
directory = docs/coverage

[xml]
output = docs/coverage/coverage.xml

[report]
exclude_lines = if __name__ ==
```

In choba, [branch coverage](https://coverage.readthedocs.io/en/coverage-5.0.3/branch.html)
is always true regardless what you put in the configuration file.


##### sample module:

```python
# ./src/myproject/common/utils.py

import re


def flatten(text):
    """
    Remove line breaks and trim.
    """
    text = re.sub(r'[\r\n\t]+', ' ', text)
    text = re.sub(r'  +', ' ', text)
    return text.strip()
```


##### sample test:

```python
# ./tests/common/utils.py

import unittest


# test against ./src/myproject/common/utils.py
from myproject import utils


class TestCommon(unittest.TestCase):

    def test_myfunc(self):
        text = "\raaa\nbbb\t\r\n"
        self.assertEquals("aaa bbb", utils.flatten(text))
```
