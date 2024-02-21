#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Description:
py3iconv.py replaces strings in a text file with other strings from a replacement table.

- The replacement table is a text file with the first space used as a delimiter or first space after quoted text.
- New file is UTF-8 encoded unless --outputEncoding (-oe) is specified.
- Error handling options: https://docs.python.org/3.4/library/codecs.html#error-handlers

Usage: python py3iconv -h

License: See main project/readme.

##stop reading now##

"""
#set default options
defaultEncodingType='utf-8'
defaultConsoleEncodingType='utf-8'
defaultOutputEncodingType='utf-8'

#set static internal use variables
currentVersion='2024Jan15'
usageHelp='\n Usage: python py3iconv.py myInputFile.txt -ie utf-8 -oe shift-jis'

import argparse                #used to add command line options
import os.path                   #test if file exists
import sys                          #end program on fail condition
import io                            #manipulate files (imports open/read/write/close functions)
from pathlib import Path  #override file in file system with another, experimental library, not sure why or how this is useful or how it is 'experimental' but it might break something if I remove it, so I will just leave it.
import codecs                 #Improves error handling when dealing with text file codecs.
#import chardet               #attempt to detect chara encoding, import conditionally later. Update: Use library instead.

#Using the 'namereplace' error handler for text encoding requires Python 3.5+, so default to an old one.
sysVersion=int(sys.version_info[1])
if sysVersion >= 5:
    defaultOutputEncodingErrorHandler='namereplace'
elif sysVersion < 5:
    defaultOutputEncodingErrorHandler='backslashreplace'    
else:
    sys.exit('Unspecified error.'.encode(defaultConsoleEncodingType))

#add command line options
commandLineParser=argparse.ArgumentParser(description='Description: Provides very simple conversion from one text encoding format to another using py3 standard library.' + usageHelp)
commandLineParser.add_argument('inputFile', help='Specify the text file to process.',type=str)
commandLineParser.add_argument('-o', '--output', help='Specify the name of the output file. Default is to append \'.mod.txt\'')

commandLineParser.add_argument('-nc', '--noCopy', help='Modify the existing file instead of creating a copy. Default=Create a copy. Takes precedence over -o',action='store_true')

#commandLineParser.add_argument('-ie', '--inputEncoding', help='Specify the encoding of the input file. default='+defaultEncodingType,default=defaultEncodingType,type=str)
commandLineParser.add_argument('-ie', '--inputEncoding', help='Specify the encoding of the input file. Default='+defaultEncodingType,type=str)
commandLineParser.add_argument('-oe', '--outputEncoding', help='Specify the encoding of the output file. Default='+defaultEncodingType,default=defaultEncodingType,type=str)
commandLineParser.add_argument('-ce', '--consoleEncoding', help='Specify encoding for stdout. Default='+defaultEncodingType,default=defaultConsoleEncodingType,type=str)

#commandLineParser.add_argument('-a', '--automaticallyDetectEncoding', help='Try to detect source encoding and then exit, requires \'chardet\' library. Install with \'pip install chardet\'',action='store_true')
commandLineParser.add_argument('-ieh', '--inputErrorHandling', help='If the wrong input codec is specified, how should the resulting conversion errors be handled? See: docs.python.org/3.4/library/codecs.html#error-handlers Default=\'strict\'.',default='strict',type=str)
commandLineParser.add_argument('-eh', '--outputErrorHandling', help='How should output conversion errors between incompatible encodings be handled? See: docs.python.org/3.4/library/codecs.html#error-handlers Default=\''+defaultOutputEncodingErrorHandler+'\'.',default=defaultOutputEncodingErrorHandler,type=str)


commandLineParser.add_argument('-v', '--version', help='Print version and exit.',action='store_true')
commandLineParser.add_argument('-d', '--debug', help='Print too much information.',action='store_true')


#parse command line settings
commandLineArguments=commandLineParser.parse_args()
inputFileName=commandLineArguments.inputFile
inputEncodingType=commandLineArguments.inputEncoding

if commandLineArguments.output == None:
    outputFileName=inputFileName+".mod.txt"
else:
    outputFileName=commandLineArguments.output
outputEncodingType=commandLineArguments.outputEncoding

#automaticallyDetectEncoding=commandLineArguments.automaticallyDetectEncoding
inputErrorHandlingMethod=commandLineArguments.inputErrorHandling
outputErrorHandlingMethod=commandLineArguments.outputErrorHandling
noCopy=commandLineArguments.noCopy

consoleEncoding=commandLineArguments.consoleEncoding
if commandLineArguments.version == True:
    sys.exit(('Current version is from: '+currentVersion).encode(consoleEncoding))
debug=commandLineArguments.debug

#Test code for messing with console encoding.
#Nothing works. Just specify .encode() .Otherwise the console will output all ????'s.
#python 3.7+ only
#sys.stdout.reconfigure(encoding='cp437')
#sys.stdout=codecs.getwriter('utf-8')(sys.stdout.detatch())#
#python 3.1+
#def make_streams_binary():
#    sys.stdin = sys.stdin.detach()
#    sys.stdout = sys.stdout.detach()
#make_streams_binary()
#Also doesn't work.
#sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

#print(('pie').encode('utf-8'))

#check to make sure inputFile.txt actually exists
if os.path.isfile(inputFileName) != True:
    sys.exit(('Error: Unable to find input file "' + inputFileName + '"' + usageHelp).encode(consoleEncoding))


#validate input settings
#if (outputEncodingType.lower() == 'shift-jis') or (outputEncodingType.lower() == 'shift_jis'):
#    print(('Warning: shift-jis detected as output encoding. Altering to cp932 as a workaround for a bug. Comment out the conversion code if this is not desired.').encode(consoleEncodingType))
#    outputEncodingType='cp932'

#validate input settings
#if (encodingType.lower() == 'shift-jis') or (encodingType.lower() == 'shift_jis'):
#    print(('Warning: shift-jis detected as input encoding. Altering to cp932 as a workaround for a bug. Comment out the conversion code if this is not desired.').encode(consoleEncodingType))
#    encodingType='cp932'


#Try to detect input file encoding seperately from user input.
#detector=chardet.UniversalDetector()
#for line in open(inputFileName, 'rb'):
#    detector.feed(line)
#    if detector.done:
#        break
#print(detector.result)

#detector=chardet.UniversalDetector()
#openFile=open(inputFileName, 'rb')
#for line in openFile:
#    detector.feed(line)
#    if detector.done:
#        break
#openFile.close()  #doesn't work apparently

#https://docs.python.org/3.7/tutorial/inputoutput.html#methods-of-file-objects
#"It is good practice to use the with keyword when dealing with file objects. The advantage is that the file is properly closed after its suite finishes, even if an exception is raised at some point."

resultOfDetector=None
if 5 > 7:
#if automaticallyDetectEncoding == True:

    detector=chardet.UniversalDetector()
#   with open(inputFileName, 'rb', 0) as openFile:
    with open(inputFileName, 'rb') as openFile:
        for line in openFile:
            detector.feed(line)
            if detector.done == True:
                openFile.close()
                break
    print(openFile.closed) #says closed, but not actually closed. Changing Buffering doesn't matter. /giveup
    #Whatever. Just split program into two different modes. One for detecting encoding and one for converting between different encode modes since same file cannot be read from, closed and read from a second time in python apparently.
    openFile.close() #doesn't work
    #print(locals())
    #os.close(open(inputFileName))
    print(('Input encoding analysis of '+inputFileName+':').encode(consoleEncoding))
    print(str(detector.result).encode(consoleEncoding))
    resultOfDetector=detector.result['encoding']
    inputEncodingType=detector.result['encoding']
    print('Using detected encoding: '+inputEncodingType)
    #sys.exit()
#print('"'+str(resultOfDetector)+'"')

def detectEncoding(myFileName):
    import chardet
    detector=chardet.UniversalDetector()
    with open(myFileName, 'rb') as openFile:
        for line in openFile:
            detector.feed(line)
            if detector.done == True:
                openFile.close()
                break
    temp=detector.result['encoding']
    if debug == True:
        print((myFileName+':'+str(detector.result)).encode(consoleEncoding))
    return temp

#returns a string containing the encoding to use, relies on detectEncoding(filename)
#if (no encoding specified) and (automaticallyDetectEncoding == True): 
def handleDeterminingFileEncoding(myFileName, rawCommandLineOption, defaultEncoding):
    #elif (encoding was specified):
    if rawCommandLineOption != None:
        #set encoding to specified
        return rawCommandLineOption
    #if (no encoding specified for file...):
    elif rawCommandLineOption == None:
        try:
            import chardet
            chardetLibraryAvailable=True
        except:
            chardetLibraryAvailable=False
        #chardetLibraryAvailable=False
        #if automaticallyDetectEncoding library is available:
        if chardetLibraryAvailable == True:
            #set encoding to detectEncoding(myFileName)
            tempResult=detectEncoding(myFileName)
            print(('Warning: Using automatic encoding detection for file:\"'+str(myFileName)+'" as:\"'+str(tempResult)+'"').encode(consoleEncoding))
            return tempResult
        elif chardetLibraryAvailable == False:
            #set encoding to default value
            print(('Warning: Using default text encoding for file:\"'+str(myFileName)+'" as:\"'+str(defaultEncoding)+'"').encode(consoleEncoding))
            return defaultEncoding
        else:
            sys.exit('Unspecified error.'.encode(consoleEncoding))
    else:
        sys.exit('Unspecified error.'.encode(consoleEncoding))

inputEncodingType = handleDeterminingFileEncoding(myFileName=inputFileName, rawCommandLineOption=commandLineArguments.inputEncoding, defaultEncoding=defaultEncodingType)

#print(inputEncodingType)

#codecs.open is not compatible with 'with' command apparently. It opens the file twice. And disabling buffering (buffering=0) for text files does not work.
#with codecs.open(inputFileName,mode='r', encoding=inputEncodingType, buffering=1) as openFile: #buffering = 1 doesn't work either, huh? Both buffering and not buffering don't work. What a confusing library.
#with codecs.open(inputFileName,mode='r', encoding=inputEncodingType) as openFile:
#    print(openFile.closed)
#    for line in openFile:
#        print(line.encode(consoleEncoding))
#        break
#print(openFile.closed)
#openFile.close()
#print(openFile.closed)#while loop within a while loop cannot really itterate through it line by line
#    with codecs.open(outputFileName,mode='w', encoding=inputEncodingType) as outFile:

if inputEncodingType != outputEncodingType:
    if noCopy == False:
        print(('Writing to file:'+outputFileName+' using encoding: \'' + outputEncodingType+'\'.').encode(consoleEncoding))
    elif noCopy == True:
        print(('Writing to file:'+inputFileName+' using encoding: \'' + outputEncodingType+'\'.').encode(consoleEncoding))
    try:
        inputFile=codecs.open(inputFileName,mode='r', encoding=inputEncodingType, errors=inputErrorHandlingMethod)
        outputFile=codecs.open(outputFileName,mode='w', encoding=outputEncodingType, errors=outputErrorHandlingMethod)
        #print('pie')
        for line in inputFile:
            outputFile.write(line)
    finally:
        inputFile.close()
        outputFile.close()
        #print(inputFile.closed)
        #inputFile.close()
        #print(inputFile.closed)
elif inputEncodingType == outputEncodingType:
    print(('inputEncodingType:'+inputEncodingType+'='+'outputEncodingType:'+outputEncodingType+' Nothing to do.').encode(consoleEncoding))
    sys.exit(usageHelp.encode(consoleEncoding))

#actually, not compatible with mode 't'. That is what causes it to open twice. Regular open() works fine but not codecs.open()
#myFile = codecs.open(inputFileName,mode='rt', encoding=inputEncodingType)
#myFileContents=myFile.read()
#print(myFile.closed)
#myFile.close()
#print(myFile.closed)


#Open file
#codecs.open(inputFileName,mode='r', encoding=inputEncodingType).read()

#Open file handle
#myFile=
#read in contents
#myFileContents=myFile.read()
#Close file
#myFile.close()

#print(myFileContents.encode(consoleEncoding))

if noCopy==True:
    if os.path.isfile(outputFileName) == True:
        Path(outputFileName).replace(inputFileName)
