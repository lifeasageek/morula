# Morula

Morula is a secure replacement of Zygote to fortify weakened ASLR on Android.
Please refer the paper, , for more details.

# How to download/build Morula

## Download AOSP
```sh
repo init -u https://android.googlesource.com/platform/manifest -b android-4.2.1_r1
repo sync
```

Refer http://source.android.com/source/downloading.html for more details


## Patch AOSP with Morula
```sh
(cd libcore && git remote add github-morula git@github.com:lifeasageek/platform_libcore.git && git pull github-morula morula)
(cd dalvik && git remote add github-morula git@github.com:lifeasageek/platform_dalvik.git && git pull github-morula morula)
(cd frameworks/base && git remote add github-morula git@github.com:lifeasageek/platform_frameworks_base.git && git pull github-morula morula)
```

## Download the vendor binaries

## Build (Galaxy Nexus, maguro)
```sh
. build/envsetup.sh
lunch full_maguro-userdebug
make -j8
```

## Flash the image into a device
```
adb reboot bootloader
fastboot flashall -w
```

# How to activate Morula
