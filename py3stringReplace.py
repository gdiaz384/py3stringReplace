#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Description:
py3str_Replace.py replaces strings in a text file with other strings from a replacement table.

- The replacement table is a text file with the first space used as a delimiter or first space after quoted text.
- New file is UTF-8 encoded unless --outputEncoding (-oe) is specified.
- Use showMatching option to see what would be replaced. 

Usage: python py3stringReplace.py myinput.txt myTable.txt
#will output myinput.txt.sr.txt

Error handling documentation: docs.python.org/3.4/library/codecs.html#error-handlers
Example: www.w3schools.com/python/ref_string_encode.asp

Pick your license: Public Domain, GPL (any), or BSD (any), or MIT/Apache

###stop reading now###

"""

#set default options
defaultEncodingType='utf-8'
defaultReplacementListEncodingType='utf-8'
defaultConsoleEncodingType='utf-8'

#set static internal use variables
currentVersion='v0.4 - 2024Jan15'
usageHelp='\n Usage: python py3stringReplace.py myInputFile.txt myReplacementTable.txt'

import argparse                #used to add command line options
import os.path                  #test if file exists
import sys                        #end program on fail condition
import io                          #manipulate files (open/read/write/close)
from io import IOBase      #test if variable is a file object (an "IOBase" object)
from pathlib import Path    #override file in file system with another, experimental library. Not clear why needed, but might break something if removed, so just leave it.
#import csv                      #the dream; replacementList.csv
import codecs                 #Improves error handling when dealing with text file codecs.
try:
    import resources.dealWithEncoding as dealWithEncoding
    dealWithEncodingLibraryIsAvailable=True
except:
    dealWithEncodingLibraryIsAvailable=False

#Using the 'namereplace' error handler for text encoding requires Python 3.5+, so default to an old one.
sysVersion=int(sys.version_info[1])
if sysVersion >= 5:
    defaultOutputEncodingErrorHandler='namereplace'
elif sysVersion < 5:
    defaultOutputEncodingErrorHandler='backslashreplace'    
else:
    sys.exit('Unspecified error.'.encode(defaultConsoleEncodingType))

#add command line options
commandLineParser=argparse.ArgumentParser(description='Description: Replaces strings in text files using a replacement table.' + usageHelp)
commandLineParser.add_argument('inputFile', help='The text file to process.',type=str)
commandLineParser.add_argument('replacementList', help='The replacementList.txt file with match pairs.',type=str)
commandLineParser.add_argument('-o', '--output', help='Specify the output file name. Default is to append \'.mod.txt\'')

commandLineParser.add_argument('-nc', '--noCopy', help='Modify the existing file instead of creating a copy. Default=create a copy. Takes precedence over -o',action='store_true')
commandLineParser.add_argument('-sm', '--showMatching', help='Show matches in stdout and exit.',action='store_true')

commandLineParser.add_argument('-e', '--encoding', help='Specify input file encoding. Will also be used for output file if -oe one is not specified. Default='+defaultEncodingType,type=str)
commandLineParser.add_argument('-rle', '--replacementListEncoding', help='Specify encoding for replacementList.txt. Default='+defaultReplacementListEncodingType,type=str)
commandLineParser.add_argument('-oe', '--outputEncoding', help='Specify output file encoding. Default='+defaultEncodingType,type=str)
commandLineParser.add_argument('-ce', '--consoleEncoding', help='Specify encoding for stdout. Default='+defaultConsoleEncodingType,default=defaultConsoleEncodingType,type=str)

commandLineParser.add_argument('-ieh', '--inputErrorHandling', help='If the wrong input codec is specified, how should the resulting conversion errors be handled? See: docs.python.org/3.4/library/codecs.html#error-handlers Default=\'strict\'.',default='strict',type=str)
commandLineParser.add_argument('-eh', '--outputErrorHandling', help='How should output conversion errors between incompatible encodings be handled? See: docs.python.org/3.4/library/codecs.html#error-handlers Default=\''+defaultOutputEncodingErrorHandler+'\'.',default=defaultOutputEncodingErrorHandler,type=str)
commandLineParser.add_argument('-v', '--version', help='Show version information and exit.',action='store_true')
commandLineParser.add_argument('-d', '--debug', help='Show generated replacementTable and exit.',action='store_true')

#parse command line settings
commandLineArguments=commandLineParser.parse_args()   #magic
inputFileName=commandLineArguments.inputFile
replaceListName=commandLineArguments.replacementList
if commandLineArguments.output != None:
    outputFileName=commandLineArguments.output
else:
    outputFileName=inputFileName+'.mod.txt'

noCopy=commandLineArguments.noCopy
showMatching=commandLineArguments.showMatching

#The encoding of text files will be dealt with later. For now just set the stdout/console encoding.
consoleEncoding=commandLineArguments.consoleEncoding

inputErrorHandling=commandLineArguments.inputErrorHandling
outputErrorHandling=commandLineArguments.outputErrorHandling
if commandLineArguments.version == True:
    sys.exit(('currentVersion:'+currentVersion).encode(consoleEncoding))
debug=commandLineArguments.debug

#Now that file input names have been decided, handle the encoding settings for those files.
#The dealWithEncoding library will internally check if the files exist before and if it attempts to open them.
#So do not deal with checking if they exist yet in the main program.
if dealWithEncodingLibraryIsAvailable == True:
    #the dealWithEncoding library is available, so use it
    #update internal library variables to match main program settings
    dealWithEncoding.debug=debug
    dealWithEncoding.consoleEncoding=consoleEncoding
    #Syntax is: dealWithEncoding.ofThisFile(myFileName, rawCommandLineOption, fallbackEncoding):
    inputFileEncodingType=dealWithEncoding.ofThisFile(inputFileName,commandLineArguments.encoding,defaultEncodingType)
    replacementListEncodingType=dealWithEncoding.ofThisFile(replaceListName,commandLineArguments.replacementListEncoding,defaultReplacementListEncodingType)
elif dealWithEncodingLibraryIsAvailable == False:
    #the dealWithEncoding library is not available, so check if an encoding was specified manually
    if commandLineArguments.encoding != None:
        inputFileEncodingType=commandLineArguments.encoding
    else:
        #just set to default and hope for the best
        inputFileEncodingType=defaultEncodingType
        print(('Warning: Encoding not specified for file: \''+inputFileName+'\'. Using default encoding:\''+defaultEncodingType+'\'').encode(consoleEncoding))

    if commandLineArguments.replacementListEncoding != None:
        replacementListEncodingType=commandLineArguments.replacementListEncoding
    else:
        #just set to default and hope for the best
        replacementListEncodingType=defaultReplacementListEncodingType
        print(('Warning: Encoding not specified for file: \''+replaceListName+'\'. Using default encoding:\''+defaultEncodingType+'\'').encode(consoleEncoding))
else:
    sys.exit('Unspecified error.'.encode(consoleEncoding))

#encodingType=()commandLineArguments.encoding  #Isn't this a syntax error? Huh?
#replacementListEncodingType=commandLineArguments.replacementListEncoding

#Set encoding for output file.
#if output encoding is specified
if commandLineArguments.outputEncoding != None:
    #set output encoding to specified encoding
    outputEncodingType=commandLineArguments.outputEncoding
#else if no output encoding is specified
elif commandLineArguments.outputEncoding == None:
    #then set output encoding to utf-8
    #outputEncodingType=defaultEncodingType
    #Potentially, it would also be a sane setting to set the output the encoding as whatever the user input at the CLI. Yes, do that instead actually.
    #If user inserted a value for inputFile encoding at the CLI,
    if commandLineArguments.encoding != None:
        #then use that setting
        outputEncodingType=commandLineArguments.encoding
    #otherwise use default value.
    else:
        #This could also be set to the auto detected encoding, but utf-8 is just better.
        #If the user cannot be bothered to specify it, then just always output as utf-8.
        outputEncodingType=defaultEncodingType


#debug code
#print('outputEncodingType'+outputEncodingType)
#print('inputFileName='+inputFileName)
#print('replaceListName='+replaceListName)
#print('outputFileName='+outputFileName)
#print('noCopy='+str(noCopy))
#print('showMatching='+str(showMatching))
#print('debug='+str(debug))


#First, check to make sure inputFile.txt and replacementList.txt actually exist
if os.path.isfile(inputFileName) != True:
    sys.exit(('Error: Unable to find input file "' + inputFileName + '"' + usageHelp).encode(consoleEncoding))
if os.path.isfile(replaceListName) != True:
    sys.exit(('Error. Unable to find replacement list "' + replaceListName + '"' + usageHelp).encode(consoleEncoding))

#read replacement list
replaceListFile=codecs.open(replaceListName,'r',encoding=replacementListEncodingType,errors=inputErrorHandling)
replacementTable=dict({})

#Use the following syntax to update the dictionary:
#myDictionary["color"] = "red"
#next(replaceListFile)  #skip first line
for line in replaceListFile:
    if len(line.strip()) != 0:
        if line.count('"') == 2:
            replacementTable[line.split(sep='"')[1].strip()]=line.split(sep='"')[2][1:-1].strip()
        elif line.count('"') == 4:
            replacementTable[str(line.split(sep='" "',maxsplit=1)[0]+'"').strip()]=str('"'+line.split(sep='" "',maxsplit=1)[1]).strip()
        elif line[0] == '#':
            pass
        elif line[0] == ' ':
            pass
        elif line[0] == '':
            pass
        else:
            replacementTable[line.split(maxsplit=1)[0]]=line.split(maxsplit=1)[1][0:-1]
replaceListFile.close()

if debug == True:
    for i,v in replacementTable.items():
        print(("_" + i + "_" + v +"_").encode(consoleEncoding))
    sys.exit(0)


#For information on error handling: docs.python.org/3.4/library/codecs.html#error-handlers
#myInputFile=io.open(inputFileName,mode='r',encoding=inputFileEncodingType)
myInputFile=codecs.open(inputFileName,mode='r',encoding=inputFileEncodingType,errors=inputErrorHandling)
myInputFileContents=myInputFile.read()
myInputFile.close() #tidy tidy
if showMatching!=True:
    #myWriteFile=io.open(outputFileName,mode='w',encoding=outputEncodingType)
    myWriteFile=codecs.open(outputFileName,mode='w', encoding=outputEncodingType,errors=outputErrorHandling)
else:
    myWriteFile=outputFileName


for line in myInputFileContents:
    #newline=line
    for i,v in replacementTable.items():
        if line.rfind(i) != -1:
            if showMatching==True:
                print(('matchfound: ' + i).encode(consoleEncoding)) 
                print(('matchfound: ' + i+" in " + line).encode(consoleEncoding))
                print((line.replace(i,v)).encode(consoleEncoding))
                print('\n')
            else:
                line=line.replace(i,v)
                #print(newline.encode(consoleEncoding))
    if showMatching!=True:
        #print('wrote line')
        myWriteFile.write(line)

#tidy up
if isinstance(myWriteFile, IOBase) == True:
    if myWriteFile.closed != True:
        myWriteFile.close()

if showMatching==True:
    sys.exit(0)

if noCopy==True:
    if os.path.isfile(outputFileName) == True:
        Path(outputFileName).replace(inputFileName)
        print(('Wrote ' + inputFileName).encode(consoleEncoding))
elif noCopy!=True:
    print(('Wrote ' + outputFileName).encode(consoleEncoding))
