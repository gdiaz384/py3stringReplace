# py3stringReplace

py3stringReplace replaces strings in text files based upon a user defined list.

## Key Features:

- Automates tedious ctrl+f replacements.
- Command Line Interface (CLI).
- Precompiled binaries for x64 Windows.
- Scripting friendly.
- Cross platform (Python 3).
- Supports various [character encodings](//docs.python.org/3.4/library/codecs.html#standard-encodings) and [error handing](//docs.python.org/3.4/library/codecs.html#error-handlers).
    - For direct conversions from one character encoding schema to another, use: `py3iconv.py`

## Example Usage Guide:

Syntax: `py3stringReplace [-h] [-o output.txt] [-nc] [-sm] [-d] inputFile.txt replacementList.txt`

Notes:
- `[ ]` means optional.
- Flags that only specify encoding and error handling options were not included above. See Advanced Usage below.

```
Syntax help:
py3stringReplace -h
py3stringReplace --help

Basic Usage:
py3stringReplace myscript.txt unlocalize.txt
py3stringReplace myscript.txt unlocalize.txt -o myscript.unlocalized.txt
py3stringReplace myscript.txt unlocalize.txt --output myscript.unlocalized.txt
py3stringReplace myscript.txt unlocalize.txt -nc
py3stringReplace myscript.txt unlocalize.txt --noCopy

Advanced Usage:
py3stringReplace myscript.txt unlocalize.txt -sm
py3stringReplace myscript.txt unlocalize.txt --showMatching
py3stringReplace myscript.txt unlocalize.txt -sm > matching.txt
py3stringReplace myscript.txt unlocalize.txt --showMatching > matching.txt
py3stringReplace myscript.txt unlocalize.txt -d
py3stringReplace myscript.txt unlocalize.txt --debug
py3stringReplace myscript.txt unlocalize.txt --debug > replacementTable.txt
py3stringReplace myscript.txt unlocalize.txt -e utf-8
py3stringReplace myscript.txt unlocalize.txt -e windows-1251
py3stringReplace myscript.txt unlocalize.txt --encoding windows-1251
py3stringReplace myscript.txt unlocalize.txt -ce windows-1251
py3stringReplace myscript.txt unlocalize.txt --consoleEncoding utf-8
py3stringReplace myscript.txt unlocalize.txt -e windows-1251 -ce utf-8 -sm
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

## Replacement List Syntax:

- `replacementList.txt` is made up of line seperated `match pairs`
- A `match pair` specifies `theStringToReplace` and `theReplacement`.
- The match pair delimiter is the first space or, in the case of quoted text, the first space after quoted text.
- To include quotation marks in `theReplacement` text, use exactly four of them.
- A `replacementList.txt` example can be found at `replacementLists\unlocalize.txt`

match pair | theStringToReplace | theReplacement
--- | --- | ---
They're they are | They're | they are
Can't Cannot | Can't | Cannot
"I cannot" I can | I cannot | I can
!? ? | !? | ?
"See ya." See you. | See ya. | See you.
"Master Shuga" Shuga-sama | Master Shuga | Shuga-sama
"Юки Нагато" Нагато Юки | Юки Нагато | Нагато Юки 
咲月 Satsuki| 咲月 | Satsuki
Satsuki さつき | Satsuki  | さつき
colour color | colour | color
check cheque | check | cheque
one two three | one | two three
"one two" three | one two | three
" one two" " three " | " one two" | " three "

- Match pairs are case sensitive.
- To debug the syntax for entering match pairs use the --debug option.
    - `py3stringReplace myscript.txt unlocalize.txt -d > pairs.txt`
- The syntax for replacementList.txt is unforgiving and as follows:
    - The first line is ignored.
    - The last line must be an empty line. The list may not end in a match pair.
    - Lines that start with `#` indicate a comment.
    - Empty lines are ignored.
    - Non-empty lines with only whitespace are ignored.
    - Whitespace outside of quotation marks is ignored.
    - Whitespace within quotation marks `"` is preserved **if** it is also within two characters that are not whitespace. Otherwise, it will be ignored.
    - The order of match pairs in replacementList.txt is not important, at least in Python <=3.6. It might be for Python 3.7+.
    - Quotations marks `"` are overloaded in order to provide an option for replacements to include them.
        - Including 2x quotation marks means: split at the first space after the second quotation mark. Ignore all quotation marks.
        - Including 4x quotation marks means: split where there are two quotation marks and a space in the middle `" "` Preserve all quotation marks.

## Release Notes:

- Replacements are performed out of order. To perform ordered replacements, use a second replacement list.
- Ordered replacements might be possible/happening in Python >=3.7 due to dictionaries becoming ordered, but that has not been tested.
- If downloading a `replacementList.txt` from github directly instead of using a release.zip, remember to change the line ending back to not-broken before attempting to use it by using Notepad++ or VS Code (if applicable).

### Dealing with character encoding:

- Computers only understand 1's and 0's. The letter `A` is ultimately a series of 1's and 0's. How does a computer know to display `A`, `a`, `à`, or `あ`? By using a standardized encoding schema.
- Due to various horrible and historical reasons, there is no way for computers to deterministically detect arbitrary character encodings from files. Automatic encoding detection is a lie. Those just use heuristics which can and will fail catastrophically eventually.
- Thus, the encodings for the text files and the console must be specified at runtime, or something might break.
- Supported encodings: [docs.python.org/3.4/library/codecs.html#standard-encodings](//docs.python.org/3.4/library/codecs.html#standard-encodings) Common encodings:
    - `utf-8` - If at all possible, please only use `utf-8`, and use it for absolutely everything.
    - `shift-jis` - Required and many Japanese text files, visual novels, games, archives, and media in general.
    - `cp437` - This is the old IBM code page for English that Windows with an English locale often uses by default. Thus, this is very often the encoding used by cmd.
    - `cp1252` - This is the code page for western european languages that Windows with an English locale often uses by default. Thus, this is very often the encoding used by cmd.
- Files will be read/written as `utf-8` encoded by default. To change the encoding use the `-e` option.
- To use a different output encoding than input encoding, use `--outputEncoding` (`-oe`).
    - Combined with an empty replacement list, this can convert between different formats similar to the unix `iconv` tool, although this is very hacky. 
    - Instead, use `py3iconv.py` for direct conversions. It has a simpler interface as well.
- Output to stdout/console is `utf-8` formatted by default. To change the console encoding use the -ce option.
- `replacementList.txt` is read as `utf-8` by default. To change the encoding use the `-rle` option.
- Due to console limitations, consider using [Notepad++](//notepad-plus-plus.org/download) or VS Code to change the input to `utf-8` when debuging.
    - On newer versions of Windows (~Win 10 1809+), consider changing the console encoding to native `utf-8`. There is a checkbox for it in the change locale window.
    - On older versions of Windows, attempting to use `utf-8` via the related code page will make the console crash.
- To print the currently active code page on Windows, open a command prompt and type `chcp`
- Some character encodings cannot be converted to other encodings. When such errors occur, use the following error handling options:
    - [docs.python.org/3.4/library/codecs.html#error-handlers](//docs.python.org/3.4/library/codecs.html#error-handlers), and [More Examples](//www.w3schools.com/python/ref_string_encode.asp).
    - The default error handler for input files is `strict` which means 'crash the program if the encoding specified does not match the file perfectly'.
    - The default error handler for the output file is `namereplace` and it requires Python 3.5+. For Python <=3.4, the default is `backslashreplace`
        - These obnoxious error handlers were chosen to make it obvious that there were conversion errors but also not crash catastrophically and to make it easy to do ctrl+f replacements to fix any problems.
        - If there are more than one or two such errors per file, then the chosen source file encodings are probably incorrect.
- If the `chardet` library is available (Python 3.7+), it can be used to try to detect the character encoding of files via heuristics, but that is obviously very error prone.
    - To make it available: `pip install chardet`
    - The following library that actually implements chardet must also be present: `resources/dealWithEncoding.py`
    - If both of the above are not available, then everything will be assumed to be `utf-8` if not otherwise specified.

## Advanced Usage Guide:

- The idea is to type `fix mysubs.ass` or `fix *` and have the rest be automatic.
- Make sure py3stringReplace.exe is in `%path%` and put the following in a file called `C:\Users\User\fix.bat`

```
@echo off
setlocal

if /i "%~1" equ "" (goto usageHelp)
if /i "%~1" equ "?" (goto usageHelp)
if /i "%~1" equ "/?" (goto usageHelp)
if /i "%~1" equ "h" (goto usageHelp)
if /i "%~1" equ "-h" (goto usageHelp)

::set defaults
set default_unlocalizeTxt=c:\unlocalize.txt
set stringReplaceExe=py3stringreplace

::read inputs
set file=%~1
if "%~2" equ "" (set replacementList=%default_unlocalizeTxt%) else (set replacementList=%~2)

::validate input
if not exist "%file%" (echo   Error: "%file%" does not exist.
goto end)
if not exist "%replacementList%" (echo   Error: Replacement list "%replacementList%" does not exist. 
goto end)

if "%file%" equ "*" goto batchMode

::core logic
"%stringReplaceExe%" "%file%" "%replacementList%" -nc

goto end


:batchMode
set tempfile=temp_%random%.temp
set tempScript=temp_%random%.cmd
if exist "%tempfile%" del "%tempfile%"
if exist "%tempScript%" del "%tempScript%"

dir /b *.txt >> %tempfile% 2>nul
dir /b *.ass >> %tempfile% 2>nul

for /f "delims=*" %%i in (%tempfile%) do echo call "%~nx0" "%%i" "%~2">>%tempScript%
if exist "%tempfile%" del "%tempfile%"

type "%tempScript%"
call "%tempScript%"
::type "%tempScript%"
if exist "%tempScript%" del "%tempScript%"

goto end

:usageHelp
echo   "fix" uses py3stringReplace with a predefined list to manipulate text files.
echo   Dependencies: py3stringReplace, c:\wordList.txt
echo.
echo   Syntax:
echo   fix myfile  or   fix *
echo   Examples:
echo   fix myfile.txt
echo   fix myfile.ass
echo   fix myfile.ass C:\unlocalize.txt
echo   fix *
echo.
echo   Notes: fix * will activate batch mode for .txt and .ass files
echo.

:end
endlocal
```

## Dependency Notes:

- [Python 3.4+](//www.python.org/downloads). For Windows 7, use [this repository](//github.com/adang1345/PythonWin7/).
    - Make sure `Add to Path` is checked/selected.
- Optional: Improved text encoding detection for files requires the `chardet` library.
    - The `chardet` library says it requires Python 3.7+: [pypi.org/project/chardet](//pypi.org/project/chardet/) Install using:
        - `python -m pip install --upgrade pip`     #Install latest version of pip package manager.
        - `pip install chardet`                             #Use `pip` to install `chardet`.
    - If this library is not available, then the default encoding of `utf-8` will always be used instead.
- To compile: pip, [pyinstaller](//www.pyinstaller.org).
    - #Use `pip` to install `pyinstaller`.
    - `pip install pyinstaller`                            

## Download and Install Guide:
```
Latest Version: 0.4
Development: Stopped. Open an issue for bugs, feature, or compile requests.
```
1. Download either the native executable `py3stringReplace.exe` or the python script `py3stringReplace.py`. Pick one:
    - Click on the green `< > Code` button at the top -> Download ZIP.
    - Click on on "Releases" at the side (desktop), or bottom (mobile), or [here](//github.com/gdiaz384/py3stringReplace/releases).
        - Download the appropriate binary for the OS and architecture.
    - Advanced:
        - Start a command prompt or terminal. On Windows this is `cmd.exe`
        - `git clone github.com/gdiaz384/py3stringReplace`
        - The above command requires git to be installed. Git is annoying to install on Windows due to some shell extensions it adds to explorer, but explaining how to get it to not be obnoxious is outside the scope of this guide.
1. If using the `.py` file, see the **Dependency Notes** section. Install Python 3.7+ and the `chardet` library before continuing.
    - Python may already be installed. Check by entering the following in a command prompt or terminal: `>python --version`
    - The `.exe` files do not require Python or the `chardet` library to be installed as they bundle precompiled (.pyc) binary versions of the necessary libraries already. However, they are no longer portable across different operating systems, cannot benefit from improvements in the Python standard library, and cannot be easily updated.
1. Extract all files including `py3stringReplace.exe` or `py3stringReplace.py` from the archive.
1. Place `py3stringReplace.exe` or `py3stringReplace.py` in the enviornmental path. To find places to put it: 
    - `>echo %path%`
1. (Optional) Rename `py3stringReplace.exe` or `py3stringReplace.py` to something memorable.
1. Open a command prompt or terminal and check it is in path using:
    - If using the `.py`, always invoke it using: `>python py3stringReplace.py --version`
    - If using the `.exe`, it can be invoked directly: `>py3stringReplace.exe --version`
1. Create a text file to use as `replacementList.txt`. See **Replacement List Syntax** and `replacementLists\unlocalize.txt` for additional information and an example.
1. Refer to the **Example Usage Guide** above for usage as well as `>py3StringReplace --help`

### Compile(exe) Guide:

- If downloading from github directly, remember to change the line ending back from broken-because-of-github by using [Notepad++](//notepad-plus-plus.org/download) or VS Code before attempting to compile. 
- Pyinstaller compatible character encodings for .py files are ascii, ansi, and utf-8 (without bom).

```
>python --version       #requires 3.4+. If using chardet, then 3.7+ is required.
>pip install pyinstaller
>pip install chardet     #optional, but reccomended
>pyinstaller --version  #to make sure it installed
>pyinstaller --onefile py3stringReplace.py
```
Look for the output under the 'dist' folder.

## Licenses:

- Python standard library's [license](//docs.python.org/3/license.html).
- chardet library's license is [LGPL v2+](https://pypi.org/project/chardet/).
- pyinstaller's [license](//pyinstaller.org/en/stable/license.html).
- For the .py files in this project, pick your license: GPL (any), or BSD (any), or MIT/Apache.
- If compiled with pyinstaller and then also distributed outside of your organization, then the executable file(s) is/are subject to Python's license, and the chardet library is subject to LGPL.
