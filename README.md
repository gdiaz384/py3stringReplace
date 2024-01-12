# py3stringReplace

py3stringReplace replaces strings in text files based upon a user defined list.

## Key Features:

- Automates tedious ctrl+f replacements.
- Command Line Interface (CLI).
- Precompiled binaries for Windows.
- Scripting friendly.
- Cross platform (Python 3).
- Supports various character [encodings](https://docs.python.org/3.4/library/codecs.html#standard-encodings). 

## Example Usage Guide:

Syntax: py3stringReplace [-h] [-o output.txt] [-nc] [-sm] [-d] inputFile.txt replacementList.txt

Notes:
- [ ] means optional.
- Flags that only specify the encoding for this or that file were not included above. See Advanced Usage below.

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

## Download and Install Guide:
```
Latest Version: 0.31
Development: stopped. Open an issue for bugs, feature or compile requests.
```
1. Click [here](//github.com/gdiaz384/py3stringReplace/releases) or on "releases" at the top to download the latest version.
2. Extract py3stringReplace.exe from the archive of your OS/architecture.
3. Place py3stringReplace.exe in your enviornmental path
  - To find places to put it: >echo %path%
4. (optional) rename it to something memorable
5. Create a text file to use as a replacementList.txt. See **Replacement List Syntax** and **replacementLists\unlocalize.txt** for additional information.
6. Refer to the **Example Usage Guide** above for usage.

## Replacement List Syntax:

- The replacementList.txt is made up of line seperated "match pairs."
- A "match pair" specifies theStringToReplace and theReplacement.
- The match pair delimiter is the first space or, in the case of quoted text, the first space after quoted text.
- To include quotation marks as literals, use exactly four of them.
- A reference replacementList.txt can be found at **replacementLists\unlocalize.txt**

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
  - py3stringReplace myscript.txt unlocalize.txt -d > pairs.txt
- The syntax for replacementList.txt is unforgiving and as follows:
  - The first line is ignored.
  - The last line must be an empty line. The list may not end in a match pair.
  - Lines that start with # indicate a comment.
  - Empty lines are ignored.
  - Whitespace outside of quotation marks is ignored.
  - Whitespace within quotation marks is preserved.
  - Non-empty lines with only whitespace are ignored.
  - The order of match pairs in replacementList.txt is not important, at least in Python <=3.6.
  - Quotations marks (") are overloaded in order to provide an option for replacements to include them.
    - Including 2 quotation marks means: split at the first space after the second quotation mark.
    - Including 4 quotation marks means: split where there are two quotation marks and a space in the middle, preserving both.
 
## Release Notes:
- Replacements are performed out of order. To perform ordered replacements, use a second replacement list.
- Ordered replacements might be possible/happening in Python >=3.7, but this has not been tested.
- Dealing with character encoding:
    - The input files will be read/written as utf-8 encoded by default. To change the encoding use the -e option.
    - To use a different output encoding than input encoding, use --outputEncoding (-oe).
        - Combined with an empty replacement list, this can convert between different formats similar to the unix `iconv` tool, although this is very hacky.
        - Proper support for direct conversions might be added later, and maybe replacementList as a .csv too.
    - Output to stdout is utf-8 formatted by default. To change the console encoding use the -ce option.
    - The replacementList.txt is read as utf-8 by default. To change the encoding use the -rle option.
    - Due to console limitations, consider using [Notepad++](//notepad-plus-plus.org/download) to change the input to utf-8 when debuging.
        - On newer versions of Windows (~Win 10 1809+), consider changing the console encoding to native utf-8. There is a checkbox for it in the change locale window.
    - [https://docs.python.org/3.4/library/codecs.html#standard-encodings](https://docs.python.org/3.4/library/codecs.html#standard-encodings) 
- If downloading a replacementList.txt from github directly instead of using a release.zip, remember to change the line ending back to not-broken before attempting to use it by using Notepad++ or VS Code (if applicable).

## Advanced Usage Guide:

- The idea is to type "fix mysubs.ass" or "fix *" and have the rest be automatic.
- Make sure py3stringReplace.exe is in %path% and put the following in a file called C:\Users\User\fix.bat.

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

for /f "delims=*" %%i in (%tempfile%) do echo call "%~nx0" "%%i" %2>>%tempScript%
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

## Dependencies
- [Python 3.4+](//www.python.org/downloads)
- To compile: pip, [pyinstaller](http://www.pyinstaller.org)

## Compile(exe) Guide:

- If downloading from github directly, remember to change the line ending back from broken-because-of-github by using [Notepad++](//notepad-plus-plus.org/download) before attempting to compile. 
- Pyinstaller compatible character encodings for .py files are ANSI and utf-8 w/o BOM.

```
>python --version   #requires 3.4+
>pip install pyinstaller
>pyinstaller --version  #to make sure it installed
>pyinstaller --onefile py3stringReplace.py
```
Look for the output under the "dist" folder.

## License:
Pick your License: Public Domain, GPL (any) or BSD (any) or MIT/Apache
