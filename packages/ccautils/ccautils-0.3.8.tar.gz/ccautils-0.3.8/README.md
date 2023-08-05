[![Tests](https://github.com/ccdale/ccautils/workflows/Tests/badge.svg)](https://github.com/ccdale/ccautils/actions?workflow=Tests)
[![Codecov](https://codecov.io/gh/ccdale/ccautils/branch/master/graph/badge.svg)](https://codecov.io/gh/ccdale/ccautils)
# ccautils

a set of utilities for python3.6+ programs and scripts.

<a name=headdd></a>
* [Install](#install)
* [Development](#devel)
* [Testing](#testing)
* [Error Utilities](#errors)
* [Miscellaneous Utilities](#utils)
    * [Usage](#uusage)
* [File Utilities](#futils)
    * [Usage](#fusage)


<a name=install></a>
## [Install](#headdd)

Install for the user:
```
pip3 install ccautils --user
```

Install for a virtual environment:
```
pip install ccautils
```

<a name=devel></a>
## [Development](#headdd)

I use [poetry](https://python-poetry.org/) to manage these utilities.
Clone this repository and install `poetry`, then install the dependancies.

```
git clone https://github.com/ccdale/ccautils.git
cd ccautils
poetry install
```

<a name=testing></a>
## [Testing](#headdd)
To run the tests you must have `pytest`, `nox` and `poetry` installed.

install nox into your python user environment.
```
pip install nox --user
```

Run the tests with

```
nox -rs tests
```

Run the linter with

```
nox -rs lint
```

Run the console ask tests with

```
nox -rs tests -- -sm ask
```

<a name=errors></a>
## Error Utilities(#headdd)

See the [code](https://github.com/ccdale/ccautils) for how to use these
Exception helpers.


<a name=utils></a>
## [Miscellaneous Utilities](#headdd)

<a name=uusage></a>
### [Usage](#headdd)

```
import ccautils.utils as UT
```

<a name=menu></a>
* [addToString](#addtostring)
* [delimitString](#delimitstring)
* [makeDictFromString](#makedictfromstring)
* [askMe](#askme)
* [padStr](#padstr)
* [reduceTime](#reducetime)
* [displayValue](#displayvalue)
* [secondsFromHMS](#secondsfromhms)
* [hms](#hms)

<a name=addtostring></a>
### [addToString(xstr, xadd)](#menu)

[Code](https://github.com/ccdale/ccautils/blob/master/ccautils/utils.py#L26)

Returns a string with `xadd` appended to `xstr`.  If `xadd` is a list, all
`str` members of the list will be appended in order.

```
UT.addToString("hello", [" ", "world"])

> "hello world"
```

<a name=delimitstring></a>
### [delimitString(xstr, delimeter=" - ")](#menu)

[Code](https://github.com/ccdale/ccautils/blob/master/ccautils/utils.py#L49)

`xstr` can be a list or a string.  If it is a string, it is spit apart at
spaces and delimeted with `delimeter`.  If it is a list, each member is
delimeted with `delimeter`.

```
UT.delimitString(["bright", "world"], " ")

> "bright world"

UT.delimitString("I wandered lonely as an artichoke", ".")

> "I.wandered.lonely.as.an.artichoke"
```

<a name=makedictfromstring></a>
### [makeDictFromString(istr)](#menu)

[Code](https://github.com/ccdale/ccautils/blob/master/ccautils/utils.py#L64)

Constructs a dictionary from a string of parameters. Leading and trailing
whitespace is stripped.

`istr` should be in the form `someparam=somevalue,someotherparam=otherval`

```
UT.makeDictFromString("sparam=sval, soparam = soval")

> {"sparam": "sval", "soparam": "soval"}
```

<a name=askme></a>
### [askMe(q, default)](#menu)

[Code](https://github.com/ccdale/ccautils/blob/master/ccautils/utils.py#L89)

Requests input from the user.  Poses the question `q`. Returns the users
input or `default` if no input given.

```
UT.askMe("press 5, please", "8")

> press 5, please: 5
> 5
```

<a name=padstr></a>
### [padStr(xstr, xlen=2, pad=" ", padleft=True)](#menu)

[Code](https://github.com/ccdale/ccautils/blob/master/ccautils/utils.py#L101)

Returns `xstr` `pad`ded to the required length, either on the
left (`padleft` is True) or the right (`padleft` is False)

```
UT.padStr("23", 5, "0")

> "00023"
```

<a name=reducetime></a>
### [reduceTime(unit, secs)](#menu)

[Code](https://github.com/ccdale/ccautils/blob/master/ccautils/utils.py#L115)

Divides `secs` by `unit` returning a tuple of (`units`, `remainder`)

Raises a `ValueError` if `unit` is zero.

```
UT.reduceTime(3600, 3700)

> (1, 100)
```

<a name=displayvalue></a>
### [displayValue(val, label, zero=True)](#menu)

[Code](https://github.com/ccdale/ccautils/blob/master/ccautils/utils.py#L131)

Pluralises `label` if `val` > 1 or `val` is 0.

Will return an empty string if `val` == 0 and `zero` == True

```
UT.displayValue(12, "table")

> "12 tables"
```

<a name=secondsfromhms></a>
### [secondsFromHMS(shms)](#menu)

[Code](https://github.com/ccdale/ccautils/blob/master/ccautils/utils.py#L142)

converts HMS strings into integer seconds

```
UT.secondsFromHMS("01:01:23.43")
# 1 hour, 1 minute, 23 seconds + 0.43 second

> 3683
```

<a name=hms></a>
### [hms(secs, small=True, short=True, single=False, colons=False)](#menu)

[Code](https://github.com/ccdale/ccautils/blob/master/ccautils/utils.py#L214)

Convert `secs` to days, hours, minutes and seconds

if `small` is True then only return the higher values if they are > zero

if `short` is True then the labels are their short form

if `single` is True then the labels are single letters

if `colons` is True then the output is of the form `01:03:23`

```
UT.hms(67)

> "1 min and 7 secs"

UT.hms(67, short=False)

> "1 minute and 7 seconds"

UT.hms(67, small=False, short=False)

> "0 days, 0 hours, 1 minute and 7 seconds"

secs = 86400 + 7200 + 300 + 34
UT.hms(secs, single=True)

> "1d 2h 5m 34s"

secs = 345
UT.hms(secs, colons=True)

> "05:45"

secs = 86400 + 7200 + 300 + 34
UT.hms(secs, colons=True)

> "01:02:05:34"
```

<a name=futils></a>
## [File Utilities](#headdd)

<a name=fusage></a>
### [Usage](#headdd)

```
import ccautils.fileutils as FT
```

<a name=fmenu></a>
* [fileExists](#fileexists)
* [dirExists](#direxists)
* [dfExists](#dfexists)
* [makePath](#makepath)

<a name=fileexists></a>
### [fileExists(fqfn)](#fmenu)

[Code](https://github.com/ccdale/ccautils/blob/master/ccautils/fileutils.py#L30)

Tests for the existence of the fully-qualified (absolute) file name `fqfn`

Returns: `True` if `fqfn` exists, else `False`

```
fn = "/home/chris/output.csv"
if FT.fileExists(fn):
    # do something
else:
    raise(f"File {fn} does not exist")
```

<a name=direxists></a>
### [dirExists(fqdn)](#fmenu)

[Code](https://github.com/ccdale/ccautils/blob/master/ccautils/fileutils.py#L38)

Tests for the existence of the fully-qualified (absolute) directory name `fqdn`

Returns: `True` if `fqdn` exists, else `False`

```
dn = "/home/chris"
if FT.dirExists(dn):
    # do something
else:
    raise(f"Directory {dn} does not exist")
```

<a name=dfexists></a>
### [dfExists(fqdfn)](#fmenu)

[Code](https://github.com/ccdale/ccautils/blob/master/ccautils/fileutils.py#L46)

Tests to see if the file `fqdfn` exists, if not checks if `fqdfn` is
a directory that exists.

Returns: `True` if `fqdfn` exists, else `False`

```
dn = "/home/chris"
if FT.dfExists(dn):
    # do something
else:
    raise(f"File / Directory {dn} does not exist")
```

<a name=makepath></a>
### [makePath(pn)](#fmenu)

[Code](https://github.com/ccdale/ccautils/blob/master/ccautils/fileutils.py#L57)

Makes the path `pn` including any missing parent directories.  Does
nothing if path `pn` already exists.

Returns: None
```
dn = "/home/chris/appdir/subdir"
FT.makePath(dn)
```


[modeline]: # ( vim: set ft=markdown tw=74 fenc=utf-8 spell spl=en_gb mousemodel=popup: )
