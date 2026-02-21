# Useful Commands for GSI Flashing

This document contains useful commands for working with GSI images and Android devices.

## ADB Commands

### Basic ADB
```bash
# Check connected devices
adb devices

# Reboot to different modes
adb reboot                    # Normal reboot
adb reboot bootloader         # Reboot to bootloader/fastboot
adb reboot recovery           # Reboot to recovery
adb reboot fastboot           # Reboot to fastbootd (userspace fastboot)

# Shell access
adb shell                     # Interactive shell
adb shell <command>           # Run single command
adb shell su                  # Root shell (if rooted)
```

### File Operations
```bash
# Push file to device
adb push local.file /sdcard/

# Pull file from device
adb pull /sdcard/file.txt ./

# Install APK
adb install app.apk

# Uninstall app
adb uninstall com.package.name
```

### Logcat
```bash
# View logs
adb logcat

# Filter logs
adb logcat -s TAG:*

# Clear logs
adb logcat -c

# Save logs to file
adb logcat > log.txt
```

## Fastboot Commands

### Basic Fastboot
```bash
# Check connected devices
fastboot devices

# Reboot
fastboot reboot
fastboot reboot bootloader
fastboot reboot recovery
fastboot reboot fastboot      # Reboot to fastbootd
```

### Flashing Partitions
```bash
# Flash system
fastboot flash system system.img

# Flash boot
fastboot flash boot boot.img

# Flash vendor
fastboot flash vendor vendor.img

# Flash vbmeta with disabled verification
fastboot --disable-verity --disable-verification flash vbmeta vbmeta.img

# Flash recovery
fastboot flash recovery recovery.img
```

### Erasing Partitions
```bash
# Erase system
fastboot erase system

# Erase data
fastboot erase userdata

# Erase cache
fastboot erase cache

# Erase all (factory reset)
fastboot -w
```

### Dynamic Partitions (Android 10+)
```bash
# List logical partitions
fastboot getvar all | grep partition

# Delete logical partition
fastboot delete-logical-partition product
fastboot delete-logical-partition product_a
fastboot delete-logical-partition product_b

# Resize logical partition
fastboot resize-logical-partition system <size>

# Create logical partition
fastboot create-logical-partition system <size>
```

### Slot Management (A/B Devices)
```bash
# Get current slot
fastboot getvar current-slot

# Set active slot
fastboot set_active a
fastboot set_active b

# Get all slot variables
fastboot getvar all | grep slot
```

## Device Information

### Get Device Properties
```bash
# Basic info
adb shell getprop ro.product.model
adb shell getprop ro.product.manufacturer
adb shell getprop ro.build.version.release
adb shell getprop ro.build.version.sdk

# Treble info
adb shell getprop ro.treble.enabled
adb shell getprop ro.vndk.version

# Architecture
adb shell getprop ro.product.cpu.abi
adb shell getprop ro.product.cpu.abilist

# Partition info
adb shell getprop ro.build.ab_update
adb shell getprop ro.boot.dynamic_partitions
adb shell getprop ro.build.system_root_image
```

### List All Properties
```bash
adb shell getprop
```

## Image Operations

### Sparse Images
```bash
# Convert sparse to raw
simg2img sparse.img raw.img

# Convert raw to sparse
img2simg raw.img sparse.img

# Check sparse image info
simg_dump.py sparse.img
```

### Brotli Compression
```bash
# Decompress .dat.br
brotli --decompress system.new.dat.br -o system.new.dat

# Compress to .br
brotli --compress system.new.dat -o system.new.dat.br
```

### LZ4 Compression
```bash
# Decompress .lz4
lz4 -d file.img.lz4 file.img

# Compress to .lz4
lz4 -B6 --content-size file.img file.img.lz4
```

### DAT Files
```bash
# Convert .dat to .img
python3 sdat2img.py system.transfer.list system.new.dat system.img

# Convert .img to .dat
python3 img2sdat.py system.img -o output_dir
```

## Dynamic Partitions

### Extract from super.img
```bash
# Convert sparse super to raw
simg2img super.img super_raw.img

# Extract partitions
lpunpack super_raw.img output_dir/

# View super partition info
lpdump super_raw.img
```

