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
import json
from pathlib import Path

import scanlib 
from scanlib import ModuleInfoClass
from scanlib import ModuleDeviceClass
from scanlib import DeviceInfoClass
from scanlib import DeviceScannerElementClass
from scanlib import DeviceCompatibleJsonDataClass
from scanlib import DeviceListInfoClass

from utils import progressbar

# Global Variables 
DeviceDataList = []
OBMC_DEVICE_DB_DIR = None
OBMC_LINUX_SOURCE_DIR = None
OBMC_LINUX_SOURCE_DRIVER_DIR = None
OBMC_LINUX_SOURCE_DOC_DIR = None
InterfaceDiscoveryList = []
InterfaceCommitList = []
InterfaceList = []
DeviceTypeList = []
DeviceList = []
ManufacturerList = []
CompatibilityDeviceList = []
data_record_count = 0
DeviceGeneratedJsonList = []
DriverReferenceList = []
DocReferenceList = []
DTReferenceList = []
LinuxVersion = ""
  
def BuildDriversDirectoryList(rootdir):
    obj = os.scandir(rootdir)
    for entry in obj:
        if os.path.islink(entry):
            continue
        if entry.is_dir():
            BuildDriversDirectoryList(entry)
        else:
            if entry.name.endswith('.c'):
                #print(entry.name)
                DriverReferenceList.append(entry)
                #ProcessDriverFile(entry)

    return 

def BuildDriversDocList(rootdir):
    global DocReferenceList
    obj = os.scandir(rootdir)
    for entry in obj:
        if os.path.islink(entry):
            continue
        if entry.is_dir():
            BuildDriversDocList(entry)
        else:
            if entry.name.endswith('.rst'):
                #print(entry.name)
                DocReferenceList.append(entry)
    return 

def BuildDTDocList(rootdir):
    global DTReferenceList
    obj = os.scandir(rootdir)
    for entry in obj:
        if os.path.islink(entry):
            continue
        if entry.is_dir():
            BuildDTDocList(entry)
        else:
            if entry.name.endswith('.yaml'):
                #print(entry.name)
                DTReferenceList.append(entry)
    return 

def BuildDeviceCatalog():
    global LinuxVersion    
    fileReader = open(OBMC_LINUX_SOURCE_DIR+"/Makefile", "r")
    filelines = fileReader.readlines()
    fileReader.close
    Linuxversion = ""
    LinuxPatchLevel = ""
    LinuxSubLevel = ""

    for line in filelines:
        if "VERSION =" in line and LinuxVersion != None:
            Linuxversion = line.replace("VERSION =", "").strip()
        if "PATCHLEVEL =" in line and LinuxPatchLevel != None:
            LinuxPatchLevel = line.replace("PATCHLEVEL =", "").strip()
        if "SUBLEVEL =" in line and LinuxSubLevel != None:
            LinuxSubLevel = line.replace("SUBLEVEL =", "").strip()
            break

    lversionlist = []
    lversionlist.append(Linuxversion)
    lversionlist.append(LinuxPatchLevel)
    lversionlist.append(LinuxSubLevel)
    LinuxVersion = ".".join(lversionlist)
    print(LinuxVersion)

    for i in progressbar(range(len(DriverReferenceList)), "Building Device Catalog : ", 100):
        ProcessDriverFile(DriverReferenceList[i])

def GetDriverDocName(drivername):
    for entry in DocReferenceList:
        dName = drivername.split(".")
        eName = entry.name.split(".")        
        if len(dName) > 1 and len(eName) > 1:
            if dName[0].strip() == eName[0].strip():
                #print(dName[0], eName[0])
                return entry
    
    return None

def GetDTReference(devicename):
    for entry in DTReferenceList:
        dName = devicename.split(".")
        eSplit = entry.name.split(".")        
        eName = eSplit[0]
        if "," in eName:
            eName = eName.split(",")[1]
    
        if dName[0].strip() in eName.strip():
#            print("DT :",dName[0], eName)
            return entry

    return None

def AddDiscoveryList(intftype):
    if len(InterfaceDiscoveryList) == 0:
        InterfaceDiscoveryList.append(intftype)
    else:
        found = False
        for s in InterfaceDiscoveryList:
            if s == intftype:
                found = True
        if found == False:
            InterfaceDiscoveryList.append(intftype)        

