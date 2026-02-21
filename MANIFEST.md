# GSI Converter Tools - Package Manifest

This document lists all files included in the GSI Converter Tools package.

## Core Files

### Main Script
| File | Description | Size |
|------|-------------|------|
| `gsi_converter_tools.py` | Main Python script for GSI conversion | ~40KB |

### Installation Scripts
| File | Description | Size |
|------|-------------|------|
| `install.sh` | Automatic dependency installer | ~6.7KB |
| `flash_helper.sh` | Helper script for flashing GSI | ~8.3KB |

## Documentation Files

### User Guides
| File | Description | Size |
|------|-------------|------|
| `README.md` | Main documentation and overview | ~9.2KB |
| `QUICKSTART.md` | Quick start guide for beginners | ~5.9KB |
| `USEFUL_COMMANDS.md` | Reference for ADB/Fastboot commands | ~8KB |

### Troubleshooting
| File | Description | Size |
|------|-------------|------|
| `TROUBLESHOOTING.md` | Comprehensive troubleshooting guide | ~12KB |

### Resources
| File | Description | Size |
|------|-------------|------|
| `GSI_RESOURCES.md` | Links to GSI sources and tools | ~7.9KB |
| `MANIFEST.md` | This file - package contents list | ~2KB |

## Total Package Size

- **Core Scripts**: ~55KB
- **Documentation**: ~45KB
- **Total**: ~100KB (excluding downloaded tools)

## Directory Structure

```
GSI_Tools/
├── gsi_converter_tools.py    # Main script
├── install.sh                # Installer
├── flash_helper.sh           # Flash helper
├── README.md                 # Main docs
├── QUICKSTART.md            # Quick start
├── USEFUL_COMMANDS.md       # Command reference
├── TROUBLESHOOTING.md       # Troubleshooting
├── GSI_RESOURCES.md         # Resource links
├── MANIFEST.md              # This file
└── tools/                   # Downloaded tools (created by installer)
    ├── payload-dumper-go
    ├── sdat2img/
    ├── img2sdat/
    └── oppo_ozip_decrypt/
```

## Installation Locations

### User Directories (Created)
- `~/GSI_Tools/` - Main working directory
- `~/GSI_Tools/tools/` - Downloaded tools
- `~/GSI_Tools/firmware/` - Extracted firmware
- `~/GSI_Tools/output/` - Generated GSI images

### System Paths (Modified)
- `~/.bashrc` or `~/.zshrc` - PATH updated

## File Permissions

| File | Permissions |
|------|-------------|
| `*.py` | 644 (rw-r--r--) |
| `*.sh` | 755 (rwxr-xr-x) |
| `*.md` | 644 (rw-r--r--) |

## Dependencies

### System Dependencies (Auto-installed)
- `adb` - Android Debug Bridge
- `fastboot` - Fastboot utility
- `python3` - Python 3.6+
- `git` - Version control
- `java` - OpenJDK 17
- `brotli` - Brotli decompression
- `lz4` - LZ4 decompression
- `p7zip` - 7-Zip archiver
- `simg2img` - Sparse image tools

### Python Packages (Auto-installed)
- `protobuf` - Protocol buffers
- `pycryptodome` - Cryptographic library
- `twrpdtgen` - TWRP device tree generator
- `extract-dtb` - DTB extraction tool

### Downloaded Tools (Auto-downloaded)
- `payload-dumper-go` - OTA payload extractor
- `sdat2img` - DAT to IMG converter
- `img2sdat` - IMG to DAT converter
- `ozipdecrypt` - OZIP decryptor

## Version Information

- **Package Version**: 1.0.0
- **Release Date**: 2024
- **Python Version**: 3.6+
- **Supported OS**: Linux, macOS, Windows (WSL)

## Checksums

To verify file integrity:

```bash
# Generate checksums
md5sum gsi_converter_tools.py install.sh flash_helper.sh

# Verify
md5sum -c checksums.md5
```

## License

All files in this package are released under the MIT License unless otherwise specified.

## Support

For support and updates:
- Check documentation files
- Visit GitHub repository
- Join community forums

---

**Package Created**: 2024
**Last Updated**: 2024
