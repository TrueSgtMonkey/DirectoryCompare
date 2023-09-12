# Pass in two directories, and recursively check both for file and file size differences.

import os as os

## used for data - always retrieve paths with these when looking for files
DIR_1_NAME = "dir_1"
DIR_2_NAME = "dir_2"

## these used for printing and are calculated in main()
REL_DIR_NAME_1 = ""
REL_DIR_NAME_2 = ""

def main():
    attr = getAttributes("files.ini")
    lastSlashIdx1 = attr[DIR_1_NAME].rfind("\\")
    lastSlashIdx2 = attr[DIR_2_NAME].rfind("\\")
    REL_DIR_NAME_1 = attr[DIR_1_NAME][lastSlashIdx1+1:len(attr[DIR_1_NAME])]
    REL_DIR_NAME_2 = attr[DIR_2_NAME][lastSlashIdx2+1:len(attr[DIR_2_NAME])]
    print("Absolute Directories:\n\"" + attr[DIR_1_NAME] + "\"\n\"" + attr[DIR_2_NAME] + "\"")

    if parse(os.listdir(attr[DIR_1_NAME]), attr[DIR_1_NAME], os.listdir(attr[DIR_2_NAME]), attr[DIR_2_NAME], "", "dir1:\\\\" + REL_DIR_NAME_1, "dir2:\\\\" + REL_DIR_NAME_2):
        print("Directories are equal!")
    else:
        print("Directories are not equal!")

def parse(dir1, currDir1, dir2, currDir2, subDirString, dir1Name, dir2Name) -> bool:
    isEqual = True
    dir1.sort()
    dir2.sort()
    print(subDirString + "Relative Directories:\n" + subDirString + dir1Name + "\n" + subDirString + dir2Name)
    if not checkNumFilesForDirs(dir1, dir2, True, subDirString):
        print(subDirString + "Number of files in both directories not equal!")
        isEqual = False
    
    # Gathering all files that in one directory are not in the other directory
    filesToBeRemoved1 = getRemovalArray(dir1, dir2, subDirString, dir2Name)
    filesToBeRemoved2 = getRemovalArray(dir2, dir1, subDirString, dir1Name)
    if len(filesToBeRemoved1) > 0 or len(filesToBeRemoved2) > 0:
        isEqual == False

    # Deleting all files in one directory that are not in the other directory
    dir1 = delFilesFromDirArray(dir1, filesToBeRemoved1, subDirString, dir1Name)
    dir2 = delFilesFromDirArray(dir2, filesToBeRemoved2, subDirString, dir2Name)
    filesToBeRemoved1.clear()
    filesToBeRemoved2.clear()

    if not (len(dir1) == len(dir2)):
        print("ERROR: directories still not equal.")
        return False

    # Checking for byte differences in each file
    for idx in range(len(dir1)):
        fullPath1 = currDir1 + "\\" + dir1[idx]
        fullPath2 = currDir2 + "\\" + dir2[idx]
        if (not os.path.isdir(fullPath1)) and (not os.path.isdir(fullPath2)):
            # Check for byte differences in similar files from both directories
            sizeFile1 = os.path.getsize(fullPath1)
            sizeFile2 = os.path.getsize(fullPath2)
            if sizeFile1 != sizeFile2:
                print(subDirString + dir1[idx], "size:", sizeFile1, "vs", dir2[idx], "size:", sizeFile2)
        else:
            # need to keep the value of isEqual should it turn False
            if (not os.path.isdir(fullPath1)) or (not os.path.isdir(fullPath2)):
                print("ERROR:", dir1[idx], "or", dir2[idx], "are not directories")
                continue

            # parse sub-directory and return if that sub-directory was equal
            isSubDirEqual = parse(os.listdir(fullPath1), fullPath1, os.listdir(fullPath2), fullPath2, subDirString + "  ", dir1Name + "\\" + dir1[idx], dir2Name + "\\" + dir2[idx])
            if isSubDirEqual:
                print(subDirString + "  " + dir1Name, "and", dir2Name, "are equal!")
            else:
                print(subDirString + "  " + dir1Name, "and", dir2Name, "are NOT equal!")
            isEqual = isEqual and isSubDirEqual

    return isEqual

def delFilesFromDirArray(dir, filesToBeRemoved, subDirString, dirName) -> list:
    if len(filesToBeRemoved) > 0:
        print(subDirString + str(len(filesToBeRemoved)), "files were removed from", "\"" + dirName + "\"")
        for delFile1 in filesToBeRemoved:
            dir.remove(delFile1)

    return dir

def getRemovalArray(dir1, dir2, subDirString, dirName) -> list:
    filesToBeRemoved = []
    for fileName1 in dir1:
        if (fileName1 not in dir2):
            print(subDirString + fileName1, "not in", "\"" + dirName + "\"")
            filesToBeRemoved.append(fileName1)
    return filesToBeRemoved

def checkNumFilesForDirs(dir1, dir2, printLengths, subDirString):
    dir1Len = len(dir1)
    dir2Len = len(dir2)
    if printLengths:
        print(subDirString + "dir_1_files:", dir1Len)
        print(subDirString + "dir_2_files:", dir2Len)
    return dir1Len == dir2Len

def getAttributes(filename):
    lineNum = 1 # used for debugging
    filefound = False
    attrDict = {}
    retArr = getFile(filename)
    file = retArr[0]
    filefound = retArr[1]

    if not filefound:
        return attrDict
    
    for line in file.readlines():
        line = line.strip()

        # ignore entire lines if they start with a comment
        if line.startswith("#") or line == "": # comments or empty space
            continue

        print(line)

        # remove all comments on the same line as an argument
        if line.find("#") != -1:
            line = line[0:(line.find("#"))]
            line = line.strip()
        
        attrDict[line[0:(line.find(":"))].strip()] = line[(line.find(":")+2):len(line)].strip()
        lineNum += 1

    return attrDict

def getFile(filename):
    fileFound = False
    try:
        file = open(filename)
        fileFound = True
    except FileNotFoundError:
        print("Cannot find " + filename)
        return [None, False]
    
    return [file, fileFound]

if __name__ == "__main__":
    main()