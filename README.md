# GSI Converter Tools

**Universal Firmware to GSI Converter**

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive Python tool to convert stock Android firmware from various manufacturers into Generic System Images (GSI) for Project Treble devices.

## Features

- **Universal Firmware Support**: Extracts and converts firmware from:
  - **Xiaomi** (MIUI, HyperOS) - `.dat.br`, `.dat` formats
  - **OnePlus** - `payload.bin` format
  - **Samsung** - `.tar.md5`, `.lz4` formats
  - **Oppo/Realme** (ColorOS) - `.ozip` format
  - **Motorola** - `sparsechunk` format
  - **Google** - `payload.bin` format
  - **ASUS** (RogUI) - Raw image format
  - **Tecno/Itel/Infinix** (HiOS, ItelOS, XOS) - Various formats
  - **Dynamic Partitions** - `super.img` extraction

- **Android Version Support**: Android 10 through Android 17
- **Automatic Detection**: Detects firmware type automatically
- **Device Compatibility Check**: Verifies Treble support, VNDK version, architecture
- **Interactive Menu**: Easy-to-use command-line interface
- **Batch Processing**: Extract, build, and flash in one go

## Requirements

### System Requirements
- **OS**: Linux (Ubuntu/Debian/Arch/Fedora), macOS, or Windows (with WSL)
- **RAM**: Minimum 4GB (8GB+ recommended)
- **Storage**: At least 20GB free space
- **Python**: 3.6 or higher

### Required Tools
The script can automatically install most dependencies:

| Tool | Purpose | Auto-Install |
|------|---------|--------------|
| `adb` | Android Debug Bridge | ✅ |
| `fastboot` | Fastboot utility | ✅ |
| `python3` | Python runtime | Manual |
| `git` | Version control | ✅ |
| `java` | Java runtime (OpenJDK 17) | ✅ |
| `brotli` | Brotli decompression | ✅ |
| `lz4` | LZ4 decompression | ✅ |
| `simg2img` | Sparse image converter | ✅ |
| `img2simg` | Image to sparse converter | ✅ |
| `7z` | Archive extraction | ✅ |
| `payload-dumper-go` | OTA payload extractor | ✅ |
| `sdat2img` | DAT to IMG converter | ✅ |
| `lpunpack` | Dynamic partition extractor | Manual |
| `lpmake` | Dynamic partition builder | Manual |

## Installation

### Quick Start

1. **Download the script**:
```bash
wget https://raw.githubusercontent.com/yourusername/gsi-converter-tools/main/gsi_converter_tools.py
chmod +x gsi_converter_tools.py
```

2. **Run the script**:
```bash
python3 gsi_converter_tools.py
```

3. **Install dependencies** (Option 1 in menu):
```bash
python3 gsi_converter_tools.py --install-deps
```

### Manual Installation

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y adb fastboot openjdk-17-jdk git p7zip-full p7zip-rar     brotli lz4 liblzma-dev python3-pip curl wget build-essential     libncurses5-dev libssl-dev unzip zip android-tools-fsutils

