import os

import json

import sys

dirpath = "/home/kp4/myfm/lctes-riscv/eval/spec-swh/508.namd_r/build"
file1 = "main.o.baseline"
file2 = "main.o.abstractor"

def compare_sec(secAndSize1, secAndSize2, title):
    comp_size = [("", title)]
    for i in range(0, len(secAndSize1)):
        item1 = secAndSize1[i]
        diff = item1[1]
        sec2 = [x[0] for x in secAndSize2]
        if item1[0] in sec2:
            item2Index = sec2.index(item1[0])
            item2 = secAndSize2[item2Index]
            diff -= item2[1]
        if diff!=0:
            comp_size.append((item1[0], diff))

    for i in range(len(secAndSize2)):
        item2 = secAndSize2[i]
        diff = -item2[1]
        sec1 = [x[0] for x in secAndSize1]
        if not item2[0] in sec1:
            comp_size.append((item2[0], diff))

    return comp_size
   
def getSectionAndSize(filepath):
    instrFormat = "riscv32-unknown-elf-readelf -S --wide {}"
    instr = instrFormat.format(filepath)
    p = os.popen(instr, "r")
    lines = p.readlines()
    linetype = 0
    secAndSize = []
    currentSecName = ""
    for line in lines:
        items = line.split()
        if len(items) <= 0:
            continue
        if items[0] == "[Nr]":
            continue
        elif items[0].startswith("["):
            linetype = 1
            currentSecName = items[1]
            sizeStr = items[5]
            if currentSecName.endswith("]"):
                currentSecName = items[2]
                if currentSecName=="NULL":
                    continue
                sizeStr = items[6]
            size = int(sizeStr, 16)
            secAndSize.append([currentSecName, size])
            linetype = 0
            continue
    return secAndSize

def dumpSecAndSize(secAndSize):
    str2Print = ""
    for item in secAndSize:
        strFormat = "{}, {}\n"
        str2Print = str2Print + strFormat.format(item[0], item[1])
    print(str2Print)



def compareSec(dirpath, file1, file2):
    file1path = os.path.join(dirpath, file1)
    file2path = os.path.join(dirpath, file2)
    title = file1 + " - " + file2

    secAndSize1 = getSectionAndSize(file1path)
    secAndSize2 = getSectionAndSize(file2path)

    comp_size = compare_sec(secAndSize1, secAndSize2, title)
    dumpSecAndSize(comp_size)


def printUsage():
    print("USAGE:\tpython CompareSec.py OPTIONS param...\n\n" +
            "OPTIONS:\n"+
            "\t-compare\t\Compare the sections size differerce of the files.\n" +
            "\t-dump\t\tDump the sections of the file and each section's size.\n" +
            "\t-h\t\tPrint usage of this file.\n")

if __name__=="__main__":
    if len(sys.argv) < 3:
        print("ERROR:\tparams not enough\n")
        printUsage()
        exit()
    option = sys.argv[1]
    if option.__eq__("-h"):
        printUsage()
        exit()
    if option.__eq__("-dump"):
        if len(sys.argv) == 3:
            filepath = sys.argv[2]
            secAndSize = getSectionAndSize(filepath)
            dumpSecAndSize(secAndSize)

    if option.__eq__("-compare"):
        if len(sys.argv) < 4:
            print("ERROR:\tparams not enough\n")
            printUsage()
            exit()
        if len(sys.argv) == 5:
            dirpath = sys.argv[2]
            file1 = sys.argv[3]
            file2 = sys.argv[4]
            compareSec(dirpath, file1, file2)
