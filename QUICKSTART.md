# GSI Converter Tools - Quick Start Guide

This guide will help you get started with GSI Converter Tools quickly.

## Prerequisites

Before you begin, ensure you have:
- A Linux, macOS, or Windows (with WSL) computer
- USB cable to connect your Android device
- At least 20GB free disk space
- Python 3.6 or higher installed

## Step 1: Install Dependencies

### Option A: Automatic Installation (Recommended)

Run the installation script:
```bash
chmod +x install.sh
./install.sh
```

This will automatically install all required dependencies for your system.

### Option B: Manual Installation

See [README.md](README.md) for manual installation instructions.

## Step 2: Check Device Compatibility

### Enable USB Debugging
1. Go to **Settings** → **About Phone**
2. Tap **Build Number** 7 times to enable Developer Options
3. Go to **Settings** → **System** → **Developer Options**
4. Enable **USB Debugging**

### Check Treble Support
Connect your device and run:
```bash
python3 gsi_converter_tools.py --detect-device
```

Or use the interactive menu:
```bash
python3 gsi_converter_tools.py
# Select option 2: Detect Device Info
```

**Required for GSI:**
- ✅ Project Treble support: **YES**
- VNDK Version: Note this down
- Architecture: ARM64/ARM/x86
- Partition Type: A/B or A-Only

If your device doesn't support Treble, you cannot use GSI.

## Step 3: Get Stock Firmware

Download stock firmware for your device from:
- Manufacturer's official website
- XDA Developers forums
- Firmware hosting sites (SamFW, MiFirm, etc.)

**Supported formats:**
- `.zip` (Xiaomi, Motorola, etc.)
- `.ozip` (Oppo/Realme)
- `.tar.md5` (Samsung)
- `payload.bin` (OnePlus, Google)

## Step 4: Extract Firmware

### Using Interactive Menu
```bash
python3 gsi_converter_tools.py
# Select option 3: Extract Firmware
# Enter firmware file path when prompted
```

### Using Command Line
```bash
python3 gsi_converter_tools.py --firmware /path/to/firmware.zip
```

The tool will automatically detect the firmware type and extract it.

## Step 5: Build GSI

After extraction, build the GSI:

### Using Interactive Menu
```bash
python3 gsi_converter_tools.py
# Select option 4: Build GSI
# Enter path to extracted system.img
```

### Using Command Line
```bash
python3 gsi_converter_tools.py --build-only /path/to/extracted/system.img --output my_gsi.img
```

The GSI will be saved to `~/GSI_Tools/output/`.

## Step 6: Flash GSI to Device

⚠️ **WARNING**: This will erase all data on your device. Backup important data first!

### Unlock Bootloader (if not already unlocked)
1. Enable **OEM Unlocking** in Developer Options
2. Reboot to bootloader: `adb reboot bootloader`
3. Unlock: `fastboot flashing unlock`
4. Follow on-screen instructions

### Flash the GSI

#### Using Interactive Menu
```bash
python3 gsi_converter_tools.py
# Select option 5: Flash GSI
# Enter path to GSI image
```

#### Using Command Line
```bash
python3 gsi_converter_tools.py --flash-only /path/to/gsi.img
```

### Manual Flashing (if needed)

If automatic flashing fails, you can flash manually:

```bash
# Reboot to bootloader
adb reboot bootloader

# Flash vbmeta with disabled verification
fastboot --disable-verity --disable-verification flash vbmeta vbmeta.img

# For devices with dynamic partitions
fastboot reboot fastboot
fastboot delete-logical-partition product

# Erase and flash system
fastboot erase system
fastboot flash system system.img

# Wipe data and reboot
fastboot -w
fastboot reboot
```

## Step 7: First Boot

After flashing:
1. Device will reboot automatically
2. First boot may take 5-15 minutes (be patient!)
3. Complete initial setup
4. Enjoy your GSI!

## Full Process (All-in-One)

To extract, build, and flash in one command:

```bash
python3 gsi_converter_tools.py
# Select option 6: Full Process
# Follow the prompts
```

## Troubleshooting

### Device not detected
```bash
# Check ADB connection
adb devices

# If unauthorized, check device screen and allow USB debugging
# If not listed, try:
adb kill-server
adb start-server
adb devices
```

### Fastboot not working
```bash
# Check fastboot connection
fastboot devices

# If no devices, try different USB port or cable
# Some devices need specific drivers
```

### GSI too large
For devices with dynamic partitions:
```bash
fastboot reboot fastboot
fastboot delete-logical-partition product
fastboot delete-logical-partition system_ext
# Then flash GSI
```

### Bootloop after flashing
1. Boot to recovery (usually Power + Volume Up)
2. Wipe data/factory reset
3. Reboot

### Restore Stock Firmware
If something goes wrong:
1. Download stock firmware
2. Flash using manufacturer tool (Odin, MiFlash, etc.)
3. Or use fastboot to flash stock images

## Tips

### Finding the Right GSI
- Use **Treble Info** app from Play Store or F-Droid
- Check [phhusson's GSI list](https://github.com/phhusson/treble_experimentations/wiki/Generic-System-Image-(GSI)-list)
- Match VNDK version and architecture

### Common GSI Sources
- [phhusson's Treble Experimentations](https://github.com/phhusson/treble_experimentations)
- [ErfanGSI](https://github.com/erfanoabdi/ErfanGSIs)
- [Ponces' Treble AOSP](https://github.com/ponces/treble_aosp)

### Backup Before Flashing
Always backup:
- Personal data (photos, documents, etc.)
- App data
- Current ROM (if possible)

## Getting Help

If you encounter issues:

1. **Check device-specific forum** on XDA Developers
2. **Use Treble Info app** to verify compatibility
3. **Search for your device + "GSI"** on Google
4. **Join Telegram groups** for your device
5. **Read logs** with `adb logcat` if boot fails

## Next Steps

After successful GSI installation:
- Install Google Apps (GApps) if needed
- Install Magisk for root (optional)
- Customize and enjoy!

---

**Remember**: GSI is a generic system image. Some device-specific features may not work (fingerprint, camera features, etc.).

**Happy Flashing! 🚀**