### Create super.img
```bash
# Create super image
lpmake \
    --metadata-size 65536 \
    --super-name super \
    --metadata-slots 3 \
    --device super:<size> \
    --group main:<size> \
    --partition system:readonly:<size>:main \
    --image system=system.img \
    --partition vendor:readonly:<size>:main \
    --image vendor=vendor.img \
    --sparse \
    --output super.img
```

## Payload.bin Extraction

### Using payload-dumper-go
```bash
# Extract all partitions
payload-dumper-go payload.bin -o output_dir/

# Extract specific partition
payload-dumper-go payload.bin -o output_dir/ -p system

# Extract multiple partitions
payload-dumper-go payload.bin -o output_dir/ -p system -p vendor -p boot
```

## GSI Flashing

### Standard Flashing
```bash
# Reboot to bootloader
adb reboot bootloader

# Flash vbmeta
fastboot --disable-verity --disable-verification flash vbmeta vbmeta.img

# Flash system
fastboot erase system
fastboot flash system system.img

# Wipe and reboot
fastboot -w
fastboot reboot
```

### Dynamic Partitions Flashing
```bash
# Reboot to bootloader
adb reboot bootloader

# Flash vbmeta
fastboot --disable-verity --disable-verification flash vbmeta vbmeta.img

# Reboot to fastbootd
fastboot reboot fastboot

# Delete product partition
fastboot delete-logical-partition product

# Flash system
fastboot erase system
fastboot flash system system.img

# Reboot to recovery
fastboot reboot recovery
# Then factory reset
```

## Troubleshooting

### Check Bootloader Status
```bash
fastboot getvar unlocked
```

### Check Partition Sizes
```bash
fastboot getvar all | grep partition-size
```

### Verify Flash
```bash
# Verify system partition
fastboot getvar partition-size:system
fastboot getvar partition-type:system
```

### Boot to Safe Mode
```bash
# From powered off state
# Hold Power + Volume Down until boot logo appears
# Then release Power but keep holding Volume Down
```

## Backup and Restore

### Backup Partitions
```bash
# Backup boot
adb shell su -c "dd if=/dev/block/bootdevice/by-name/boot of=/sdcard/boot.img"
adb pull /sdcard/boot.img ./

# Backup recovery
adb shell su -c "dd if=/dev/block/bootdevice/by-name/recovery of=/sdcard/recovery.img"
adb pull /sdcard/recovery.img ./

# Backup system (requires root)
adb shell su -c "dd if=/dev/block/bootdevice/by-name/system of=/sdcard/system.img"
adb pull /sdcard/system.img ./
```

### Restore Partitions
```bash
# Flash backup
fastboot flash boot boot_backup.img
fastboot flash recovery recovery_backup.img
```

## Script Examples

### Automated Flash Script
```bash
#!/bin/bash
GSI_IMG="system.img"
VBMETA_IMG="vbmeta.img"

echo "Flashing GSI..."
adb reboot bootloader
sleep 5

fastboot --disable-verity --disable-verification flash vbmeta "$VBMETA_IMG"
fastboot reboot fastboot
sleep 5

fastboot delete-logical-partition product
fastboot erase system
fastboot flash system "$GSI_IMG"
fastboot reboot recovery

echo "Done! Please factory reset in recovery."
```

### Device Info Script
```bash
#!/bin/bash
echo "=== Device Information ==="
echo "Model: $(adb shell getprop ro.product.model)"
echo "Android: $(adb shell getprop ro.build.version.release)"
echo "Treble: $(adb shell getprop ro.treble.enabled)"
echo "VNDK: $(adb shell getprop ro.vndk.version)"
echo "Arch: $(adb shell getprop ro.product.cpu.abi)"
echo "A/B: $(adb shell getprop ro.build.ab_update)"
echo "Dynamic: $(adb shell getprop ro.boot.dynamic_partitions)"
```

## Tips

### Faster Flashing
- Use USB 3.0 port for faster transfer
- Close unnecessary programs
- Use SSD for storing images

### Safety
- Always backup before flashing
- Keep stock firmware available
- Don't interrupt flashing process

### Common Issues
```bash
# Device not detected
adb kill-server
adb start-server

# Permission denied
sudo adb devices  # Or fix udev rules

# Fastboot permission issues
sudo fastboot devices  # Or add user to plugdev group
```

---

**Note**: Commands may vary depending on device manufacturer and Android version. Always verify commands for your specific device.
