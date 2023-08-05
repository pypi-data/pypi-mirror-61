# beancount-syspath

Manipulate `sys.path` from within the beancount file. This is a plugin for
[Beancount](http://furius.ca/beancount/
), a double-entry bookkeeping computer language.

## Installation

Install via pip

```shell
pip install beancount-syspath
```

## Usage

Prepend list of paths

```beancount
plugin "beancount_syspath.prepend" "[
    'some/dir',
    'other/dir'
]"
```

or append list of paths

```beancount
plugin "beancount_syspath.append" "[
    'some/dir',
    'other/dir'
]"
```

Place the directive before other plugin loading ones, so they can make use of the updated `sys.path`.

The config value is a python list literal, which will be evaluated by `ast.literal_eval`, and then
prepended/appended to `sys.path`.