def ProcessDatabase(selection):
    global OBMC_LINUX_SOURCE_DIR    
    global OBMC_LINUX_SOURCE_DRIVER_DIR
    global OBMC_LINUX_SOURCE_DOC_DIR

    OBMC_LINUX_SOURCE_DIR = os.environ.get('OBMC_LINUX_SOURCE_DIR')

    if OBMC_LINUX_SOURCE_DIR == None:
        print("Database Operations require OpenBMC Linux Source Path")
        print("OBMC_LINUX_SOURCE_DIR NOT SET")        
        print("perform git clone https://github.com/openbmc/linux and point to the directory")
        print("Use export OBMC_LINUX_SOURCE_DIR=<Linux Root Directory Path>")
        print("Unable to perform Database Operation ")
        return                
    
    OBMC_LINUX_SOURCE_DRIVER_DIR = os.path.join(OBMC_LINUX_SOURCE_DIR, 'drivers')
    OBMC_LINUX_SOURCE_DOC_DIR =  os.path.join(OBMC_LINUX_SOURCE_DIR, 'Documentation')

    if selection == "build":
        #print(selection)
        BuildDriversDocList(OBMC_LINUX_SOURCE_DOC_DIR)
        BuildDTDocList(OBMC_LINUX_SOURCE_DOC_DIR)
        BuildDriversDirectoryList(OBMC_LINUX_SOURCE_DRIVER_DIR)
        BuildDeviceCatalog()
        #print("Interfaces Found ", len(InterfaceDiscoveryList))
        GenerateDeviceCatalogDatabaseForJson()        
    if selection == "update":
        #print(selection)
#        OBMC_LINUX_SOURCE_DRIVER_DIR = '/home/hari/github/LinuxSource/linux-dev-6.0/drivers'
        BuildDriversDirectoryList(OBMC_LINUX_SOURCE_DRIVER_DIR)
        BuildDeviceCatalog()
        GenerateDeviceCatalogDatabaseForJson()

def InitDB():
    cwd = os.getcwd()
    global OBMC_DEVICE_DB_DIR
    OBMC_DEVICE_DB_DIR = os.path.join(cwd, "dataBase")    
    print("Device Database: Initializing Device Database ...")
    if os.path.exists(OBMC_DEVICE_DB_DIR):
        db_path = os.path.join(OBMC_DEVICE_DB_DIR, "DeviceCatalogDB.json")
        if os.path.exists(db_path):
            GenerateDeviceCatalogDBFromJson()
        else:
            ProcessDatabase("build")
            GenerateDeviceCatalogDBFromJson()
    else: 
        os.mkdir(OBMC_DEVICE_DB_DIR)    
        ProcessDatabase("build")
        GenerateDeviceCatalogDBFromJson()
    print("Device Database: Ready ...")  

def GenerateDeviceCatalogDatabaseForJson():
    device_json_list = []

    for i in progressbar(range(len(DeviceDataList)), "Generate Device Catalog : ", 100):
        device_json = {}
        
        #print("Interface Type ",DeviceJsonList[i].JsonData.InterfaceType,len(DeviceJsonList[i].JsonData.Devices) )
        device_json['FileName'] = DeviceDataList[i].FileName.strip()
        device_json['DeviceType'] = DeviceDataList[i].DeviceType.strip()
        device_json['Description'] = DeviceDataList[i].Description.strip() 
        device_json['DriverInformation'] = DeviceDataList[i].DriverInformation.strip()
        device_list = []
        for j in range(0, len(DeviceDataList[i].DeviceInfoList)):
            device = {}
            #print("Interface Type ", DeviceDataList[i].DeviceInfoList[j].InterfaceType, "DeviceID ", DeviceDataList[i].DeviceInfoList[j].DeviceID)
            device['InterfaceType'] = DeviceDataList[i].DeviceInfoList[j].InterfaceType.strip()
            device['DeviceID'] = DeviceDataList[i].DeviceInfoList[j].DeviceID.strip()
            device_list.append(device)

        device_json['Devices'] = device_list

        comp_device_list = []
        for j in range(0, len(DeviceDataList[i].CompatibleList)):
            comp_device = {}
            comp_device['Manufacturer'] = DeviceDataList[i].CompatibleList[j].Manufacturer.strip()
            comp_device['DeviceName'] = DeviceDataList[i].CompatibleList[j].DeviceName.strip()
            comp_device['DTReference'] = DeviceDataList[i].CompatibleList[j].DTReference.strip()
            comp_device_list.append(comp_device)                

        device_json['Compatible'] = comp_device_list
        device_json_list.append(device_json)

    data = {}
    data["LinuxVersion"] = LinuxVersion
    data["DeviceCatalogDatabase"] = device_json_list
    data["DateOfLastUpdate"] = "INIT"
    PrettyJson = json.dumps(data, indent=4, separators=(',', ':'))
    #print("Generate", OBMC_DEVICE_DB_DIR)
    with open(os.path.join(OBMC_DEVICE_DB_DIR,"DeviceCatalogDB.json"), "w") as outfile:
        outfile.write(PrettyJson)

