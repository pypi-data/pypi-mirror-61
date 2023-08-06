pyreindent
==========
Tired of PEP8 tyranny? **pyreindent** is a Python script that allows you to switch between various Python indentation styles and clean up trailing spaces and tabs. For example, to switch from PEP8 tabs (four spaces) to hard tabs in all ``.py`` files in a folder ``~/foobar`` (without cleaning up any trailing symbols), simply type

	$ pyreindent.py -r -f soft4 -t hard ~/foobar

This will display a list of all files that the script has found, a summary of changes and ask if you want to apply the changes. By default, the files will be modified in-place, with original versions backed up at their original locations with ``~`` appended to the end of their original names. To switch back without storing any backups and remove any trailing spaces or tabs, type

	$ pyreindent.py -r -b "" -rt -f hard -t soft4 ~/foobar

The resulting code should be both consistently formatted and semantically equivalent to the input; if it is not, please submit a bug report. For details see the ''How it works'' section below.

Installation
------------

	$ pip install pyreindent

Features
--------
Help provided by the ``-h`` option lists all the features available:
```
$ ./pyreindent.py -h
usage: pyreindent.py [-h] -f {hard,soft4,soft2} -t {hard,soft4,soft2} [-r]
                     [-b postfix] [-rt] [-q] [-o output_file]
                     input_path

Freely switch between Python indentation styles

positional arguments:
  input_path            Location of the input

optional arguments:
  -h, --help            show this help message and exit
  -r, --recursive       Recursively find all .py files in the input path and
                        convert them
  -b postfix, --backup-postfix postfix
                        Back up unmodified input file(s) under their original
                        name(s) with this postfix. Set to an empty string to
                        suppress backups. Default: ~
  -rt, --remove-trailing
                        Remove any trailing tabs or spaces, leaving multiline
                        string literals intact
  -q, --quiet           Suppress all messages and prompts except for errors
  -o output_file, --output output_file
                        Output file name. Default: overwrite the original
                        file. Note: does not work with the -r option

required flags:
  -f {hard,soft4,soft2}, --from-tabs {hard,soft4,soft2}
                        Style of indentation to convert from
  -t {hard,soft4,soft2}, --to-tabs {hard,soft4,soft2}
                        Style of indentation to convert to
```
How it works
------------
To ensure the consistency of formatting, *pyreindent* splits Python code into [logical lines](https://docs.python.org/3/reference/lexical_analysis.html) (in *pyreindent* code they are called *blocks*) . A logical line can consist of several physical lines joined implicitly, explicitly or as triple-quoted literals. Semantically, indentation of a logical line is determined by the looking at its first physical line; indentation of subsequent physical lines is semantically meaningless and therefore arbitrary. This has led to a common practice of padding these subsequent lines with spaces to align the lines and improve readability. To preserve this alignment, *pyreindent* replaces exactly the same amount of indentation symbols at the beginning of each physical line in the block. For example, this snippet indented with four spaces
```python
def fun1():
    ''' Returns the following structure:
         ([1, 2], 3)
    '''
    a = [1, # a comment containing a bracket: ]
         2], \
        3
    # another comment
    return a
```
after reindentation with two spaces will look like this:
```python
def fun1():
  ''' Returns the following structure:
       ([1, 2], 3)
  '''
  a = [1, # a comment containing a bracket: ]
       2], \
      3
  # another comment
  return a
```
This is the general idea. In reality, things are a bit more complicated due to the existence of triple quoted string literals. On one hand, they can be used to define variables, in which case all leading tabs or spaces in the physical lines occurring between the triple quotes are meaningful: changing them would change the value of the variable. On the other hand, they are often used as [docstrings](https://www.python.org/dev/peps/pep-0257/) or multiline comments, in which case any leading tabs or white spaces are for readability only and are replaced with built-in formatting whenever the docstring is used (e.g. when help() is called on the function or module).

To keep both formatting and semantics consistent, *pyreindent* detects logical lines that contain triple quoted string literals and determines which of these two use cases has occurred. If the logical line starts with a triple quote, then the entirety of it is a string literal that is not assigned to any variables. In this case it is safe to reindent the logical line and *pyreindent* will do so. If the triple quote occurs in the middle of the logical line, then it might be meaningful. In this case *pyreindent* will keep the indentation of all physical lines occurring within triple quoted string literals definitions. For example, this snippet indented with four spaces
```python
def fun2():
    '''This is
       a comment
    '''
    a = ["""field 0
             of the list""",
         '''
         field 1 of the list
         ''']
    return a
```
after being reindented with two spaces will become
```python
def fun2():
  '''This is
     a comment
  '''
  a = ["""field 0
             of the list""",
       '''
         field 1 of the list
         ''']
  return a
```
Values returned by ``fun2`` in both snippets are identical.

Trailing tabs and spaces removal works similarly: *pyreindent* will not remove trailing symbols occurring within a triple quote string definition that can affect code execution.

Known limitations
-----------------
- Comments or dosctrings that use [string prefixes](https://docs.python.org/3/reference/lexical_analysis.html#grammar-token-stringprefix) will be interpreted as possibly affecting the code execution and their indentation will be kept intact.
- Sequences of three quotes in which the first quote is escaped (e.g. ``\'''``) will be mistaken for a boundary of a string literal. Consequently, an attempt to reindent the following valid Python script
	```python
	a = '\'''
	print(a)
	```
	will result in a ``ValueError``.

