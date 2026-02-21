# GSI Resources and References

This document contains useful resources, links, and references for working with GSI images.

## Official Documentation

### Android Project Treble
- [Project Treble Overview](https://source.android.com/docs/core/architecture/vndk)
- [Generic System Images](https://source.android.com/docs/core/tests/vts/gsi)
- [Treble Compliance](https://source.android.com/docs/compatibility/vintf)

### Android Build System
- [AOSP Build Guide](https://source.android.com/docs/setup/build/building)
- [GSI Build Targets](https://source.android.com/docs/core/tests/vts/gsi#build-targets)

## GSI Sources

### Official/Stable GSIs

#### phhusson's Treble Experimentations
- **GitHub**: https://github.com/phhusson/treble_experimentations
- **Downloads**: https://github.com/phhusson/treble_experimentations/releases
- **Wiki**: https://github.com/phhusson/treble_experimentations/wiki
- **Features**:
  - Pure AOSP-based
  - Wide device compatibility
  - Regular updates
  - Fixes for common issues

#### Ponces' Treble AOSP
- **GitHub**: https://github.com/ponces/treble_aosp
- **Downloads**: https://github.com/ponces/treble_aosp/releases
- **Features**:
  - Android 12/13/14 GSIs
  - Clean AOSP experience
  - Good stability

#### ErfanGSIs
- **GitHub**: https://github.com/erfanoabdi/ErfanGSIs
- **Features**:
  - OEM porting tool
  - Convert stock ROMs to GSI
  - Support for many OEM skins

### Custom ROM GSIs

#### LineageOS GSI
- **Source**: https://github.com/LineageOS
- **Downloads**: Check XDA forums
- **Features**:
  - LineageOS features
  - Privacy-focused
  - Regular security updates

#### Pixel Experience GSI
- **Website**: https://download.pixelexperience.org/
- **Features**:
  - Pixel-like experience
  - Google Pixel features
  - Regular updates

#### crDroid GSI
- **Website**: https://crdroid.net/
- **Features**:
  - Customization options
  - Performance optimizations
  - Regular updates

### Specialized GSIs

#### LeOS GSI
- **Telegram**: https://t.me/LeOS_Support
- **Features**:
  - Lightweight
  - Privacy-focused
  - Minimal bloat

#### AOSP Extended GSI
- **GitHub**: https://github.com/AospExtended
- **Features**:
  - Extended AOSP features
  - Customization options

## Tools and Utilities

### Extraction Tools

#### payload-dumper-go
- **GitHub**: https://github.com/ssut/payload-dumper-go
- **Purpose**: Extract payload.bin from OTA updates
- **Features**: Fast, parallel extraction

#### sdat2img / img2sdat
- **GitHub**: https://github.com/xpirt/sdat2img
- **Purpose**: Convert between .dat and .img formats

#### oppo_ozip_decrypt
- **GitHub**: https://github.com/bkerler/oppo_ozip_decrypt
- **Purpose**: Decrypt Oppo/Realme OZIP files

### Partition Tools

#### lpunpack / lpmake / lpdump
- **Source**: Android Open Source Project
- **Purpose**: Dynamic partition management
- **Installation**: Build from AOSP or download from Android CI

#### simg2img / img2simg
- **Source**: Android Open Source Project
- **Purpose**: Sparse image conversion
- **Installation**: `android-tools-fsutils` package

### Flashing Tools

#### Fastboot / ADB
- **Source**: Android SDK Platform Tools
- **Download**: https://developer.android.com/studio/releases/platform-tools

#### Odin (Samsung)
- **Source**: Samsung official tool
- **Download**: Various versions available

#### MiFlash (Xiaomi)
- **Source**: Xiaomi official tool
- **Download**: https://miui.com/download.html

#### SP Flash Tool (MediaTek)
- **Source**: MediaTek
- **Download**: Various versions

## Information Resources

### Device Compatibility

#### Treble Info App
- **F-Droid**: https://f-droid.org/en/packages/tk.hack5.treblecheck/
- **Google Play**: https://play.google.com/store/apps/details?id=tk.hack5.treblecheck
- **Purpose**: Check device Treble compatibility

#### Treble Check App
- **Google Play**: https://play.google.com/store/apps/details?id=com.kevintresuelo.treblecheck
- **Purpose**: Check Treble, VNDK, architecture info

### Community Resources

#### XDA Developers Forums
- **Project Treble Section**: https://xdaforums.com/c/project-treble.7259/
- **GSI List Thread**: https://xdaforums.com/t/treble-gsis-list.4691348/
- **Ultimate GSI Guide**: https://xdaforums.com/t/ultimate-gsi-guide.4695349/

#### Telegram Groups
- **GSI Discussion**: Search for "GSI" or your device model
- **Device-specific groups**: Usually named after device model

#### Reddit
- **r/AndroidRoot**: https://www.reddit.com/r/AndroidRoot/
- **r/ProjectTreble**: https://www.reddit.com/r/ProjectTreble/

### Databases

#### GitHub GSI List
- **Repository**: https://github.com/phhusson/treble_experimentations/wiki/Generic-System-Image-(GSI)-list
- **Features**: Comprehensive list of GSIs

#### Treble Device Database
- **Website**: Various community-maintained lists
- **Purpose**: Check device Treble compatibility

## Firmware Sources

### Official Firmware

#### Samsung
- **SamFW**: https://samfw.com/
- **Frija Tool**: Download official firmware
- **SamMobile**: https://www.sammobile.com/

#### Xiaomi
- **MiFirm**: https://mifirm.net/
- **Xiaomi Firmware Updater**: https://xiaomifirmwareupdater.com/

#### OnePlus
- **Official**: https://www.oneplus.com/support/softwareupgrade
- **OxygenOS**: https://oxygenos.oneplus.com/

#### Google Pixel
- **Factory Images**: https://developers.google.com/android/images
- **OTA Images**: https://developers.google.com/android/ota

#### Motorola
- **Official**: https://motorola-global-portal.custhelp.com/

#### Sony
- **Xperia Firmware**: https://xperiafirmware.com/

### Third-Party Firmware

#### Firmware.mobi
- **Website**: https://firmware.mobi/
- **Features**: Multiple device firmwares

#### Needrom
- **Website**: https://www.needrom.com/
- **Features**: Various device firmwares

## Development Resources

### Building GSI from Source

#### AOSP Source
```bash
# Initialize repo
repo init -u https://android.googlesource.com/platform/manifest -b android-14.0.0_r1

# Sync source
repo sync -c -j$(nproc)

# Build GSI
source build/envsetup.sh
lunch gsi_arm64-userdebug
make -j$(nproc) systemimage
```

#### GSI Branches
- `android-10.0.0_rXX` - Android 10
- `android-11.0.0_rXX` - Android 11
- `android-12.0.0_rXX` - Android 12
- `android-12.1.0_rXX` - Android 12L
- `android-13.0.0_rXX` - Android 13
- `android-14.0.0_rXX` - Android 14
- `android-15.0.0_rXX` - Android 15

### Vendor Interface

#### VNDK Documentation
- **VNDK Design**: https://source.android.com/docs/core/architecture/vndk
- **VNDK Changes**: https://source.android.com/docs/core/architecture/vndk/versions

#### HIDL/AIDL
- **HIDL**: https://source.android.com/docs/core/architecture/hidl
- **AIDL**: https://source.android.com/docs/core/architecture/aidl

## Troubleshooting Resources

### Log Analysis

#### ADB Logcat
```bash
# Full log
adb logcat

# Filter by tag
adb logcat -s TAG_NAME:D

# Save to file
adb logcat -d > log.txt
```

#### Kernel Logs
```bash
# Dmesg
adb shell dmesg

# Last kmsg
adb shell cat /proc/last_kmsg
```

### Common Fixes

#### Fix Mobile Data
```bash
# Reset APN
adb shell settings put global mobile_data 1
```

#### Fix Bluetooth
```bash
# Clear Bluetooth data
adb shell pm clear com.android.bluetooth
```

#### Fix Camera
```bash
# Grant permissions
adb shell pm grant com.android.camera2 android.permission.CAMERA
```

## YouTube Channels

### GSI/Treble Content
- **Various creators**: Search "GSI Android" or "Project Treble"
- **Device-specific guides**: Search your device model + "GSI"

## Contributing

### How to Contribute
1. Test GSIs on your device
2. Report bugs with logs
3. Share working configurations
4. Help others in forums

### Documentation
- Update wikis with device info
- Write guides for your device
- Share fixes and workarounds

---

**Note**: This is a community-maintained list. If you find broken links or want to add resources, please submit an update.

**Last Updated**: 2024