def ProcessDriverFile(file):
    line = ""
    fileReader = open(file, "r")    
    filelines = fileReader.readlines()
    fileReader.close
    lines = []
    for line in filelines:
        if line.count != 0:
            lines.append(line)
    
    #print(len(lines))    
    moduleInfo = ModuleInfoClass()

    for s in lines:
        if "MODULE_DESCRIPTION" in s:            
            s1 = s.split("\"")
            if len(s1) > 1: 
                if "driver" in s1[1]:
                    moduleInfo.ModuleDescription = s1[1].replace("driver", "")
                elif "Driver" in s1[1]:
                    moduleInfo.ModuleDescription = s1[1].replace("Driver", "")
                else:
                    moduleInfo.ModuleDescription = s1[1]
        
        if "_NAME" in s and "#define" in s and "\"" in s: 
            if len(s.split("\"")) > 1: 
                moduleInfo.DRV_NAME = s.split("\"")[1]
        

        if "MODULE_DEVICE_TABLE(of" in s:
            #print("MO")
            t = s.split(",")[1]
            moduleInfo.ModuleDeviceTableOfId = t.split(")")[0]
            #ModuleInfoList.append(moduleInfo)
        else:
            if "MODULE_DEVICE_TABLE(" in s:                
                if len(s.split("(")) > 1:
                    #print("MDT")
                    t = s.split("(")[1]
                    t1 = t.split(")")       
                    moduledeviceInfo = ModuleDeviceClass()                    
                    moduledeviceInfo.InterfaceType = str(t1[0].split(",")[0])
                    AddDiscoveryList(moduledeviceInfo.InterfaceType)
                    moduledeviceInfo.ModuleDeviceTableId = str(t1[0].split(",")[1])
                    #print("Interace Type ",moduledeviceInfo.InterfaceType)
                    #print(moduledeviceInfo.InterfaceType, moduledeviceInfo.ModuleDeviceTableId) 
                    moduleInfo.ModuleInfoList.append(moduledeviceInfo)

    if not moduleInfo.ModuleDescription:
        return
    if not moduleInfo.ModuleDeviceTableOfId and len(moduleInfo.ModuleInfoList) == 0:
        return
    
    #print("File ", file,len(moduleInfo.ModuleInfoList), moduleInfo.ModuleDeviceTableOfId )
    CurrentDeviceElementScanner = DeviceScannerElementClass()
    CurrentDeviceElementScanner.FileName = str(file.name)
    CurrentDeviceElementScanner.Description = str(moduleInfo.ModuleDescription)    
    DocFile = GetDriverDocName(file.name)
    if DocFile != None: 
        CurrentDeviceElementScanner.DriverInformation = str(Path(DocFile).absolute()).replace(OBMC_LINUX_SOURCE_DOC_DIR,"")

    t = os.path.abspath(Path(file).parent)        
    t1 = t.replace(OBMC_LINUX_SOURCE_DRIVER_DIR, "")
    
    IDString = t1.split("/")
    #print("ID", IDString)
    DeviceTypesList = []
    if len(IDString) > 0:
        for id in IDString: 
            if id != "":
                DeviceTypesList.append(id)

    if len(DeviceTypesList) > 1:
        CurrentDeviceElementScanner.DeviceType = str(",".join(DeviceTypesList))
    elif len(DeviceTypesList) == 1:
        CurrentDeviceElementScanner.DeviceType = str(DeviceTypesList[0])
    else:
        hello = False

    for modInfo in moduleInfo.ModuleInfoList:        
        #print(CurrentDeviceElementScanner.DeviceTypesList)
        #print(modInfo.ModuleDeviceTableId)
        
        header_found = False   
        ffound = False     
        for index in range(0, len(lines)):
            if modInfo.ModuleDeviceTableId+"[]" in lines[index] and modInfo.InterfaceType in lines[index] and "=" in lines[index]:
                #print("1 ", s)
                header_found = True
                continue            
            if header_found == True:
                if "{" in lines[index] and "}" in lines[index]:                    
                    eLine = lines[index].replace("{", "")
                    eLine = eLine.replace("}", "")
                    eLine = eLine.split(",")[0]
                    eLine = eLine.replace("\"", "").strip()
                    #elements.append(lines[idx].replace("{", "").replace("}", "").split(",")[0].replace("\"", ""))
                    if eLine != "" and eLine:
                        if "=" in eLine:
                            eLine = eLine.split("=")[1].strip()
                        devinfo = DeviceInfoClass(modInfo.InterfaceType, eLine)
                        CurrentDeviceElementScanner.DeviceInfoList.append(devinfo)
                elif "{" in lines[index]:
                    if "\"" in lines[index]:
                        s1 = lines[index].split("\"")
                        eLine = s1[1]
                        if "=" in eLine:
                            eLine = eLine.split("=")[1].strip()
                        devinfo = DeviceInfoClass(modInfo.InterfaceType, eLine)
                        CurrentDeviceElementScanner.DeviceInfoList.append(devinfo)                            
                elif "};" in lines[index]:
                    break;
                else:
                    Warning

    if moduleInfo.ModuleDeviceTableOfId:
        header_found = False
        for s in lines:
            if moduleInfo.ModuleDeviceTableOfId+"[]" in s and "=" in s:
                header_found = True
                continue
            if header_found == True:
                if "};" in s:
                    header_found = False
                    break
                if ".compatible" in s: 
                    if len(s.split("\"")) > 1:
                        element = s.split("\"")[1]                
                        elements = element.split(",")

                        if len(elements) > 1:
                            DeviceCompatibleData = DeviceCompatibleJsonDataClass(elements[0], elements[1])
                            DTFile = GetDTReference(elements[1]) 
                            if DTFile != None:
                                DeviceCompatibleData.DTReference = str(Path(DTFile).absolute()).replace(OBMC_LINUX_SOURCE_DOC_DIR,"")
                            CurrentDeviceElementScanner.CompatibleList.append(DeviceCompatibleData)                                                   
                        else:
                            DeviceCompatibleData = DeviceCompatibleJsonDataClass("Group", elements[0])
                            DTFile = GetDTReference(elements[0]) 
                            if DTFile != None:
                                DeviceCompatibleData.DTReference = str(Path(DTFile).absolute()).replace(OBMC_LINUX_SOURCE_DOC_DIR,"")
                            CurrentDeviceElementScanner.CompatibleList.append(DeviceCompatibleData)                                                   
                    else:
                        Warning
                        #print(s)
                       
    DeviceDataList.append(CurrentDeviceElementScanner)

    return 

