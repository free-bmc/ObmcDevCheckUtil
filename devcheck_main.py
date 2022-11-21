#!/usr/bin/env python3
#MIT License

#Copyright (c) 2022 hramacha

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import os

from devicecatalog import InitDB
from devcheck_cli import CLIStart

global DeviceJson
global aParser
global DirNameList
global RootDirectory
global DocFileList 
global DriverDirList
global ToolVersion

DirNameList = []
RootDirectory = ""
DocFileList = []
DriverDirList = []
OBMC_DEVICE_WORK_DIR = None

ToolVersion = "1.0"

def main():
    print("Welcome to OpenBMC Device Check Utility")
    cwd = os.getcwd()
    
    OBMC_DEVICE_WORK_DIR = os.path.join(cwd, "work")    
    if os.path.exists(OBMC_DEVICE_WORK_DIR) == False:
        os.mkdir(OBMC_DEVICE_WORK_DIR)
        os.environ["OBMC_DEVICE_WORK_DIR"] = OBMC_DEVICE_WORK_DIR
    else:
        os.environ["OBMC_DEVICE_WORK_DIR"] = OBMC_DEVICE_WORK_DIR 
    InitDB()
    CLIStart(ToolVersion)

if __name__ == "__main__":
    main()

