# Version

A version is a string that matches the following regex:
```python
"^v?(\d+)(?:.(\d+))?(?:.(\d+))?(?:-?(a|b|rc)(\d+)?)?$"
```
E.g. v0.11.22-rc3.

#### Assumptions
1. v1 is equivalent to v1.0.0
2. A version without a candidate is greater than its candidate counterpart
   e.g. v2 > v2rc > v2b > v2a

## Installation

```
pip install rtimbo-version
```

## Usage

```python
>>> from version import Version
>>> v1 = Version("v0.2.11rc3")
>>> v1.major
0
>>> v1.minor
2
>>> v1.patch
11
>>> v1.candidate
'rc'
>>> v1.candidate_number
3
>>> v1 > 0
True
>>> v1 > 1
False
```

```python
>>> available_versions = [
...     Version("v0.9.2b"),
...     Version("v0.9.1"),
...     Version("v0.9.2"),
...     Version("v2.9.3rc1"),
...     Version("3.0.0"),
...     Version("v0.9.2a1"),
...     Version("v0.9.2rc1"),
...     Version("1.0.0"),
...     Version("2.5.7"),
...     Version("v0.9.2rc3")]
>>> 
>>> print('\n'.join([str(version) for version in sorted(available_versions)]))
v0.9.1
v0.9.2a1
v0.9.2b0
v0.9.2rc1
v0.9.2rc3
v0.9.2
v1.0.0
v2.5.7
v2.9.3rc1
v3.0.0

```