pip3 install protobuf pycryptodome twrpdtgen extract-dtb
```

#### Arch Linux
```bash
sudo pacman -S --noconfirm android-tools jdk17-openjdk git p7zip brotli lz4 python-pip
pip3 install protobuf pycryptodome twrpdtgen extract-dtb
```

#### macOS (with Homebrew)
```bash
brew install android-platform-tools openjdk@17 git p7zip brotli lz4 python@3.11
pip3 install protobuf pycryptodome twrpdtgen extract-dtb
```

## Usage

### Interactive Mode (Recommended)

Launch the interactive menu:
```bash
python3 gsi_converter_tools.py
```

Menu options:
1. **Install Dependencies** - Automatically install all required tools
2. **Detect Device Info** - Check device Treble compatibility
3. **Extract Firmware** - Extract firmware from various formats
4. **Build GSI** - Create GSI from extracted system image
5. **Flash GSI** - Flash GSI to connected device
6. **Full Process** - Extract + Build + Flash in one go
7. **Check Dependencies** - Verify installed tools

### Command Line Mode

#### Extract Firmware Only
```bash
python3 gsi_converter_tools.py --firmware /path/to/firmware.zip
```

#### Build GSI from Extracted System Image
```bash
python3 gsi_converter_tools.py --build-only /path/to/system.img --output my_gsi.img
```

#### Flash GSI to Device
```bash
python3 gsi_converter_tools.py --flash-only /path/to/gsi.img
```

#### Detect Device Information
```bash
python3 gsi_converter_tools.py --detect-device
```

#### Install Dependencies
```bash
python3 gsi_converter_tools.py --install-deps
```

## Supported Firmware Formats

| Manufacturer | OS | Format | Status |
|--------------|-----|--------|--------|
| Xiaomi | MIUI, HyperOS | `.dat.br`, `.dat` | ✅ Supported |
| OnePlus | OxygenOS | `payload.bin` | ✅ Supported |
| Samsung | OneUI | `.tar.md5`, `.lz4` | ✅ Supported |
| Oppo | ColorOS | `.ozip` | ✅ Supported |
| Realme | RealmeUI | `.ozip` | ✅ Supported |
| Motorola | Stock | `sparsechunk` | ✅ Supported |
| Google | Pixel | `payload.bin` | ✅ Supported |
| ASUS | RogUI | `.img` | ✅ Supported |
| Tecno | HiOS | Various | ✅ Supported |
| Infinix | XOS | Various | ✅ Supported |
| Itel | ItelOS | Various | ✅ Supported |
| Nokia | Stock | `.zip` | ✅ Supported |
| Sony | Xperia | `.ftf` | ⚠️ Partial |
| LG | Stock | `.kdz` | ⚠️ Partial |

## Android Version Compatibility

| Android Version | API Level | VNDK Version | Status |
|-----------------|-----------|--------------|--------|
| Android 10 | 29 | 29 | ✅ Full Support |
| Android 11 | 30 | 30 | ✅ Full Support |
| Android 12 | 31-32 | 31 | ✅ Full Support |
| Android 12L | 32 | 31 | ✅ Full Support |
| Android 13 | 33 | 33 | ✅ Full Support |
| Android 14 | 34 | 34 | ✅ Full Support |
| Android 15 | 35 | 35 | ✅ Full Support |
| Android 16 | 36 | 36 | ✅ Full Support |
| Android 17 | 37 | 37 | ✅ Planned |

## GSI Types

The tool automatically detects and recommends the correct GSI type:

| Architecture | Binder | Partition | GSI Type |
|--------------|--------|-----------|----------|
| ARM64 | 64-bit | A/B | `arm64_binder64_ab` |
| ARM64 | 64-bit | A-Only | `arm64_binder64_a` |
| ARM | 32-bit | A/B | `arm_ab` |
| ARM | 32-bit | A-Only | `arm_a` |
| x86_64 | 64-bit | A/B | `x86_64_ab` |
| x86 | 32-bit | A/B | `x86_ab` |

## Workflow

### 1. Prepare Device
- Enable **USB Debugging** in Developer Options
- Enable **OEM Unlocking** (if bootloader needs unlocking)
- Connect device via USB

### 2. Check Device Compatibility
```bash
python3 gsi_converter_tools.py --detect-device
```

Required checks:
- ✅ Project Treble support
- ✅ VNDK version
- ✅ Architecture (ARM64/ARM/x86)
- ✅ Partition type (A/B or A-Only)

### 3. Extract Firmware
```bash
python3 gsi_converter_tools.py --firmware /path/to/stock_firmware.zip
```

### 4. Build GSI
```bash
python3 gsi_converter_tools.py --build-only /path/to/extracted/system.img
```

### 5. Flash GSI
```bash
python3 gsi_converter_tools.py --flash-only /path/to/gsi_system.img
```

Or use **Full Process** mode for automatic extraction, building, and flashing.

## Troubleshooting

### Common Issues

#### "Device not found"
- Ensure USB debugging is enabled
- Check USB cable (use original/data cable)
- Try different USB port
- Run `adb devices` to verify connection

#### "Failed to extract firmware"
- Verify firmware file is not corrupted
- Check available disk space (minimum 20GB)
- Ensure firmware format is supported

#### "Failed to flash GSI"
- Verify bootloader is unlocked
- Check device is in bootloader/fastboot mode
- Ensure correct GSI type for device
- Try deleting product partition: `fastboot delete-logical-partition product`

#### "Bootloop after flashing"
- Wipe data/factory reset in recovery
- Flash correct vbmeta with disabled verification
- Ensure GSI matches device architecture
- Check vendor partition compatibility

### Getting Help

1. Check device-specific forums on XDA Developers
2. Review Project Treble documentation
3. Use Treble Info app to verify compatibility
4. Join Telegram groups for your device

## Important Notes

⚠️ **Warning**: Flashing GSI may void warranty and can potentially brick your device. Always:
- Backup important data before proceeding
- Have stock firmware available for recovery
- Follow instructions carefully
- Understand the risks involved

⚠️ **Compatibility**: Not all devices work perfectly with GSIs. Some features may not work:
- Fingerprint sensors (especially under-display)
- Camera (may need GCam ports)
- NFC
- Specific manufacturer features

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Credits

- [phhusson](https://github.com/phhusson) - Project Treble pioneer
- [Erfan Abdi](https://github.com/erfanoabdi) - ErfanGSI tool
- [xpirt](https://github.com/xpirt) - sdat2img/img2sdat
- [ssut](https://github.com/ssut) - payload-dumper-go
- [bkerler](https://github.com/bkerler) - oppo_ozip_decrypt

## Disclaimer

This tool is provided as-is without any warranties. The authors are not responsible for any damage to devices, data loss, or bricked devices. Use at your own risk.

---

**Happy Flashing! 🚀**
