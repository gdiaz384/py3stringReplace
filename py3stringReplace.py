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

License: Public domain

##stop reading now##

"""

import argparse                #used to add command line options
import os.path                   #test if file exists
import sys                          #end program on fail condition
import io                            #manipulate files (open/read/write/close)
from io import IOBase     #test if variable is a file object (an "IOBase" object)
from pathlib import Path  #override file in file system with another, experimental library

#set default options
defaultEncodingType='utf-8'
defaultConsoleEncodingType='utf-8'
defaultReplacementListEncodingType='utf-8'

#set static internal use variables
currentVersion='v0.31 - 2024Jan11'
usageHelp='\n Usage: python py3stringReplace.py myInputFile.txt myReplacementTable.txt'

#add command line options
command_Line_parser=argparse.ArgumentParser(description='Description: Replaces strings in text files using a replacement table.' + usageHelp)
command_Line_parser.add_argument("inputFile", help="the text file to process",type=str)
command_Line_parser.add_argument("-e", "--encoding", help="specify input/output file encoding, default=utf-8",default=defaultEncodingType,type=str)
command_Line_parser.add_argument("replacementList", help="the text file with match pairs",type=str)
command_Line_parser.add_argument("-rle", "--replacementListEncoding", help="specify encoding for the replacementList.txt, default=utf-8",default=defaultReplacementListEncodingType,type=str)
command_Line_parser.add_argument("-o", "--output", help="specify the output file name, default is to append '.mod.txt'")
command_Line_parser.add_argument("-oe", "--outputEncoding", help="specify output file encoding, default=utf-8",default=defaultEncodingType,type=str)

command_Line_parser.add_argument("-nc", "--noCopy", help="modify the existing file instead of creating a copy, default=create a copy, Takes precedence over -o",action="store_true")
command_Line_parser.add_argument("-sm", "--showMatching", help="show matches in stdout and exit",action="store_true")

command_Line_parser.add_argument("-ce", "--consoleEncoding", help="specify encoding for stdout, default=utf-8",default=defaultConsoleEncodingType,type=str)
command_Line_parser.add_argument("-d", "--debug", help="show generated replacementTable and exit",action="store_true")

#parse command line settings
command_Line_arguments=command_Line_parser.parse_args()
inputFileName=command_Line_arguments.inputFile
encodingType=command_Line_arguments.encoding
replaceListName=command_Line_arguments.replacementList
replacementListEncodingType=command_Line_arguments.replacementListEncoding
outputEncodingType=command_Line_arguments.outputEncoding

noCopy=command_Line_arguments.noCopy
showMatching=command_Line_arguments.showMatching

consoleEncodingType=command_Line_arguments.consoleEncoding
debug=command_Line_arguments.debug

#validate input settings
if (outputEncodingType.lower() == 'shift-jis') or (outputEncodingType.lower() == 'shift_jis'):
    print(('Warning: shift-jis detected as output encoding. Altering to cp932 as a workaround for a bug. Comment out the conversion code if this is not desired.').encode(consoleEncodingType))
    outputEncodingType='cp932'

if command_Line_arguments.output != None:
    outputFileName=command_Line_arguments.output
else:
    outputFileName=inputFileName+".mod.txt"

#debug code
#print(outputEncodingType)
#print("inputFileName="+inputFileName)
#print("replaceListName="+replaceListName)
#print("outputFileName="+outputFileName)
#print("noCopy="+str(noCopy))
#print("showMatching="+str(showMatching))
#print("debug="+str(debug))

#check to make sure inputFile.txt and replacementList.txt actually exist
if os.path.isfile(inputFileName) != True:
    sys.exit('\n Error: Unable to find input file "' + inputFileName + '"' + usageHelp)
if os.path.isfile(replaceListName) != True:
    sys.exit('\n Error. Unable to find replacement list "' + replaceListName + '"' + usageHelp)


#read replacement list
replaceListFile=open(replaceListName,'r',encoding=replacementListEncodingType)
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
        print(("_" + i + "_" + v +"_").encode(consoleEncodingType))
    sys.exit(0)


myInputFile=io.open(inputFileName,mode='r',encoding=encodingType)
if showMatching!=True:
    myWriteFile=io.open(outputFileName,mode='w',encoding=outputEncodingType)
else:
    myWriteFile=outputFileName

for line in myInputFile:
    #newline=line
    for i,v in replacementTable.items():
        if line.rfind(i) != -1:
            if showMatching==True:
                print(('matchfound: ' + i).encode(consoleEncodingType)) 
                print(('matchfound: ' + i+" in " + line).encode(consoleEncodingType))
                print((line.replace(i,v)).encode(consoleEncodingType))
                print('\n')
            else:
                line=line.replace(i,v)
                #print(newline.encode(consoleEncodingType))
    if showMatching!=True:
        #print('wrote line')
        myWriteFile.write(line)

#tidy up
myInputFile.close()
if isinstance(myWriteFile, IOBase) == True:
    if myWriteFile.closed != True:
        myWriteFile.close()

if showMatching==True:
    sys.exit(0)

if noCopy==True:
    if os.path.isfile(outputFileName) == True:
        Path(outputFileName).replace(inputFileName)
        print(('Wrote ' + inputFileName).encode(consoleEncodingType))
elif noCopy!=True:
    print(('Wrote ' + outputFileName).encode(consoleEncodingType))
