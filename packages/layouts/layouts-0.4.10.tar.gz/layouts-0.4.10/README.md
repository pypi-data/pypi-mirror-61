# HID-IO layouts Python API

This is the Python API for the HID-IO [layouts](https://github.com/hid-io/layouts) repository.
By default, the API will download the latest version of the layouts git repository to use that as a cache.

The purpose of this API is to acquire and merge the JSON HID layouts.
With some additional helpers to deal with string composition.

[layouts](https://pypi.org/project/layouts/) is also available on PyPi.
```bash
pip install layouts
```

[![GitHub Action Status](https://github.com/hid-io/layouts-python/workflows/Python%20package/badge.svg)](https://github.com/hid-io/layouts-python/actions)
[![PyPI version](https://badge.fury.io/py/layouts.svg)](https://badge.fury.io/py/layouts)

[![Visit our IRC channel](https://kiwiirc.com/buttons/irc.freenode.net/hid-io.png)](https://kiwiirc.com/client/irc.freenode.net/#hid-io)


## Usage

Some basic usage examples.


### List Layouts

**GitHub Cache**

```python
import layouts

mgr = layouts.Layouts()
print(mgr.list_layouts()
```

**Local Cache**

```python
import layouts

layout_dir = "/tmp/mylayouts/layouts"
mgr = layouts.Layouts(layout_path=layout_dir)
print(mgr.list_layouts()
```


### Retrieve Layout

```python
import layouts

mgr = layouts.Layouts()
layout = mgr.get_layout('default')

print(layout.name()) # Name of merged layout
print(layout.json()) # Fully merged JSON dict
print(layout.locale()) # Tuple (<USB HID locale code>, <name>)
```


### Composition Example

```python
import layouts

mgr = layouts.Layouts()
layout = mgr.get_layout('default')

input_str = "Hello World!"
print(layout.compose(input_str))

# Only use code clears when necessary (blank USB packet)
print(layout.compose(input_str, minimal_clears=True))
```


### Codes for C-Style Defines

```python
import layouts
import layouts.emitter

mgr = layouts.Layouts()
layout = mgr.get_layout('default')

# Returns a list of list of tuples
# Each type of code has a pre-defined (configurable) prefix
# [<keyboard codes>, <led codes>, <system control codes>, <consumer codes>]
# (<name>, <code>)
# Useful for:
# #define KEY_A 0x04
print(layouts.emitter.basic_c_defines(layout))
```

