# timework

[![PyPI](https://img.shields.io/pypi/v/timework?style=flat)](https://pypi.org/project/timework/)
[![Build Status](https://travis-ci.org/bugstop/timework-timeout-decorator.svg?branch=master;style=flat)](https://travis-ci.org/bugstop/timework-timeout-decorator)
[![Coverage Status](https://coveralls.io/repos/github/bugstop/timework-timeout-decorator/badge.svg?branch=master;style=flat)](https://coveralls.io/github/bugstop/timework-timeout-decorator?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c659ee01edaf404cbb346dbac8cefe38)](https://www.codacy.com/manual/bugstop/timework-timeout-decorator?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=bugstop/timework-timeout-decorator&amp;utm_campaign=Badge_Grade)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/timework?style=flat)](https://www.python.org)
[![platform](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-red?style=flat)](https://github.com/bugstop/timework-timeout-decorator)

Cross-platform python module to set run time limits <sup>(`timer`, `timeout`, `iterative`)</sup> as decorators.

## Install

```bash
pip install timework
```

## Usage

```python
import timework as tw
```

### timework.timer

**`timework.TimeError`** contains two parts:

- `TimeError.message` ***string***
  \<*inner function name*\>: \<*time used*\> seconds used
- `TimeError.result`
  result of the inner function

**Notice:** In **`timework.timer`** decorator, `timeout` is used to raise a `Error` **after** the inner function finishes. 
If you want to **stop** the function from running with a time limit, please use **`timework.limit`**.

```python
import logging

@tw.timer(logging.warning)
def timer_demo_a():
    i = 0
    while i < 2 ** 23:
        i += 1
    return i

@tw.timer(print, detail=True)
def timer_demo_b():
    i = 0
    while i < 2 ** 24:
        i += 1
    return i

@tw.timer(timeout=1)
def timer_demo_c():
    i = 0
    while i < 2 ** 25:
        i += 1
    return i
```
```python
a = timer_demo_a()
b = timer_demo_b()

try:
    c = timer_demo_c()
except tw.TimeError as e:
    print('error:', e.message)
    c = e.result

print(a, b, c)
```
```bash
WARNING:root:timer_demo_a: 0.496672 seconds used
START:  Tue Feb 18 15:06:45 2020
FINISH: Tue Feb 18 15:06:46 2020
timer_demo_b: 0.989352 seconds used
error: timer_demo_c: 1.9817 seconds used
8388608 16777216 33554432
```

### timework.limit

**`timework.TimeError`** only contains:

- `TimeError.message` *string*
  \<*inner function name*\>: \<*timeout*\> seconds exceeded

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
except tw.TimeError as e:
    print(e)
else:
    print('result:', s)

try:
    s = limit_demo(30)
except tw.TimeError as e:
    print(e)
else:
    print('result:', s)
```
```bash
result: 16
limit_demo: 3 seconds exceeded
```

### timework.iterative

**`timework.TimeError`** contains three parts:

- `TimeError.message` *string*
  \<*inner function name*\>.iterative_deepening: \<*timeout*\> seconds exceeded
- `TimeError.result`
  result of the last level of the iterative deepening search
- `TimeError.detail` *collections.deque*
  results of the upper levels *(number of historical records is set at `history`)*

**Notice:** Please make sure the **max-depth**-variable name is given at `key` <sup>(`key='max_depth'` by default)</sup> and its value should be an **integer**.

```python
@tw.iterative(3)
def iterative_demo_a(max_depth):
    i = 0
    while i < 2 ** max_depth:
        i += 1
    return max_depth, i

@tw.iterative(3, history=5, key='depth')
def iterative_demo_b(depth):
    i = 0
    while i < 2 ** depth:
        i += 1
    return depth
```
```python
try:
    s = iterative_demo_a(max_depth=10)
except tw.TimeError as e:
    print(e.message)
    print(e.result, e.detail)
else:
    print('result:', s)

try:
    s = iterative_demo_a(max_depth=25)
except tw.TimeError as e:
    print(e.message)
    print(e.result, e.detail)
else:
    print('result:', s)

try:
    s = iterative_demo_b(depth=25)
except tw.TimeError as e:
    print(e.message)
    print(e.result, e.detail)
else:
    print('result:', s)
```
```bash
result: (10, 1024)
iterative_demo_a.iterative_deepening: 3 seconds exceeded
(20, 1048576) deque([(20, 1048576)], maxlen=1)
iterative_demo_b.iterative_deepening: 3 seconds exceeded
20 deque([16, 17, 18, 19, 20], maxlen=5)
```

## License

MIT © <a href="https://github.com/bugstop" style="color:black;text-decoration: none !important;">bugstop</a>