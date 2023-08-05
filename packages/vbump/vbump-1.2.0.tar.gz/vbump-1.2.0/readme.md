# vbump

vbump is yet another Python package version bump tool. Unlike others, e.g. [bumpversion](https://github.com/peritus/bumpversion), [changes](https://github.com/michaeljoseph/changes), etc., it aims to just do the obvious thing without any unneeded configuration or requirements.

It is a simple < 100 LOC package which has no dependencies and is compatible with Python 2.7 and 3.5+.


## Prerequisites

- A SemVer version string specified in either **setup.py** or **\_\_version\_\_.py**.
- If \_\_version\_\_.py exists that will be used; the expected fromat is `VERSION = "1.0.0"`.
- Otherwise setup.py will be used.


## Installing

`$ pip install vbump`


## Usage

```
usage: vbump [-h] [--patch | --minor | --major] [--test]

Yet another Python version bumper

optional arguments:
  -h, --help  show this help message and exit
  --patch     increment patch level
  --minor     increment minor level
  --major     increment major level
  --test      shows result of version bump with writing
```

## Examples

- `vbump --major` to increment from version `1.0.0` to `2.0.0`.
- `vbump --minor --test` to preview updating from version `1.0.0` to `1.1.0`.
- if no arguments are specified the current version will be printed without changes.