def AddInterfaceList(interface, jsonData):
    if len(InterfaceList) == 0: 
        devicelistinfo = DeviceListInfoClass(interface, jsonData)        
        InterfaceList.append(devicelistinfo)
    else:
        found = False
        for intf in InterfaceList:
            if intf.DeviceInfo == interface:
                intf.Count += 1
                found = True
        if found == False:
            devicelistinfo = DeviceListInfoClass(interface, jsonData)
            InterfaceList.append(devicelistinfo)

def AddDeviceTypeList(devicetype, jsonDataRecord):
    if len(DeviceTypeList) == 0: 
        devicelistinfo = DeviceListInfoClass(devicetype, jsonDataRecord)
        DeviceTypeList.append(devicelistinfo)
    else:
        found = False
        for devtype in DeviceTypeList:
            if devtype.DeviceInfo == devicetype:
                devtype.Count += 1
                found = True
        if found == False:
            devicelistinfo = DeviceListInfoClass(devicetype, jsonDataRecord)
            DeviceTypeList.append(devicelistinfo)

    return

def AddDeviceList(device, jsonDataRecord):
    if len(DeviceList) == 0: 
        deviceinfo = DeviceListInfoClass(device, jsonDataRecord)
        DeviceList.append(deviceinfo)
    else:
        found = False
        for dev in DeviceList:
            if dev.DeviceInfo == device:
                dev.Count += 1
                found = True
        if found == False:
            deviceinfo = DeviceListInfoClass(device, jsonDataRecord)
            DeviceList.append(deviceinfo)
    return

