# OpenBMC Device Checker Utility
 
 This utility can be used by OpenBMC firmware engineers, platform builders to check which of the devices are supported, including capability to search by interfaces, devices and manufacturers

## Rationale 
1. Information regarding the supported firmware devices are not available to platform developers during platform design phase increasing the firmware development time and cost due to unsupported device choices
2. OpenBMC firmware team awareness to the device choices of the platform design is essential to utilize the device features effectively

## Impact 
1. Informed device choices for platform design
2. Allows firmware developers to discuss the choices and the available device support 

## Version Information 

### 1.0 
- List, search supported H/W interfaces, devices and manufacturers including list of compatible devices
- List compatible devices
- List and search drivers and relate to devices
- Builds Device Catalog Database based on different OpenBMC Linux 
- Related Driver Documentation (Will provide more information in next release) 
- Related Device Tree Information (Will provide more information in next release)


## About the Tool 

The tool utilizes the OpenBMC Linux drivers and documentation to build a Device Catalog that is utilized for search operations. The current tool is based on Linux 6.0.3

### Tool Setup 

Set up the Linux Source Directory, this is only required if the Device Catalog needs to be rebuilt otherwise ignore this step
``export OBMC_LINUX_SOURCE_DIR=/home/hari/github/LinuxSource/linux-dev-6.0/

### Tool Usage 

```
    $ ./devcheck_main.py
    Welcome to OpenBMC Device Check Utility
    Device Database: Initializing Device Database ...
    Reading Device Catalog : [####################################################################################################] 4913/4913
    Device Database: Generated Records  4913
    Device Database: Interface List  40 DeviceType List : 814 Device List :  5029 Manufacturer List :  372 Compatibility Device List :  7291
    Device Database: Ready ...
    CLI started ...
    type help to get started ...
    Device Check CLI >> help
    Commands and Options:
            version  <options>                             Version Info
            database <options>                             Device Database
            list     <options>                             List Options
            search   <device/mfg/devicetypes/interfaces>   Search Options
            device   <device>                              Device Options
            driver   <options>                             Driver Options
            cfg      <options>                             Configuration Options
    Device Check CLI >> version help
    Version Options:
            tool               Tool Version
            linux             Linux Version
    Device Check CLI >> database help
    Database Options:
            build             Build Device Database
            update            Update Device Database
            stats             Stats Device Database
            help              Help
    Device Check CLI >> list help
    List Options:
            interfaces        List Interfaces
            devicetypes       List Device Types
            device            List Devices
            mfg               List Manufacturers
            help              Help
    Device Check CLI >> search help
    Search Options:
            search  <device/mfg/devicetypes/interfaces>   Search Options
    Device Check CLI >> device help
    Device Options:
            devicename        Device Name
            help              Help
    Device Check CLI >> driver help
    Driver Options:
            devicename        Device Name Info
            help              Help
    Device Check CLI >> cfg help
    Configuration Options:
            wdir              Set Working Directory
    Device Check CLI >>

```

## Notes for Users 

### For Platform Builders 
The tool already has a default Device Catalog that is built based on the latest OpenBMC Source base, and unless there is a need for rebuilding database 

### For Firmware Developers 
The tool can be used by firmware developers to check the platform design devices and their configuration options




 

