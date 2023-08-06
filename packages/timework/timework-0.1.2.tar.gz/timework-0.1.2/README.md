# timework

[![PyPI](https://img.shields.io/pypi/v/timework)](https://pypi.org/project/timework/)
[![python](https://img.shields.io/badge/python-3-blue)](https://www.python.org)
[![Build Status](https://travis-ci.org/bugstop/timework-pylib.svg?branch=master)](https://travis-ci.org/bugstop/timework-pylib)
[![Coverage Status](https://coveralls.io/repos/github/bugstop/timework-pylib/badge.svg?branch=master)](https://coveralls.io/github/bugstop/timework-pylib?branch=master)
[![codebeat badge](https://codebeat.co/badges/3d301de4-a88c-4a8a-9712-373fab3126e4)](https://codebeat.co/projects/github-com-bugstop-timework-pylib-master)

A package used to set time limits.

## Install

```
pip install timework
```

## Usage

```python
import timework as tw
import logging

r = tw.ResultHandler(5)
```

### timework.timer

```python
@tw.timer(r)
def timer_demo_a():
    i = 0
    while i < 2 ** 23:
        i += 1
    return i

@tw.timer(r, out=print)
def timer_demo_b():
    i = 0
    while i < 2 ** 24:
        i += 1
    return i

@tw.timer(r, out=logging.warning)
def timer_demo_c():
    i = 0
    while i < 2 ** 25:
        i += 1
    return i
```
```python
timer_demo_a()
timer_demo_b()
timer_demo_c()
print(r.value)
```
```
timer_demo_b: 0.991348 seconds used
WARNING:root:timer_demo_c: 1.96977 seconds used
deque([0.5051665306091309, 0.9913477897644043, 1.96976900100708], maxlen=5)
```

### timework.limit

```python
@tw.limit(3)
def limit_demo(m):
    i = 0
    while i < 2 ** m:
        i += 1
    return i
```
```python
try:
    s = limit_demo(4)
except Exception as e:
    print(e, end='\n\n')
else:
    print(s)

try:
    s = limit_demo(30)
except Exception as e:
    print(e, end='\n\n')
else:
    print(s)
```
```
16
limit_demo: 3 seconds exceeded
```

### timework.iterative

```python
@tw.iterative(r, 1)
def iterative_demo(max_depth):
    i = 0
    while i < 2 ** max_depth:
        i += 1
    return max_depth, i
```
```python
try:
    r.clear()
    iterative_demo(max_depth=10)
except Exception as e:
    print(e)
finally:
    print(r.value, end='\n\n')

try:
    r.clear()
    iterative_demo(max_depth=25)
except Exception as e:
    print(e)
finally:
    print(r.value, end='\n\n')
```
```
deque([(6, 64), (7, 128), (8, 256), (9, 512), (10, 1024)], maxlen=5)

iterative_deepening: 1 seconds exceeded
deque([(15, 32768), (16, 65536), (17, 131072), (18, 262144), (19, 524288)], maxlen=5)
```

## License

MIT © <a href="https://github.com/bugstop" style="color:black;text-decoration: none !important;">bugstop</a>