def AddManufacturerList(mfg, jsonDataRecord):
    if len(ManufacturerList) == 0: 
        mfginfo = DeviceListInfoClass(mfg, jsonDataRecord)
        ManufacturerList.append(mfginfo)
    else:
        found = False
        for m in ManufacturerList:
            if m.DeviceInfo == mfg:
                m.Count += 1
                found = True
        if found == False:
            mfginfo = DeviceListInfoClass(mfg, jsonDataRecord)
            ManufacturerList.append(mfginfo)
    return

def AddCompatibilityDeviceList(device, jsonDataRecord):
    if len(CompatibilityDeviceList) == 0: 
        compdevinfo = DeviceListInfoClass(device, jsonDataRecord)
        CompatibilityDeviceList.append(compdevinfo)
    else:
        found = False
        for m in CompatibilityDeviceList:
            if m.DeviceInfo == device:
                m.Count += 1
                found = True
        if found == False:
            compdevinfo = DeviceListInfoClass(device, jsonDataRecord)
            CompatibilityDeviceList.append(compdevinfo)
    return

def GenerateDeviceCatalogDBFromJson():    
    global DeviceGeneratedJsonList
    global LinuxVersion
    data_record_count = 0
    dCatalogFile = open(os.path.join(OBMC_DEVICE_DB_DIR,"DeviceCatalogDB.json"), "r")
    data = json.load(dCatalogFile)
    LinuxVersion = data["LinuxVersion"]
    DevCatalog = data["DeviceCatalogDatabase"]
    if DevCatalog != None: 
        DeviceDataList = []                
        for i in progressbar(range(len(DevCatalog)), "Reading Device Catalog : ", 100):
        #for i in range(0, len(DevCatalog)):
            DevEntry = DevCatalog[i]
            if type(DevEntry) is dict:
                DeviceScannerElement = DeviceScannerElementClass()
                DeviceScannerElement.FileName = DevEntry.get("FileName");
                DeviceScannerElement.DeviceType = DevEntry.get("DeviceType");
                AddDeviceTypeList(DeviceScannerElement.DeviceType, DeviceScannerElement)
                DeviceScannerElement.Description = DevEntry.get("Description");
                DeviceScannerElement.DriverInformation = DevEntry.get("DriverInformation");
                if len(DevEntry.get("Devices")) != 0 :
                    for j in range(0, len(DevEntry.get("Devices"))):
                        DeviceEntry = DevEntry.get("Devices")[j]
                        DeviceInfo = DeviceInfoClass(DeviceEntry.get("InterfaceType"), DeviceEntry.get("DeviceID"))
                        AddInterfaceList(DeviceInfo.InterfaceType, DeviceScannerElement)
                        AddDeviceList(DeviceInfo.DeviceID, DeviceScannerElement)
                        DeviceScannerElement.DeviceInfoList.append(DeviceInfo)
                if len(DevEntry.get("Compatible")) != 0 :
                    for j in range(0, len(DevEntry.get("Compatible"))):
                        CompatibleEntry = DevEntry.get("Compatible")[j]
                        CompatibleInfo = DeviceCompatibleJsonDataClass(CompatibleEntry.get("Manufacturer"), CompatibleEntry.get("DeviceName"))
                        AddManufacturerList(CompatibleInfo.Manufacturer, DeviceScannerElement)
                        AddCompatibilityDeviceList(CompatibleInfo.DeviceName, DeviceScannerElement)
                        DeviceScannerElement.CompatibleList.append(CompatibleInfo)
                DeviceDataList.append(DeviceScannerElement)
        print("Device Database: Generated Records ", len(DeviceDataList))
        print("Device Database: Interface List ", len(InterfaceList), "DeviceType List :", len(DeviceTypeList), "Device List : ", len(DeviceList), "Manufacturer List : ", len(ManufacturerList), "Compatibility Device List : ", len(CompatibilityDeviceList))

def GetLinuxVersion():
    return LinuxVersion

def SearchDeviceCatalogDB(recordPattern):
    print(len(DeviceGeneratedJsonList))
    for deviceJson in DeviceGeneratedJsonList:
        for jsonData in deviceJson.JsonData.Devices:
            jsonData.searchRecord(recordPattern)
    