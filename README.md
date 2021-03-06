# android-patch-logger

## Description

This is a small macro, which logs different device information every day at 2pm. All information is written to the internal storage, to a file  called .patch_history. In particular, the logged information includes

1.  The current date
2.  The current security patch level of your device
3.  The current kernel version of your device
4.  The current OxygenOS version of your device (only for OnePlus phones)
5.  The current android version of your device
6.  The build date of the most recent update

Each line in the file .patch_history then looks similar to this (this example comes straight from a OnePlus 6T)

2020-08-13 2020-07-01 4.9.179-perf+ 10 10.3.5 200717

For reference, the full command is

```
echo $(date +%Y-%m-%d) $(getprop ro.build.version.security_patch) $(uname -r) $(getprop ro.build.version.release) $(getprop ro.oxygen.version) $(getprop ro.build.date.Ymd) >> /sdcard/.patch_history
```

## Installation

Install [MacroDroid](https://play.google.com/store/apps/details?id=com.arlosoft.macrodroid&hl=en_US) from the PlayStore and download the .macro file from this git repository. Afterwards use your favorite file explorer to click on the .macro file and select open with MacroDroid. This should open the respective macro and allow you to save it. Afterwards, simply let MacroDroid do its job. **NOTE**: You might want to disable battery opimization for MacroDroid, in order for the macro to run reliably. Also make sure that storage access is granted to MacroDroid.

## Sharing

After you collected some data on your device, sharing it with the community would be highly appreciated. Simply make a pull request. 
