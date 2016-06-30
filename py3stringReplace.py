#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Description:
py3str_Replace.py replaces strings in a text file with other strings from a replacement table.

- The replacement table is a text file with the first space used as a delimiter or first space after quoted text.
- New file is UTF-8 encoded.
- Use showMatching option to see what would be replaced. 

Usage: python py3stringReplace.py myinput.txt myTable.txt
#will output myinput.txt.sr.txt

Current version: 0.1.0
Last Modified: 30June16
License: any

##stop reading now##

Todo list:
- (feature) "" should be usable in replacement table
"""

import argparse                #used to add command line options
import os.path                   #test if file exists
import sys                          #end program on fail condition
import io                            #manipulate files (open/read/write/close)
from io import IOBase     #test if variable is a file object (an "IOBase" object)
from pathlib import Path  #override file in file system with another, experimental library

usage='\n Usage: python py3stringReplace.py myInputFile.txt myReplacementTable.txt'

#add command line options
command_Line_parser=argparse.ArgumentParser(description='Description: Replaces strings in text files using a replacement table.' + usage)
command_Line_parser.add_argument("inputFile", help="the text file to process",type=str)
command_Line_parser.add_argument("replacementList", help="the text file with replacement pairs",type=str)
command_Line_parser.add_argument("-o", "--output", help="specify the output file name, default is to append '.mod.txt'")
command_Line_parser.add_argument("-nc", "--noCopy", help="modify the existing file instead of creating a copy, default=create a copy, Takes precedence over -o",action="store_true")
command_Line_parser.add_argument("-sm", "--showMatching", help="show matches in stdout and exit",action="store_true")
command_Line_parser.add_argument("-d", "--debug", help="show generated replacementTable and exit",action="store_true")

#parse command line settings
command_Line_arguments=command_Line_parser.parse_args()
inputFileName=command_Line_arguments.inputFile
replaceListName=command_Line_arguments.replacementList
noCopy=command_Line_arguments.noCopy
showMatching=command_Line_arguments.showMatching
debug=command_Line_arguments.debug

if command_Line_arguments.output != None:
    outputFileName=command_Line_arguments.output
else:
    outputFileName=inputFileName+".mod.txt"

#debug code
#print("inputFileName="+inputFileName)
#print("replaceListName="+replaceListName)
#print("outputFileName="+outputFileName)
#print("noCopy="+str(noCopy))
#print("showMatching="+str(showMatching))
#print("debug="+str(debug))

#check to make sure inputFile.txt and replacementList.txt actually exist
if os.path.isfile(inputFileName) != True:
    sys.exit('\n Error: Unable to find input file "' + inputFileName + '"' + usage)
if os.path.isfile(replaceListName) != True:
    sys.exit('\n Error. Unable to find replacement list "' + replaceListName + '"' + usage)


#read replacement list
replaceListFile=open(replaceListName,'r')
replacementTable=dict({})

next(replaceListFile)  #skip first line
for line in replaceListFile:
    if len(line.strip()) != 0:
        if line.count('"') == 2:
            replacementTable[line.split(sep='"')[1].strip()]=line.split(sep='"')[2][1:-1].strip()
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
        print(("_" + i + "_" + v +"_").encode('utf-8'))
    sys.exit(0)


myInputFile=io.open(inputFileName,mode='r')
if showMatching!=True:
    myWriteFile=io.open(outputFileName,mode='w')
else:
    myWriteFile=outputFileName

for line in myInputFile:
    #newline=line
    for i,v in replacementTable.items():
        if line.rfind(i) != -1:
            if showMatching==True:
                print(('matchfound: ' + i).encode('utf-8')) 
                print(('matchfound: ' + i+" in " + line).encode('utf-8'))
                print((line.replace(i,v)).encode('utf-8'))
                print('\n')
            else:
                line=line.replace(i,v)
                #print(newline.encode('utf-8'))
    if showMatching!=True:
        #print('wrote line')
        myWriteFile.write(line)

#tidy up
myInputFile.close()
#print('python type: ' + str(isinstance(myWriteFile, IOBase)))
#if isinstance(myWriteFile, str) != True:
if isinstance(myWriteFile, IOBase) == True:
    if myWriteFile.closed != True:
        myWriteFile.close()

if showMatching==True:
    sys.exit(0)

if noCopy==True:
    #print('noCopy is true')
    if os.path.isfile(outputFileName) == True:
        Path(outputFileName).replace(inputFileName)
        print('Wrote ' + inputFileName)
elif noCopy!=True:
    #print('pie')
    print('Wrote ' + outputFileName)
