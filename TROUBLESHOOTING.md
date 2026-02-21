# GSI Troubleshooting Guide

This guide helps you resolve common issues when working with GSI images.

## Table of Contents
1. [Device Detection Issues](#device-detection-issues)
2. [Extraction Issues](#extraction-issues)
3. [Build Issues](#build-issues)
4. [Flashing Issues](#flashing-issues)
5. [Boot Issues](#boot-issues)
6. [Performance Issues](#performance-issues)

---

## Device Detection Issues

### ADB Device Not Found

**Symptoms:**
- `adb devices` shows no devices
- "Device not found" error

**Solutions:**

1. **Enable USB Debugging**
   ```
   Settings → About Phone → Tap Build Number 7 times
   Settings → System → Developer Options → Enable USB Debugging
   ```

2. **Check USB Connection**
   - Use original USB cable
   - Try different USB port (preferably USB 3.0)
   - Avoid USB hubs

3. **Restart ADB Server**
   ```bash
   adb kill-server
   adb start-server
   adb devices
   ```

4. **Install Drivers (Windows)**
   - Install Google USB Driver
   - Install manufacturer-specific drivers

5. **Check USB Mode**
   - Set USB mode to "File Transfer" or "MTP"
   - Try "PTP" mode if MTP doesn't work

### Unauthorized Device

**Symptoms:**
- Device shows as "unauthorized"

**Solution:**
1. Disconnect USB
2. Revoke USB debugging authorizations:
   ```
   Developer Options → Revoke USB debugging authorizations
   ```
3. Reconnect USB
4. Accept authorization prompt on device

### Fastboot Device Not Found

**Symptoms:**
- `fastboot devices` shows no devices
- Device in fastboot mode but not detected

**Solutions:**

1. **Windows: Install Fastboot Drivers**
   - Download Google USB Driver
   - Update driver in Device Manager

2. **Linux: Fix Permissions**
   ```bash
   # Add user to plugdev group
   sudo usermod -aG plugdev $USER

   # Create udev rule
   echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="18d1", MODE="0666", GROUP="plugdev"' | sudo tee /etc/udev/rules.d/51-android.rules

   # Reload rules
   sudo udevadm control --reload-rules
   sudo udevadm trigger
   ```

3. **Try Different USB Port/Cable**

---

## Extraction Issues

### "Failed to Extract Firmware"

**Symptoms:**
- Extraction process fails
- Corrupted output files

**Solutions:**

1. **Verify Firmware Integrity**
   ```bash
   # Check MD5/SHA256 checksum
   md5sum firmware.zip
   sha256sum firmware.zip

   # Compare with official checksum
   ```

2. **Check Disk Space**
   ```bash
   df -h
   # Ensure at least 20GB free
   ```

3. **Redownload Firmware**
   - Delete corrupted file
   - Download again from official source
   - Use stable internet connection

4. **Check File Permissions**
   ```bash
   chmod 644 firmware.zip
   ```

### "Unknown Firmware Type"

**Symptoms:**
- Tool cannot detect firmware format

**Solutions:**

1. **Check File Extension**
   ```bash
   file firmware_file
   ```

2. **Manual Extraction**
   - Identify format from manufacturer
   - Use appropriate tool manually

3. **Rename File**
   - Some files may have wrong extension
   - Try renaming to correct extension

### Payload Extraction Fails

**Symptoms:**
- payload-dumper-go fails
- payload.bin not extracted

**Solutions:**

1. **Use Alternative Tools**
   ```bash
   # Python payload dumper
   python3 extract_android_ota_payload.py payload.bin output/
   ```

2. **Check Payload Version**
   - Some devices use proprietary payload format
   - Try manufacturer-specific tools

### OZIP Decryption Fails

**Symptoms:**
- Cannot decrypt Oppo/Realme OZIP

**Solutions:**

1. **Update ozipdecrypt**
   ```bash
   cd oppo_ozip_decrypt
   git pull
   pip3 install -r requirements.txt
   ```

2. **Check AES Keys**
   - Some devices use custom keys
   - Search for device-specific keys

---

## Build Issues

### "Failed to Mount System Image"

**Symptoms:**
- Cannot mount system.img
- Mount permission denied

**Solutions:**

1. **Check Image Format**
   ```bash
   file system.img
   ```

2. **Convert Sparse to Raw**
   ```bash
   simg2img system.img system_raw.img
   ```

3. **Use sudo**
   ```bash
   sudo mount -o loop system.img mount_dir/
   ```

4. **Check Kernel Support**
   ```bash
   # Ensure loop device support
   lsmod | grep loop
   ```

### "Insufficient Disk Space"

**Symptoms:**
- Build fails with disk space error

**Solutions:**

1. **Free Up Space**
   ```bash
   # Clean temporary files
   rm -rf /tmp/*
   rm -rf ~/.cache/*

   # Clean work directory
   rm -rf ~/GSI_Tools/firmware/*
   ```

2. **Use External Storage**
   - Mount external drive
   - Update work directory path

3. **Increase Partition Size**
   - Resize partition if using VM
   - Use LVM for dynamic resizing

### "make_ext4fs Not Found"

**Symptoms:**
- Command not found error

**Solutions:**

1. **Install android-tools-fsutils**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install android-tools-fsutils

   # Or build from source
   git clone https://android.googlesource.com/platform/system/extras
   cd extras/ext4_utils
   make
   sudo make install
   ```

2. **Use Alternative**
   ```bash
   # Use mke2fs instead
   mke2fs -t ext4 -L system system.img <size>
   ```

---

## Flashing Issues

### "Failed to Flash System"

**Symptoms:**
- Fastboot flash fails
- "Partition not found" error

**Solutions:**

1. **Check Partition Name**
   ```bash
   fastboot getvar all | grep partition
   ```

2. **Use Correct Slot (A/B devices)**
   ```bash
   fastboot flash system_a system.img
   # or
   fastboot flash system_b system.img
   ```

3. **Flash in Fastbootd Mode**
   ```bash
   fastboot reboot fastboot
   fastboot flash system system.img
   ```

### "Image Too Large"

**Symptoms:**
- "Image size larger than target device"

**Solutions:**

1. **Delete Logical Partitions**
   ```bash
   fastboot reboot fastboot
   fastboot delete-logical-partition product
   fastboot delete-logical-partition product_a
   fastboot delete-logical-partition product_b
   fastboot delete-logical-partition system_ext
   fastboot delete-logical-partition system_ext_a
   fastboot delete-logical-partition system_ext_b
   ```

2. **Use Smaller GSI**
   - Find smaller GSI build
   - Build GSI with fewer apps

3. **Resize Super Partition** (Advanced)
   - Requires repartitioning
   - High risk of bricking

### "Anti-Rollback Error"

**Symptoms:**
- "Anti-rollback check failed"

**Solutions:**

1. **Check Current Version**
   ```bash
   fastboot getvar current-slot
   fastboot getvar version-bootloader
   ```

2. **Update to Latest Stock**
   - Flash latest stock ROM first
   - Then flash GSI

3. **Disable Anti-Rollback** (Not recommended)
   - May require bootloader unlock
   - Can brick device

### "Verity/Verification Error"

**Symptoms:**
- "Verity check failed"
- Device won't boot after flash

**Solutions:**

1. **Flash vbmeta with Disabled Verification**
   ```bash
   fastboot --disable-verity --disable-verification flash vbmeta vbmeta.img
   ```

2. **Flash vbmeta_system**
   ```bash
   fastboot --disable-verity --disable-verification flash vbmeta_system vbmeta_system.img
   ```

3. **Flash Empty vbmeta**
   ```bash
   # Create empty vbmeta
   dd if=/dev/zero of=vbmeta_empty.img bs=1 count=1
   fastboot flash vbmeta vbmeta_empty.img
   ```

---

## Boot Issues

### Stuck at Boot Logo

**Symptoms:**
- Device stuck at manufacturer logo
- Boot animation loops

**Solutions:**

1. **Wait Longer**
   - First boot can take 5-15 minutes
   - Be patient, don't interrupt

2. **Factory Reset**
   ```bash
   fastboot -w
   # or
   fastboot erase userdata
   ```

3. **Wipe Cache**
   ```bash
   fastboot erase cache
   fastboot erase dalvik-cache
   ```

4. **Flash Correct Vendor**
   - GSI needs matching vendor partition
   - Flash stock vendor if incompatible

### Bootloop (Continuous Reboot)

**Symptoms:**
- Device keeps rebooting
- Cannot reach system

**Solutions:**

1. **Check Vendor Compatibility**
   - Wrong vendor causes bootloop
   - Flash correct vendor version

2. **Check GSI Type**
   ```bash
   # Verify architecture
   adb shell getprop ro.product.cpu.abi

   # Verify binder
   adb shell getprop ro.product.cpu.abilist
   ```

3. **Use Different GSI**
   - Try different GSI variant
   - Check phhusson's GSI list

4. **Flash Stock and Retry**
   - Restore stock ROM
   - Try different GSI build

### "No OS Installed" Error

**Symptoms:**
- Recovery shows "No OS installed"

**Solutions:**

1. **Reflash System**
   ```bash
   fastboot flash system system.img
   ```

2. **Check Slot**
   ```bash
   fastboot getvar current-slot
   fastboot set_active a
   ```

3. **Flash Boot**
   ```bash
   fastboot flash boot boot.img
   ```

### Black Screen After Boot

**Symptoms:**
- Device boots but screen is black
- Backlight is on

**Solutions:**

1. **Wait for Initialization**
   - Some GSIs take time to initialize display
   - Wait 5-10 minutes

2. **Different GSI**
   - Try GSI with better device support
   - Check device-specific overlays

3. **Check Logs**
   ```bash
   adb logcat | grep -i display
   adb logcat | grep -i surface
   ```

---

## Performance Issues

### Slow Performance

**Symptoms:**
- Laggy UI
- Slow app launches

**Solutions:**

1. **Disable Animations**
   ```bash
   adb shell settings put global window_animation_scale 0
   adb shell settings put global transition_animation_scale 0
   adb shell settings put global animator_duration_scale 0
   ```

2. **Clear Cache**
   ```bash
   adb shell pm trim-caches 1G
   ```

3. **Use Different GSI**
   - Some GSIs are optimized better
   - Try AOSP-based vs custom ROM-based

### Battery Drain

**Symptoms:**
- Fast battery drain
- Overheating

**Solutions:**

1. **Check Wake Locks**
   ```bash
   adb shell dumpsys power | grep -i wake
   ```

2. **Disable Unused Services**
   ```bash
   adb shell pm disable-user com.google.android.gms
   ```

3. **Use Battery Optimization**
   - Enable Doze mode
   - Restrict background apps

### No Mobile Data/Calls

**Symptoms:**
- No cellular service
- Cannot make calls

**Solutions:**

1. **Check APN Settings**
   - Settings → Network → Mobile Network → APN
   - Add correct APN for carrier

2. **Flash Correct Vendor**
   - Vendor partition contains modem firmware
   - Use stock vendor or compatible vendor

3. **Check IMEI**
   ```bash
   adb shell service call iphonesubinfo 1
   ```

### Camera Not Working

**Symptoms:**
- Camera app crashes
- Black camera preview

**Solutions:**

1. **Install GCam**
   - Google Camera ports often work better
   - Try different GCam versions

2. **Grant Permissions**
   ```bash
   adb shell pm grant com.android.camera2 android.permission.CAMERA
   ```

3. **Check SELinux**
   ```bash
   adb shell getenforce
   adb shell setenforce 0  # Temporary permissive
   ```

---

## Recovery Methods

### Hard Brick Recovery

If device is completely unresponsive:

1. **Use Manufacturer Tool**
   - Samsung: Odin
   - Xiaomi: MiFlash
   - OnePlus: MSM Download Tool
   - Motorola: blankflash

2. **EDL Mode** (Qualcomm devices)
   - Short EDL test points
   - Use QPST/QFIL to flash

3. **SP Flash Tool** (MediaTek devices)
   - Use MTK bypass if needed
   - Flash with scatter file

### Soft Brick Recovery

If device boots to recovery/fastboot:

1. **Flash Stock ROM**
   ```bash
   fastboot flash boot boot.img
   fastboot flash system system.img
   fastboot flash vendor vendor.img
   fastboot -w
   fastboot reboot
   ```

2. **Factory Reset**
   - Boot to recovery
   - Wipe data/factory reset

3. **Restore Backup**
   - Flash boot backup
   - Flash system backup

---

## Getting Help

If issues persist:

1. **Check Logs**
   ```bash
   adb logcat > log.txt
   adb shell dmesg > dmesg.txt
   ```

2. **Search Forums**
   - XDA Developers
   - Device-specific Telegram groups
   - Reddit r/AndroidRoot

3. **Provide Information**
   - Device model
   - Android version
   - GSI name/version
   - Error messages
   - Log files

---

**Remember**: Always backup before making changes. Keep stock firmware available for recovery.
