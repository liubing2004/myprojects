#!/bin/bash
apk="/home/bliu/dev/program/python/myprojects/user-authentication/platforms/android/build/outputs/apk/android-release-unsigned.apk"
cordova build --release android
keytool -genkey -v -keystore my-release-key.keystore -alias alias_name -keyalg RSA -keysize 2048 -validity 10000
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.keystore  $apk alias_name
zipalign -v 4 $apk Final.apk
