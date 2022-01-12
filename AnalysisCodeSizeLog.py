'''
Author: Wenhan Shang
Email: whu_swh@whu.edu.cn
Date: 2022-01-05 13:45:20
Description: Waiting to add
FilePath: /PyScripts/AnalysisCodeSizeLog.py
'''
import os
import sys
import re

CSVFileList = ["AbstractedRegions", "IntersectRegionClosures", "SameRegions", "SimilarRegions"]
CSVPostFix = ".csv"

def writeFileWithContent(filePath, content):
    file = open(filePath, mode="w", encoding="utf-8")
    file.write(content)


def getResultDirPath(sourceFile):
    return sourceFile.replace("."+sourceFile.split(".")[-1], "") + "/"


def convertToCSVFiles(sourceFile):
    print("Converting the log file [{}] to some CSV files.".format(sourceFile))
    logFile = open(sourceFile)
    fileStr = logFile.read()
    fileStr = re.sub("[\n]+", "\n", fileStr)
    regx = "######[ |A-Z|a-z|0-9]* Begin ######\n|######[ |A-Z|a-z|0-9]* End ######\n"
    splitStr = re.split(regx, fileStr)
    csvStr = [ x for x in splitStr if x and x != "\n" and not x.startswith("######")]
    findedStr = re.findall(regx, fileStr)
    if len(findedStr)==2*len(csvStr):
        csvDirPath = getResultDirPath(sourceFile=sourceFile)
        os.makedirs(csvDirPath, exist_ok=True)
        for i in range(len(csvStr)):
            fileName = re.sub("\s+", "", re.sub("######| Begin ######| End ######","",findedStr[2*i])) + CSVPostFix
            csvFile = csvDirPath + fileName
            writeFileWithContent(filePath=csvFile, content=csvStr[i])



def synthesizeAllInfo():
    
    pass


def printUsage():
    print("USAGE:\tpython AnalysisCodeSizeLog.py OPTIONS param...\n\n" +
            "OPTIONS:\n"+
            "\t-csv\t\tConvert the log file specified by first param to some CSV files.\n" +
            "\t-h\t\tPrint usage of this file.\n")


if __name__=="__main__":
    if len(sys.argv) < 2:
        print("ERROR:\tparams not enough\n")
        printUsage()
        exit()
    option = sys.argv[1]
    if option.__eq__("-h"):
        printUsage()
        exit()
    if option.__eq__("-csv"):
        sourceFile = sys.argv[2]
        if not os.path.exists(sourceFile):
            print("ERROR:\tSpecified file does not exist!\n")
            printUsage()
            exit()
        convertToCSVFiles(sourceFile)



        