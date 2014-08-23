# Morula

Morula is a secure replacement of Zygote to fortify weakened ASLR on Android.

# Paper

- [From Zygote to Morula: Fortifying Weakened ASLR on Android](http://www.cc.gatech.edu/~blee303/paper/morula.pdf), IEEE Symposium on Security and Privacy (Oakland) 2014

# How to download Android and patch/build Morula
Morula makes changes on three different repositories of Android 4.2.1, and forked github repositories for Morula are
- `libcore` - https://github.com/lifeasageek/platform_libcore
- `dalvik` - https://github.com/lifeasageek/platform_dalvik
- `frameworks/base` - https://github.com/lifeasageek/platform_frameworks_base

Following is a step by step guide to download Android (4.2) and patch/build Morula.
### Download AOSP
```sh
$ repo init -u https://android.googlesource.com/platform/manifest -b android-4.2.1_r1
$ repo sync
```
See http://source.android.com/source/downloading.html for more details.

### Patch AOSP with Morula
```sh
$ (cd libcore && git remote add github-morula git@github.com:lifeasageek/platform_libcore.git && git pull github-morula morula)
$ (cd dalvik && git remote add github-morula git@github.com:lifeasageek/platform_dalvik.git && git pull github-morula morula)
$ (cd frameworks/base && git remote add github-morula git@github.com:lifeasageek/platform_frameworks_base.git && git pull github-morula morula)
```

### Download the vendor binaries

### Build (Galaxy Nexus, maguro)
```sh
$ . build/envsetup.sh
$ lunch full_maguro-userdebug
$ make -j8
```
See https://source.android.com/source/building-devices.html for more details.

### Flash the image into a device
```
$ adb reboot bootloader
$ fastboot flashall -w
```

# How to activate Morula
Morula can be activated by appending following system properties in `/system/build.prop`.
- `PROCESS_CREATE_MODEL=[zygote|wrap|morula]`
    - Specify which process creation model to use.
- `ON_DEMAND_PRELOAD=yes`
    - Enable on-demand preloading.

These properties can be easily set using the provided script `morula_property_setup.py`.

```sh
$ ./morula_property_setup.py
Usage: morula_property_setup.py [options]

Options:
  -h, --help                   show this help message and exit
  -m MORULA, --morula=MORULA   Enable Morula model
  -z ZYGOTE, --zygote=ZYGOTE   Enable Zygote model
  -w WRAP, --wrap=WRAP         Enable Wrap model
  -d DEMAND, --demand=DEMAND   (optimization) on-demand preloading
  -n NATIVE, --native=NATIVE   (optimization) randomize only native apps
                                                                                                            
```
