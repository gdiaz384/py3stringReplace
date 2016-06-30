# py3stringReplace

py3stringReplace replaces strings in text files based upon a user defined list

## Key Features:

- Automates tedeious replacements
- Command Line Interface (CLI)
- Precompiled binaries for Windows.
- Scripting friendly
- Cross platform

## Example Usage Guide:

Syntax: py3stringReplace [-h] [-o output.txt] [-nc] [-sm] [-d] inputFile.txt replacementList.txt
Note: [ ] means optional.

```
py3stringReplace -h
py3stringReplace --help
py3stringReplace myscript.txt unlocalize.txt
py3stringReplace myscript.txt unlocalize.txt -o myscript.unlocalized.txt

Advanced Usage:
py3stringReplace myscript.txt unlocalize.txt --output myscript.unlocalized.txt
py3stringReplace myscript.txt unlocalize.txt -nc
py3stringReplace myscript.txt unlocalize.txt --noCopy
py3stringReplace myscript.txt unlocalize.txt -sm
py3stringReplace myscript.txt unlocalize.txt --showMatching
py3stringReplace myscript.txt unlocalize.txt -sm > matching.txt
py3stringReplace myscript.txt unlocalize.txt --showMatching > matching.txt
py3stringReplace myscript.txt unlocalize.txt --debug
py3stringReplace myscript.txt unlocalize.txt --debug > replacementTable.txt
python py3stringReplace.py myscript.txt unlocalize.txt

To string replace files in a directory: (Windows)
Basic: 
>for /f "delims==" %i in ('dir *.txt /b') do py3stringReplace "%i" unlocalize.txt
For dynamic rename
>for /f "delims==" %i in ('dir *.txt /b') do py3stringReplace "%i" unlocalize.txt -o "%~ni.unlocalized.txt"
or for in-place modification:
>for /f "delims==" %i in ('dir *.txt /b') do py3stringReplace "%i" unlocalize.txt -nc

To string replace files in a directory: (OSX/Linux)
TODO: put stuff here
```

## Download:
```
Latest Version: 0.1.0
In Development: 0.1.1
```
Click [here](//github.com/gdiaz384/py3stringReplace/releases) or on "releases" at the top to download the latest version.

## Release Notes:

- The replacementList.txt is made of of space-seperated match pairs.
- A reference replacementList.txt can be found at replacementLists\unlocalize.txt
- A "match pair" is "theStringToReplace" and "theReplacement"
- Examples:
  - They're they are   -means: theStringToReplace=They're, theReplacement=they are
  - Can't Can not   -means: theStringToReplace=Can't, theReplacement=Can not
  - "I cannot" I can    -means: theStringToReplace=I cannot, theReplacement=I can
- The match pair delimiter is the first space used or the first space after quoted text.
- Match pairs are case sensitive.
- The syntax for replacementList.txt is as follows:
  - The first line is ignored.
  - The last line must be an empty line. The list may not end in a match pair.
  - Lines that start with # indicate a comment.
  - Empty lines are ignored.
  - Whitespace is ignored.
  - Non-empty lines with only whitespace are ignored.
- Replacements are performed out of order. The order of match pairs in replacementTable.txt is not important.
- The output file will be UTF-8 encoded. To change the encoding, use Notepad++.

## Dependencies
```
Python 3.4+
To compile: pip, pyinstaller
```

## Compile(exe) Guide:

```
>python --version   #requires 3.4+
>pip install pyinstaller
>pyinstaller --version  #to make sure it installed
>pyinstaller --onefile py3stringReplace.py
```
Look for the output under the "dist" folder.

## License:
Pick your License: GPL (any) or BSD (any) or MIT/Apache
