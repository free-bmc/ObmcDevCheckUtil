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

from devicecatalog import InterfaceList
from devicecatalog import DeviceTypeList
from devicecatalog import DeviceList
from devicecatalog import ManufacturerList
from devicecatalog import CompatibilityDeviceList
from devicecatalog import ProcessDatabase
from devicecatalog import GetLinuxVersion

from utils import progressbar

def process_list(selection):
    if selection == "interfaces":
        count = 1
        for intf in InterfaceList:
            if count % 4 == 0:
                print("%16s" %intf.DeviceInfo)
            else:
                print("%16s" %intf.DeviceInfo, end=' ')
            count +=1
    elif selection == "devicetypes":
        count = 1
        for dev in DeviceTypeList:
            if count % 3 == 0:
                print("%48s" %dev.DeviceInfo)
            else:
                print("%48s" %dev.DeviceInfo, end=' ')
            count +=1
    elif selection == "device":
        count = 1
        for dev in DeviceList:
            if count % 3 == 0:
                print("%48s" %dev.DeviceInfo)
            else:
                print("%48s" %dev.DeviceInfo, end=' ')
            count +=1
    elif selection == "mfg":
        count = 1
        for dev in ManufacturerList:
            if count % 4 == 0:
                print("%16s" %dev.DeviceInfo)
            else:
                print("%16s" %dev.DeviceInfo, end=' ')
            count +=1
    print("")
                
def process_search(selection):
    found_count = 0

    for i in progressbar(range(len(InterfaceList)), "Searching Interface List : ", 100):
        if selection.lower() in InterfaceList[i].DeviceInfo.lower():
            print("Found %d devices of Interface Type" %InterfaceList[i].Count)
            found_count +=1
    for i in progressbar(range(len(DeviceTypeList)), "Searching Device Type List : ", 100):            
        if selection.lower() in DeviceTypeList[i].DeviceInfo.lower():
            print("Found %d Device Types " %DeviceTypeList[i].Count)
            found_count +=1
    for i in progressbar(range(len(DeviceList)), "Searching Device List : ", 100):            
        if selection.lower() in DeviceList[i].DeviceInfo.lower():
            print("Found in Device List: ", DeviceList[i].DeviceInfo)
            found_count +=1
    for i in progressbar(range(len(ManufacturerList)), "Searching Manufacturer List : ", 100):    
        if selection.lower() in ManufacturerList[i].DeviceInfo.lower():
            print("Found %d Manufacturer Devices " %ManufacturerList[i].Count)
            found_count +=1
    compdeviceCount = 0
    for i in progressbar(range(len(CompatibilityDeviceList)), "Searching Compatibility Device List : ", 100):    
        if selection.lower() in CompatibilityDeviceList[i].DeviceInfo.lower():
            compdeviceCount += 1
            found_count +=1
    if compdeviceCount != 0:
        print("Found %d compatible devices " %compdeviceCount)

    if found_count == 0: 
        print("No Devices Found to match your search")
    
    print("")

def process_device(selection):
    device_list = []
    for i in progressbar(range(len(DeviceList)), "Looking Up to Device List : ", 100):
        if selection.lower() in DeviceList[i].DeviceInfo.lower():
            device_list.append(DeviceList[i])
    
    for device in device_list:
            device.DataRecord.print()

def process_driver(selection):
    device_list = []
    for i in progressbar(range(len(DeviceList)), "Looking Up to Device List : ", 100):
        if selection.lower() in DeviceList[i].DeviceInfo.lower():
            device_list.append(DeviceList[i])
    
    for device in device_list:
            device.DataRecord.print()

def process_cfg(selection):
    print(selection)

def CLIStart(ToolVersion):
    print("CLI started ...")
    print("type help to get started ...")
    while True:
        option = input("Device Check CLI >> ")
        #print(option)
        if option == "quit":
            exit()

        elif option == "help":
            print("Commands and Options:")
            print("\tversion  <options>                             Version Info ")
            print("\tdatabase <options>                             Device Database ")
            print("\tlist     <options>                             List Options ")
            print("\tsearch   <device/mfg/devicetypes/interfaces>   Search Options ")
            print("\tdevice   <device>                              Device Options ")        
            print("\tdriver   <options>                             Driver Options ")        
            print("\tcfg      <options>                             Configuration Options ")        
        elif option.startswith("version"):
            suboption = option.split(" ")
            if len(suboption) == 1 or suboption[1] == "help":         
                print("Version Options:")
                print("\ttool               Tool Version ")
                print("\tlinux             Linux Version ")
            elif suboption[1] == "tool":
                print(ToolVersion)
            elif suboption[1] == "linux":
                print(GetLinuxVersion())
        elif option.startswith("database"):
            suboption = option.split(" ")
            if len(suboption) == 1 or suboption[1] == "help":         
                print("Database Options:")
                print("\tbuild             Build Device Database ")
                print("\tupdate            Update Device Database ")
                print("\tstats             Stats Device Database ")                
                print("\thelp              Help ")
            elif suboption[1] == "update" or suboption[1] == "stats" or suboption[1] == "build":
                print("Database ", suboption[1])
                ProcessDatabase(suboption[1])

        elif option.startswith("list"):
            suboption = option.split(" ")
            if len(suboption) == 1 or suboption[1] == "help":         
                print("List Options:")
                print("\tinterfaces        List Interfaces ")
                print("\tdevicetypes       List Device Types ")
                print("\tdevice            List Devices ")
                print("\tmfg               List Manufacturers ")
                print("\thelp              Help ")
            elif suboption[1] == "interfaces" or suboption[1] == "devicetypes" or suboption[1] == "mfg":
                print("List ", suboption[1])            
                process_list(suboption[1])

        elif option.startswith("search"):
            suboption = option.split(" ")
            if len(suboption) == 1 or suboption[1] == "help":         
                print("Search Options:")
                print("\tsearch  <device/mfg/devicetypes/interfaces>   Search Options ")
            else:
                print("Search ", suboption[1])            
                process_search(suboption[1])

        elif option.startswith("device"):
            suboption = option.split(" ")
            if len(suboption) == 1 or suboption[1] == "help":         
                print("Device Options:")
                print("\tdevicename        Device Name ")
                print("\thelp              Help ")
            else:
                print("Device ", suboption[1])      
                process_device(suboption[1])

        elif option.startswith("driver"):
            suboption = option.split(" ")
            if len(suboption) == 1 or suboption[1] == "help":
                print("Driver Options:")
                print("\tdevicename        Device Name Info ")
                print("\thelp              Help ")
            else:
                process_driver(suboption[1])

        elif option.startswith("cfg"):
            suboption = option.split(" ")
            if len(suboption) == 1 or suboption[1] == "help":         
                print("Configuration Options:")
                print("\twdir              Set Working Directory ")
            elif suboption[1] == "wdir":
                process_cfg(suboption[1])
        else:
            print("Invalid Command")
