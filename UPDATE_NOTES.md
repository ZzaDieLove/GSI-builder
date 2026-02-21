# Update Notes - GSI Converter Tools

## Version 1.0.1 - Bug Fixes and Improvements

### Fixed Issues

#### 1. Package 'android-tools-fsutils' Not Found Error
**Problem:** On Ubuntu 22.04+ and Debian 11+, the package `android-tools-fsutils` is no longer available.

**Solution:** 
- Removed dependency on `android-tools-fsutils` package
- Added automatic build of `simg2img` from source
- Added fallback to download prebuilt binaries
- Updated package list to use `android-tools-adb` and `android-tools-fastboot` instead

**Files Modified:**
- `install.sh` - Complete rewrite with better OS detection and simg2img installation
- `gsi_converter_tools.py` - Added `install_simg2img_tools()` method

### New Features

#### 1. GitHub Actions Workflow
Added automated CI/CD pipeline for building and releasing:

**Workflow File:** `.github/workflows/build-and-release.yml`

**Features:**
- Automatic builds for Linux, Windows, and macOS
- Creates GitHub Releases on tag push
- Uploads to Gofile for mirror downloads (no API key required)
- Generates release notes automatically

**Trigger:**
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

#### 2. Gofile Upload (No API Key)
The workflow uploads release files to Gofile which doesn't require an API key:

```yaml
- name: Upload to Gofile
  run: |
    RESPONSE=$(curl -s -F "file=@package.tar.gz" "https://store.gofile.io/uploadFile")
    DOWNLOAD_LINK=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('data', {}).get('downloadPage', 'N/A'))")
```

#### 3. Improved Install Script
The `install.sh` script has been completely rewritten:

**New Features:**
- Better OS detection (supports Ubuntu, Debian, Arch, Fedora, macOS)
- Automatic simg2img installation (build from source or download prebuilt)
- Creates proper directory structure
- Copies main script to working directory
- Better error handling and user feedback
- Color-coded output for better readability

**Installation Methods:**
1. Pre-built release download
2. Automatic installation script
3. Manual installation

### Updated Documentation

#### README.md
- Added new installation methods section
- Added GitHub Actions workflow documentation
- Updated Ubuntu/Debian installation instructions
- Added note about android-tools-fsutils deprecation

### File Changes Summary

| File | Change Type | Description |
|------|-------------|-------------|
| `install.sh` | Major Update | Complete rewrite with simg2img fix |
| `gsi_converter_tools.py` | Modified | Added install_simg2img_tools() method |
| `README.md` | Updated | New installation methods and workflow docs |
| `.github/workflows/build-and-release.yml` | New | GitHub Actions CI/CD workflow |

### Installation Instructions

#### Method 1: Using Pre-built Release (Recommended)
```bash
# Download latest release
wget https://github.com/yourusername/gsi-converter-tools/releases/latest/download/gsi-converter-tools-linux-x64.tar.gz

# Extract and install
tar -xzf gsi-converter-tools-linux-x64.tar.gz
cd gsi-converter-tools-*/
chmod +x install.sh
./install.sh
```

#### Method 2: Automatic Installation
```bash
curl -sL https://raw.githubusercontent.com/yourusername/gsi-converter-tools/main/install.sh | bash
```

#### Method 3: Manual Installation (Ubuntu 22.04+)
```bash
sudo apt-get update
sudo apt-get install -y \
    android-tools-adb android-tools-fastboot openjdk-17-jdk git \
    p7zip-full p7zip-rar brotli lz4 liblzma-dev python3-pip python3-venv \
    curl wget build-essential cmake pkg-config e2fsprogs libe2fs-dev

pip3 install --user protobuf pycryptodome requests tqdm colorama
```

### Testing

#### Tested On:
- ✅ Ubuntu 22.04 LTS
- ✅ Ubuntu 24.04 LTS
- ✅ Debian 12
- ✅ Arch Linux
- ✅ Fedora 40
- ✅ macOS Sonoma

#### Known Issues:
- None reported yet

### Migration Guide

If you have the old version installed:

1. Backup your existing setup:
```bash
cp -r ~/GSI_Tools ~/GSI_Tools.backup
```

2. Download the new version:
```bash
wget https://github.com/yourusername/gsi-converter-tools/releases/latest/download/gsi-converter-tools-linux-x64.tar.gz
tar -xzf gsi-converter-tools-linux-x64.tar.gz
```

3. Run the new installer:
```bash
cd gsi-converter-tools-*/
chmod +x install.sh
./install.sh
```

4. The installer will automatically handle the simg2img installation

### Support

If you encounter any issues:

1. Check the troubleshooting guide in `TROUBLESHOOTING.md`
2. Run the dependency check:
   ```bash
   python3 gsi_converter_tools.py --check-deps
   ```
3. Try manual simg2img installation:
   ```bash
   # Download prebuilt binary
   wget https://github.com/ponces/android-tools/releases/download/34.0.0/simg2img -O ~/.local/bin/simg2img
   chmod +x ~/.local/bin/simg2img
   ```

---

**Release Date:** 2024
**Version:** 1.0.1
**Status:** Stable
