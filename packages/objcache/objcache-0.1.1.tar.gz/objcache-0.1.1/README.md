
[![](https://codecov.io/gh/nickderobertis/obj-cache/branch/master/graph/badge.svg)](https://codecov.io/gh/nickderobertis/obj-cache)

# obj-cache

## Overview

Simple Redis-like interface to storing arbitrary Python objects. A high-level wrapper around ZoDB.

## Getting Started

Install `objcache`:

```
pip install objcache
```

A simple example:

```python
from objcache import ObjectCache

cache = ObjectCache('cache.zodb', ('a', 'b'))
cache.store(5)

# Later session
cache = ObjectCache('cache.zodb', ('a', 'b'))
result = cache.get()
print(result)
5
```

## Links

See the
[documentation here.](
https://nickderobertis.github.io/obj-cache/
)

## Author

Created by Nick DeRobertis. MIT License.