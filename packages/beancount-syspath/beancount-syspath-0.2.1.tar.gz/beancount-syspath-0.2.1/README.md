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
plugin "beancount_syspath.plugin" "{
    'append': ['some/dir', 'other/dir'],
    'prepend': ['some/dir', 'other/dir'],
}"
```

Note: Place the directive before other plugin loading ones, so they can make use of the updated `sys.path`.

### Configuration
The config value is a python dict literal, contains the following keys

| Key | Type | Optional | Default | Meaning |
|:-:|:-:|:-:|:-:|:-:|
| `append` | `List[str]` | yes | `[]` | Append the list of path to `sys.path` |
| `prepend` | `List[str]` | yes | `[]` | Prepend the list of path to `sys.path` |
| `normalize_to_root` | `bool` | yes | `True` | If the path is relative, it is considered to be relative to the root beancount file, and normalized to absolute path before adding to `sys.path`. |
