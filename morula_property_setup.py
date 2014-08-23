#!/usr/bin/python

from optparse import OptionParser
import os
import time

def usage(parser):
    print parser.print_help()
    return
    
def parseArg():
    parser = OptionParser()
    parser.add_option("-m", "--morula", help = "Enable Morula model")
    parser.add_option("-z", "--zygote", help = "Enable Zygote model")
    parser.add_option("-w", "--wrap",   help = "Enable Wrap model")
    
    parser.add_option("-d", "--demand", help = "(optimization) on-demand preloading")
    parser.add_option("-n", "--native", help = "(optimization) randomize only native apps")
    
    (opts, args) = parser.parse_args()

    model = None
    onDemandLoad = False
    nativeOpt = False

    if opts.morula is not None:
        model = "morula"
    elif opts.zygote is not None:
        model = "zygote"
    elif opts.wrap is not None:
        model = "wrap"
    else:
        usage(parser)
        exit(-1)

    if opts.demand is not None:
        onDemandLoad = True

    if opts.native is not None:
        nativeOpt = True

    return model, onDemandLoad, nativeOpt

def setPropOption(oldPropFilename, newPropFilename, mode, onDemandLoad):
    oldProps = open(oldPropFilename).read()
    newProps = ""

    reserved = ["PROCESS_CREATE_MODEL",
                "ON_DEMAND_PRELOAD",
                "DUMP_PRELOAD_TS",
                "NATIVE_OPT"]

    # Copy existing properties except Morula related settings.
    for line in oldProps.split("\n"):
        if line == "": continue

        found = [r for r in reserved if r in line]

        # Ignore all previous Morula settings.
        if len(found) > 0:
            continue
        else:
            newProps += line + "\n"


    # Append given Morula settings.
    newProps += "PROCESS_CREATE_MODEL=%s\n" % mode

    if onDemandLoad == True:
        newProps += "ON_DEMAND_PRELOAD=yes\n"

    # NativeOpt can be enabled with .apk files.
    # Commented out for the release.
    # pkgs = nativeApps.getSystemNativePackages()
    # for pkg in pkgs:
    #     newProps += "# nativeopt.%s\n" % (pkg)
    #     newProps += "NATIVE_OPT.%08x=yes\n" % (java_string_hashcode(pkg))
            
    open(newPropFilename, "w").write(newProps)
    return

# Compute the java string hashcode so that the hashed value is deterministic as
# in the Morula deamon.
def java_string_hashcode(s):
    h = 0
    for c in s:
        h = (31 * h + ord(c)) & 0xFFFFFFFF

    v = ((h + 0x80000000) & 0xFFFFFFFF)

    if v > 0x80000000:
        v = v - 0x80000000
    else:
        v = (v + 0x80000000) & 0xFFFFFFFF
    return v

def replaceDeviceProp(model, onDemandLoad, nativeOpt):
    print "[*] Replacing device prop"    
    os.system("adb pull /system/build.prop ./tmp/build.prop.old")
    setPropOption("./tmp/build.prop.old", "./tmp/build.prop.new",
                            model, onDemandLoad)
    os.system("adb shell su -c mount -o rw,remount /system")
    os.system("adb push ./tmp/build.prop.new /sdcard/build.prop")
    os.system("adb shell su -c cp /sdcard/build.prop /system/build.prop")
    os.system("adb shell su -c mount -o ro,remount /system")
    return
    
def rebootDevice():
    print "[*] Reboot the device"
    os.system("adb reboot")
    return

if __name__ == "__main__":
    mode, onDemandLoad, nativeOpt = parseArg()
    replaceDeviceProp(mode, onDemandLoad, nativeOpt)
    rebootDevice()

