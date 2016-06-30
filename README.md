# py3stringReplace

py3stringReplace replaces strings in text files based upon a user defined list.

## Key Features:

- Automates tedious replacements
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
py3stringReplace myscript.txt unlocalize.txt -d
py3stringReplace myscript.txt unlocalize.txt --debug
py3stringReplace myscript.txt unlocalize.txt --debug > replacementTable.txt
python py3stringReplace.py myscript.txt unlocalize.txt

To string replace files in a directory: (Windows)
Basic: 
>for /f "delims==" %i in ('dir *.txt /b') do py3stringReplace "%i" unlocalize.txt
To dynamicly rename files:
>for /f "delims==" %i in ('dir *.txt /b') do py3stringReplace "%i" unlocalize.txt -o "%~ni.unlocalized.txt"
For in-place modification:
>for /f "delims==" %i in ('dir *.txt /b') do py3stringReplace "%i" unlocalize.txt -nc

To string replace files in a directory: (OSX/Linux)
TODO: put stuff here
```

## Download+Install Guide:
```
Latest Version: 0.1
In Development: 0.2
```
1. Click [here](//github.com/gdiaz384/py3stringReplace/releases) or on "releases" at the top to download the latest version.
2. Extract py3stringReplace.exe from the archive of your OS/architecture.
3. Place py3stringReplace.exe in your enviornmental path
  - To find places to put it: >echo %path%
4. (optional) rename it to something memorable
5. create a text file of "match pair" values. See **Release Notes** and **replacementLists\unlocalize.txt** for additional information.
6. Refer to the **Example Usage Guide** above for usage.

## Release Notes:

- The replacementList.txt is made of of space-seperated match pairs.
- A reference replacementList.txt can be found at **replacementLists\unlocalize.txt**
- A "match pair" is "theStringToReplace" and "theReplacement"
- Examples:
  - They're they are   -means: theStringToReplace=They're, theReplacement=they are
  - Can't Can not   -means: theStringToReplace=Can't, theReplacement=Can not
  - "I cannot" I can    -means: theStringToReplace=I cannot, theReplacement=I can
- The match pair delimiter is the first space used or the first space after quoted text.
- Match pairs are case sensitive.
- To debug the syntax for entering match pairs use the --debug option.
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

- Python 3.4+
- To compile: pip, pyinstaller

## Compile(exe) Guide:

Remember to change the line ending back to not-broken-because-of-github if downloading from github directly using Notepad++ before attempting to compile. pyinstaller compatible encodings for .py files are ANSI and UTF-8 w/o BOM.

```
>python --version   #requires 3.4+
>pip install pyinstaller
>pyinstaller --version  #to make sure it installed
>pyinstaller --onefile py3stringReplace.py
```
Look for the output under the "dist" folder.

## License:
Pick your License: GPL (any) or BSD (any) or MIT/Apache
