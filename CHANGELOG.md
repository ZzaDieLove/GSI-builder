# Changelog

All notable changes to the GSI Converter Tools project will be documented in this file.

## [1.0.0] - 2024

### Initial Release

#### Added
- **Core Features**:
  - Universal firmware extraction supporting multiple formats
  - Automatic firmware type detection
  - Device compatibility checking (Treble, VNDK, architecture)
  - GSI building from extracted firmware
  - GSI flashing with automatic method detection
  - Interactive menu system
  - Command-line interface

- **Supported Firmware Formats**:
  - Xiaomi (MIUI, HyperOS) - `.dat.br`, `.dat`
  - OnePlus (OxygenOS) - `payload.bin`
  - Samsung (OneUI) - `.tar.md5`, `.lz4`
  - Oppo/Realme (ColorOS) - `.ozip`
  - Motorola - `sparsechunk`
  - Google (Pixel) - `payload.bin`
  - ASUS (RogUI) - `.img`
  - Tecno (HiOS), Infinix (XOS), Itel (ItelOS) - various formats
  - Dynamic partitions - `super.img`

- **Android Version Support**:
  - Android 10 (API 29)
  - Android 11 (API 30)
  - Android 12 (API 31)
  - Android 12L (API 32)
  - Android 13 (API 33)
  - Android 14 (API 34)
  - Android 15 (API 35)
  - Android 16 (API 36)
  - Android 17 (API 37) - planned

- **Documentation**:
  - Comprehensive README
  - Quick start guide
  - Troubleshooting guide
  - Useful commands reference
  - GSI resources list
  - Package manifest

- **Helper Scripts**:
  - Automatic dependency installer (`install.sh`)
  - Flash helper script (`flash_helper.sh`)

#### Features

##### Firmware Extraction
- Automatic format detection
- Support for encrypted firmware (OZIP)
- Brotli decompression
- LZ4 decompression
- Sparse image conversion
- Dynamic partition handling
- Batch processing

##### Device Detection
- Treble support verification
- VNDK version detection
- Architecture detection (ARM/ARM64/x86)
- Binder version detection (32/64-bit)
- Partition type detection (A-Only/A/B)
- Dynamic partition detection

##### GSI Building
- Mount and modify system images
- Create sparse GSI images
- Automatic size calculation
- Support for both A-Only and A/B devices

##### GSI Flashing
- Automatic flashing method selection
- vbmeta flashing with disabled verification
- Dynamic partition handling
- Logical partition deletion for space
- Data wipe and factory reset

#### Supported Operating Systems
- Linux (Ubuntu, Debian, Arch, Fedora)
- macOS (with Homebrew)
- Windows (with WSL)

#### System Requirements
- Python 3.6 or higher
- 4GB RAM minimum (8GB recommended)
- 20GB free disk space
- USB debugging enabled device

### Known Issues

#### Limitations
- Incremental OTA payloads not supported
- Some proprietary formats may not work
- Device-specific features may not work with GSI
- Samsung devices require patched recovery for fastbootd

#### Common Problems
- Some devices need vendor partition compatibility
- Fingerprint sensors may not work
- Camera features may be limited
- Battery optimization may need tweaking

### Future Plans

#### Version 1.1.0 (Planned)
- [ ] GUI interface using tkinter
- [ ] Support for more firmware formats
- [ ] Automatic vendor detection
- [ ] Batch GSI building
- [ ] Integration with online GSI databases

#### Version 2.0.0 (Planned)
- [ ] Web interface
- [ ] Cloud-based GSI building
- [ ] Automatic device database
- [ ] Community GSI sharing
- [ ] Advanced modification tools

### Credits

#### Contributors
- AI Assistant - Initial development

#### Third-Party Tools
- phhusson - Project Treble pioneer
- Erfan Abdi - ErfanGSI tool
- xpirt - sdat2img/img2sdat
- ssut - payload-dumper-go
- bkerler - oppo_ozip_decrypt

#### Community
- XDA Developers community
- Project Treble community
- GSI developers and testers

### License

This project is licensed under the MIT License - see LICENSE file for details.

---

## Version History

### [1.0.0] - 2024-XX-XX
- Initial release
- Full feature set implemented
- Comprehensive documentation

---

**Note**: This changelog follows [Keep a Changelog](https://keepachangelog.com/) format.
