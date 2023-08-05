# Ratus

[![Documentation Status](https://readthedocs.org/projects/ratus/badge/?version=latest)](https://ratus.readthedocs.io/en/latest/?badge=latest)
[![CircleCI](https://circleci.com/gh/nick96/ratus.svg?style=svg)](https://circleci.com/gh/nick96/ratus)
[![PyPI](https://img.shields.io/pypi/v/ratus)](https://pypi.org/project/ratus/)

Ratus is a simple expression language that can be used to easily extend Python
applications with an embedded expression language. Evaluating basic expressions
is as simple as:

``` python
from ratus import Evaluator

evaluator = Evaluator()
evaluator.evaluate("1 + 1") # => 1
evaluator.evaluate("1 > 1") # => False
evaluator.evaluate("if(1 < 2, 10, 5)") #  => 5
```

For more information, please check out the
[docs](https://ratus.readthedocs.io/en/latest/)

## What's in a name?

When I first started this project I did a bit of research around parsing
techniques as this is really the most complex part. One idea that that really
stuck out to me was [packrat](https://bford.info/packrat/) parsing. This
technique allows for linear time parsing, as opposed to the usual exponential
time of backtracking parsing.

Currently packrat parsing isn't implemented for `ratus` but I'm working on it!

## Roadmap

### `v1.0.0`

- [ ] Fully document all features
  - [ ] API
  - [ ] Grammar
- [ ] Fix known bugs
  - [ ] Don't require functions to be the root of an expression
    - e.g. ``pow(2, 2) + 1`` should be allowed
