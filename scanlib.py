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

class DeviceInfoClass:
    def __init__(self, interfacetype, deviceid):
        self.InterfaceType = interfacetype
        self.DeviceID = deviceid

class DeviceScannerElementClass: 
    def __init__(self):
        self.FileName = None
        self.DeviceType = ""
        self.Description = ""
        self.DeviceInfoList = []
        self.CompatibleList = []
        self.DriverInformation = ""
        self.DeviceTreeInformation = ""
    
    def print(self):
        print("Driver File Name                    : ", self.FileName)
        print("Device Type                         : ", self.DeviceType)
        print("Description                         : ", self.Description)
        print("DriverInformation                   : ", self.DriverInformation)
        print("DeviceTreeInformation               : ", self.DeviceTreeInformation)
        print("Total Devices Supported             : ", len(self.DeviceInfoList))
        for idx in range(0, len(self.DeviceInfoList)):
            print("%4d. %16s %24s" %(idx, self.DeviceInfoList[idx].InterfaceType, self.DeviceInfoList[idx].DeviceID))
        print("Total Compatible Devices Supported  : ", len(self.CompatibleList))
        for idx in range(0, len(self.CompatibleList)):
            print("%4d. %24s %24s %48s" %(idx, self.CompatibleList[idx].Manufacturer, self.CompatibleList[idx].DeviceName, self.CompatibleList[idx].DTReference))        

class ModuleDeviceClass:
    def __init__(self):
        self.InterfaceType = ""
        self.ModuleDeviceTableId = ""

class ModuleInfoClass: 
    def __init__(self):
        self.ModuleDescription = ""
        self.DRV_NAME = ""
        self.ModuleInfoList = []
        self.ModuleDeviceTableOfId = ""
        self.DeviceScanner = object

class PairClass:
    def __init__(self, K, V):
        self.Key = K
        self.Value = V
        self.VValues = []
    
    def getKey(self):
        return self.Key
    
    def getValue(self):
        return self.Value

class DeviceListInfoClass:
    def __init__(self, deviceInfo, DataRecord):
        self.DeviceInfo = deviceInfo
        self.DataRecord = DataRecord
        self.Count = 1

class DeviceCompatibleJsonDataClass:
    def __init__(self, manufacturer, deviceName):
        self.Manufacturer = str(manufacturer)
        self.DeviceName = str(deviceName)
        self.DTReference = ""

    def getManufacturer(self):
        return self.Manufacturer

    def getDeviceName(self):
        return self.DeviceName

    def setManufacturer(self, Manufacturer):
        self.Manufacturer = Manufacturer

    def setDeviceName(self, DeviceName):
        self.DeviceName = DeviceName    