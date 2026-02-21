#!/usr/bin/env python3
"""
GSI Converter Tools - Universal Firmware to GSI Converter
Supports: Android 10-17, Various OS (MIUI, HyperOS, ColorOS, HiOS, ItelOS, XOS, RogUI, AOSP, etc.)
Author: AI Assistant
Version: 1.0.0
"""

import os
import sys
import subprocess
import json
import shutil
import argparse
import platform
from pathlib import Path
from typing import Optional, Dict, List, Tuple
import zipfile
import tarfile

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class GSITools:
    def __init__(self):
        self.work_dir = Path.home() / "GSI_Tools"
        self.tools_dir = self.work_dir / "tools"
        self.firmware_dir = self.work_dir / "firmware"
        self.output_dir = self.work_dir / "output"
        self.device_info = {}

        self.create_directories()

    def create_directories(self):
        """Create necessary directories"""
        for dir_path in [self.work_dir, self.tools_dir, self.firmware_dir, self.output_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

    def print_header(self, text: str):
        """Print formatted header"""
        print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}{text.center(60)}{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}\n")

    def print_success(self, text: str):
        """Print success message"""
        print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

    def print_error(self, text: str):
        """Print error message"""
        print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

    def print_warning(self, text: str):
        """Print warning message"""
        print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

    def run_command(self, cmd: List[str], cwd: Optional[Path] = None, check: bool = True) -> Tuple[int, str, str]:
        """Run shell command and return result"""
        try:
            result = subprocess.run(
                cmd, 
                cwd=cwd, 
                capture_output=True, 
                text=True,
                check=check
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            if check:
                self.print_error(f"Command failed: {' '.join(cmd)}")
                self.print_error(f"Error: {e.stderr}")
            return e.returncode, e.stdout, e.stderr
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")
            return -1, "", str(e)

    def check_dependencies(self) -> Dict[str, bool]:
        """Check if required tools are installed"""
        deps = {
            'python3': False,
            'adb': False,
            'fastboot': False,
            'java': False,
            'git': False,
            'brotli': False,
            'simg2img': False,
            'img2simg': False,
            'lpunpack': False,
            'lpmake': False,
            '7z': False,
            'lz4': False,
        }

        for tool in deps.keys():
            result = self.run_command(['which', tool], check=False)
            deps[tool] = result[0] == 0

        return deps

    def install_dependencies(self):
        """Install required dependencies"""
        self.print_header("Installing Dependencies")

        system = platform.system()

        if system == "Linux":
            # Detect Linux distribution
            if os.path.exists("/etc/debian_version"):
                self.print_warning("Detected Debian/Ubuntu system")
                self.install_debian_deps()
            elif os.path.exists("/etc/arch-release"):
                self.print_warning("Detected Arch Linux system")
                self.install_arch_deps()
            elif os.path.exists("/etc/fedora-release"):
                self.print_warning("Detected Fedora system")
                self.install_fedora_deps()
            else:
                self.print_error("Unsupported Linux distribution")
                return False
        elif system == "Darwin":
            self.print_warning("Detected macOS system")
            self.install_macos_deps()
        elif system == "Windows":
            self.print_warning("Detected Windows system")
            self.print_warning("Please install dependencies manually:")
            print("1. Python 3: https://python.org")
            print("2. Git: https://git-scm.com")
            print("3. 7-Zip: https://7-zip.org")
            print("4. Platform Tools: https://developer.android.com/studio/releases/platform-tools")
            return False
        else:
            self.print_error(f"Unsupported operating system: {system}")
            return False

        # Install Python packages
        self.run_command(['pip3', 'install', 'protobuf', 'pycryptodome', 'twrpdtgen', 'extract-dtb'])

        # Download additional tools
        self.download_tools()

        return True

    def install_debian_deps(self):
        """Install dependencies for Debian/Ubuntu"""
        packages = [
            'adb', 'fastboot', 'openjdk-17-jdk', 'git', 'p7zip-full', 'p7zip-rar',
            'brotli', 'lz4', 'liblzma-dev', 'python3-pip', 'curl', 'wget',
            'build-essential', 'libncurses5-dev', 'libssl-dev', 'unzip', 'zip'
        ]

        self.run_command(['sudo', 'apt-get', 'update'])
        self.run_command(['sudo', 'apt-get', 'install', '-y'] + packages)

        # Install simg2img tools
        self.run_command(['sudo', 'apt-get', 'install', '-y', 'android-tools-fsutils'])

    def install_arch_deps(self):
        """Install dependencies for Arch Linux"""
        packages = ['android-tools', 'jdk17-openjdk', 'git', 'p7zip', 'brotli', 'lz4', 'python-pip']
        self.run_command(['sudo', 'pacman', '-S', '--noconfirm'] + packages)

    def install_fedora_deps(self):
        """Install dependencies for Fedora"""
        packages = ['android-tools', 'java-17-openjdk', 'git', 'p7zip', 'brotli', 'lz4', 'python3-pip']
        self.run_command(['sudo', 'dnf', 'install', '-y'] + packages)

    def install_macos_deps(self):
        """Install dependencies for macOS"""
        # Check if Homebrew is installed
        result = self.run_command(['which', 'brew'], check=False)
        if result[0] != 0:
            self.print_error("Homebrew not found. Please install Homebrew first:")
            print("/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
            return False

        packages = ['android-platform-tools', 'openjdk@17', 'git', 'p7zip', 'brotli', 'lz4', 'python@3.11']
        self.run_command(['brew', 'install'] + packages)
        return True

    def download_tools(self):
        """Download additional tools"""
        self.print_header("Downloading Additional Tools")

        tools = {
            'payload-dumper-go': {
                'url': 'https://github.com/ssut/payload-dumper-go/releases/latest',
                'description': 'Fast OTA payload dumper'
            },
            'sdat2img': {
                'url': 'https://github.com/xpirt/sdat2img.git',
                'description': 'Convert sparse data to image'
            },
            'img2sdat': {
                'url': 'https://github.com/xpirt/img2sdat.git',
                'description': 'Convert image to sparse data'
            },
            'ozipdecrypt': {
                'url': 'https://github.com/bkerler/oppo_ozip_decrypt.git',
                'description': 'Decrypt Oppo/Realme OZIP files'
            }
        }

        for tool_name, tool_info in tools.items():
            tool_path = self.tools_dir / tool_name
            if not tool_path.exists():
                self.print_warning(f"Downloading {tool_name}...")
                if tool_name == 'payload-dumper-go':
                    # Download prebuilt binary
                    self.download_payload_dumper()
                else:
                    self.run_command(['git', 'clone', '--depth', '1', tool_info['url'], str(tool_path)])
            else:
                self.print_success(f"{tool_name} already exists")

    def download_payload_dumper(self):
        """Download payload-dumper-go binary"""
        import urllib.request

        system = platform.system().lower()
        machine = platform.machine().lower()

        if system == "linux":
            if machine in ["x86_64", "amd64"]:
                url = "https://github.com/ssut/payload-dumper-go/releases/download/1.2.2/payload-dumper-go_1.2.2_linux_amd64.tar.gz"
            elif machine in ["aarch64", "arm64"]:
                url = "https://github.com/ssut/payload-dumper-go/releases/download/1.2.2/payload-dumper-go_1.2.2_linux_arm64.tar.gz"
            else:
                url = "https://github.com/ssut/payload-dumper-go/releases/download/1.2.2/payload-dumper-go_1.2.2_linux_386.tar.gz"
        elif system == "darwin":
            if machine in ["x86_64", "amd64"]:
                url = "https://github.com/ssut/payload-dumper-go/releases/download/1.2.2/payload-dumper-go_1.2.2_darwin_amd64.tar.gz"
            else:
                url = "https://github.com/ssut/payload-dumper-go/releases/download/1.2.2/payload-dumper-go_1.2.2_darwin_arm64.tar.gz"
        else:
            return

        output_file = self.tools_dir / "payload-dumper-go.tar.gz"
        try:
            urllib.request.urlretrieve(url, str(output_file))
            self.run_command(['tar', '-xzf', str(output_file), '-C', str(self.tools_dir)])
            output_file.unlink()
            self.print_success("payload-dumper-go downloaded successfully")
        except Exception as e:
            self.print_error(f"Failed to download payload-dumper-go: {e}")

    def detect_firmware_type(self, firmware_path: Path) -> str:
        """Detect firmware file type"""
        self.print_header("Detecting Firmware Type")

        if not firmware_path.exists():
            self.print_error(f"Firmware file not found: {firmware_path}")
            return "unknown"

        file_name = firmware_path.name.lower()

        # Check by extension
        if file_name.endswith('.ozip'):
            self.print_success("Detected: Oppo/Realme OZIP firmware")
            return "ozip"
        elif file_name.endswith('.zip'):
            # Check contents
            return self.detect_zip_contents(firmware_path)
        elif file_name.endswith('.tar') or file_name.endswith('.tar.md5'):
            self.print_success("Detected: Samsung TAR firmware")
            return "tar"
        elif file_name.endswith('.lz4'):
            self.print_success("Detected: LZ4 compressed firmware")
            return "lz4"
        elif 'payload' in file_name:
            self.print_success("Detected: A/B OTA payload")
            return "payload"
        elif file_name.endswith('.img'):
            self.print_success("Detected: Raw image file")
            return "img"
        elif 'sparsechunk' in file_name:
            self.print_success("Detected: Motorola sparsechunk")
            return "sparsechunk"
        elif file_name.endswith('.br'):
            self.print_success("Detected: Brotli compressed file")
            return "br"
        else:
            self.print_warning("Unknown firmware type, attempting auto-detection...")
            return self.auto_detect_type(firmware_path)

    def detect_zip_contents(self, zip_path: Path) -> str:
        """Detect firmware type by analyzing ZIP contents"""
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                file_list = zf.namelist()

                # Check for payload.bin (OnePlus, Google, etc.)
                if 'payload.bin' in file_list:
                    self.print_success("Detected: A/B OTA ZIP (payload.bin)")
                    return "payload_zip"

                # Check for sparsechunk (Motorola)
                if any('sparsechunk' in f for f in file_list):
                    self.print_success("Detected: Motorola sparsechunk ZIP")
                    return "sparsechunk_zip"

                # Check for .dat.br files (Xiaomi)
                if any(f.endswith('.dat.br') for f in file_list):
                    self.print_success("Detected: Xiaomi/MIUI firmware (.dat.br)")
                    return "dat_br_zip"

                # Check for .dat files (Legacy)
                if any(f.endswith('.new.dat') for f in file_list):
                    self.print_success("Detected: Legacy OTA firmware (.dat)")
                    return "dat_zip"

                # Check for super.img (Dynamic partitions)
                if 'super.img' in file_list:
                    self.print_success("Detected: Dynamic partition firmware (super.img)")
                    return "super_img_zip"

                # Check for raw images
                if any(f.endswith('.img') for f in file_list):
                    self.print_success("Detected: Image-based firmware")
                    return "img_zip"

        except zipfile.BadZipFile:
            self.print_error("Invalid ZIP file")
            return "unknown"

        return "unknown"

    def auto_detect_type(self, file_path: Path) -> str:
        """Auto-detect file type using file command"""
        result = self.run_command(['file', str(file_path)], check=False)
        if result[0] == 0:
            file_info = result[1].lower()
            if 'zip' in file_info:
                return self.detect_zip_contents(file_path)
            elif 'tar' in file_info:
                return "tar"
            elif 'sparse' in file_info:
                return "sparse"
            elif 'ext4' in file_info:
                return "ext4"

        return "unknown"

    def extract_firmware(self, firmware_path: Path, firmware_type: str) -> bool:
        """Extract firmware based on type"""
        self.print_header(f"Extracting Firmware: {firmware_type}")

        extract_dir = self.firmware_dir / firmware_path.stem
        extract_dir.mkdir(parents=True, exist_ok=True)

        extract_methods = {
            "ozip": self.extract_ozip,
            "payload_zip": self.extract_payload_zip,
            "payload": self.extract_payload,
            "sparsechunk_zip": self.extract_sparsechunk_zip,
            "dat_br_zip": self.extract_dat_br_zip,
            "dat_zip": self.extract_dat_zip,
            "super_img_zip": self.extract_super_img_zip,
            "img_zip": self.extract_img_zip,
            "tar": self.extract_tar,
            "lz4": self.extract_lz4,
            "br": self.extract_br,
            "img": self.extract_img,
            "sparsechunk": self.extract_sparsechunk,
            "sparse": self.extract_sparse,
            "ext4": self.extract_ext4,
        }

        if firmware_type in extract_methods:
            return extract_methods[firmware_type](firmware_path, extract_dir)
        else:
            self.print_error(f"No extraction method for type: {firmware_type}")
            return False

    def extract_ozip(self, firmware_path: Path, extract_dir: Path) -> bool:
        """Extract Oppo/Realme OZIP firmware"""
        self.print_warning("Decrypting OZIP file...")

        ozip_tool = self.tools_dir / "oppo_ozip_decrypt"
        if not ozip_tool.exists():
            self.print_error("ozipdecrypt tool not found")
            return False

        result = self.run_command(
            ['python3', 'ozipdecrypt.py', str(firmware_path)],
            cwd=ozip_tool
        )

        if result[0] == 0:
            self.print_success("OZIP decrypted successfully")
            # Now extract the resulting ZIP
            decrypted_zip = firmware_path.with_suffix('.zip')
            if decrypted_zip.exists():
                return self.extract_zip(decrypted_zip, extract_dir)
        return False

    def extract_payload_zip(self, firmware_path: Path, extract_dir: Path) -> bool:
        """Extract payload.bin from ZIP"""
        self.print_warning("Extracting payload.bin from ZIP...")

        # Extract ZIP first
        if not self.extract_zip(firmware_path, extract_dir):
            return False

        # Find and extract payload.bin
        payload_file = extract_dir / "payload.bin"
        if payload_file.exists():
            return self.extract_payload(payload_file, extract_dir)
        else:
            self.print_error("payload.bin not found in ZIP")
            return False

    def extract_payload(self, firmware_path: Path, extract_dir: Path) -> bool:
        """Extract payload.bin using payload-dumper-go"""
        self.print_warning("Extracting payload.bin...")

        payload_dumper = self.tools_dir / "payload-dumper-go"
        if not payload_dumper.exists():
            # Try to find it in PATH
            payload_dumper = Path("payload-dumper-go")

        result = self.run_command(
            [str(payload_dumper), str(firmware_path), '-o', str(extract_dir)]
        )

        if result[0] == 0:
            self.print_success("Payload extracted successfully")
            return True
        else:
            self.print_error("Failed to extract payload")
            return False

    def extract_sparsechunk_zip(self, firmware_path: Path, extract_dir: Path) -> bool:
        """Extract Motorola sparsechunk firmware"""
        self.print_warning("Extracting Motorola sparsechunk...")

        if not self.extract_zip(firmware_path, extract_dir):
            return False

        # Find and merge sparsechunks
        sparsechunks = sorted(extract_dir.glob("*sparsechunk*"))
        if sparsechunks:
            return self.merge_sparsechunks(sparsechunks, extract_dir / "system.img")
        return True

    def merge_sparsechunks(self, sparsechunks: List[Path], output: Path) -> bool:
        """Merge sparsechunk files into single image"""
        self.print_warning("Merging sparsechunk files...")

        chunks_str = ' '.join([str(c) for c in sparsechunks])
        result = self.run_command(['simg2img'] + [str(c) for c in sparsechunks] + [str(output)])

        if result[0] == 0:
            self.print_success("Sparsechunks merged successfully")
            return True
        else:
            self.print_error("Failed to merge sparsechunks")
            return False

    def extract_dat_br_zip(self, firmware_path: Path, extract_dir: Path) -> bool:
        """Extract Xiaomi .dat.br firmware"""
        self.print_warning("Extracting .dat.br firmware...")

        if not self.extract_zip(firmware_path, extract_dir):
            return False

        # Process .dat.br files
        for dat_br_file in extract_dir.glob("*.new.dat.br"):
            self.extract_dat_br(dat_br_file, extract_dir)

        return True

    def extract_dat_br(self, dat_br_file: Path, extract_dir: Path) -> bool:
        """Decompress .dat.br file"""
        self.print_warning(f"Decompressing {dat_br_file.name}...")

        output_dat = dat_br_file.with_suffix('')  # Remove .br
        result = self.run_command(['brotli', '--decompress', str(dat_br_file), '-o', str(output_dat)])

        if result[0] == 0:
            self.print_success(f"Decompressed: {output_dat.name}")
            # Now convert .dat to .img
            return self.convert_dat_to_img(output_dat, extract_dir)
        return False

    def convert_dat_to_img(self, dat_file: Path, extract_dir: Path) -> bool:
        """Convert .dat file to .img using sdat2img"""
        self.print_warning(f"Converting {dat_file.name} to image...")

        # Find transfer list
        transfer_list = dat_file.with_name(dat_file.name.replace('.new.dat', '.transfer.list'))
        if not transfer_list.exists():
            self.print_error(f"Transfer list not found: {transfer_list}")
            return False

        output_img = extract_dir / dat_file.name.replace('.new.dat', '.img')

        sdat2img = self.tools_dir / "sdat2img" / "sdat2img.py"
        if not sdat2img.exists():
            sdat2img = Path("sdat2img.py")

        result = self.run_command([
            'python3', str(sdat2img),
            str(transfer_list), str(dat_file), str(output_img)
        ])

        if result[0] == 0:
            self.print_success(f"Created: {output_img.name}")
            return True
        return False

    def extract_dat_zip(self, firmware_path: Path, extract_dir: Path) -> bool:
        """Extract legacy .dat firmware"""
        self.print_warning("Extracting .dat firmware...")

        if not self.extract_zip(firmware_path, extract_dir):
            return False

        # Process .dat files
        for dat_file in extract_dir.glob("*.new.dat"):
            self.convert_dat_to_img(dat_file, extract_dir)

        return True

    def extract_super_img_zip(self, firmware_path: Path, extract_dir: Path) -> bool:
        """Extract firmware with super.img (dynamic partitions)"""
        self.print_warning("Extracting dynamic partition firmware...")

        if not self.extract_zip(firmware_path, extract_dir):
            return False

        super_img = extract_dir / "super.img"
        if super_img.exists():
            return self.extract_super_img(super_img, extract_dir)
        return True

    def extract_super_img(self, super_img: Path, extract_dir: Path) -> bool:
        """Extract partitions from super.img"""
        self.print_warning("Extracting from super.img...")

        # Convert sparse to raw if needed
        raw_img = extract_dir / "super_raw.img"
        result = self.run_command(['simg2img', str(super_img), str(raw_img)])

        if result[0] != 0:
            raw_img = super_img  # Maybe it's already raw

        # Extract partitions using lpunpack
        lpunpack = self.tools_dir / "lpunpack"
        if not lpunpack.exists():
            lpunpack = Path("lpunpack")

        partitions_dir = extract_dir / "partitions"
        partitions_dir.mkdir(exist_ok=True)

        result = self.run_command([str(lpunpack), str(raw_img), str(partitions_dir)])

        if result[0] == 0:
            self.print_success("Partitions extracted successfully")
            return True
        else:
            self.print_error("Failed to extract partitions")
            return False

    def extract_img_zip(self, firmware_path: Path, extract_dir: Path) -> bool:
        """Extract image-based firmware"""
        self.print_warning("Extracting image-based firmware...")
        return self.extract_zip(firmware_path, extract_dir)

    def extract_zip(self, zip_path: Path, extract_dir: Path) -> bool:
        """Extract ZIP file"""
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(extract_dir)
            self.print_success(f"Extracted: {zip_path.name}")
            return True
        except Exception as e:
            self.print_error(f"Failed to extract ZIP: {e}")
            return False

    def extract_tar(self, firmware_path: Path, extract_dir: Path) -> bool:
        """Extract TAR/TAR.MD5 firmware (Samsung)"""
        self.print_warning("Extracting Samsung TAR firmware...")

        # Remove .md5 extension if present for extraction
        if firmware_path.name.endswith('.tar.md5'):
            # Extract without the .md5
            result = self.run_command(['tar', '-xf', str(firmware_path), '-C', str(extract_dir)])
        else:
            result = self.run_command(['tar', '-xf', str(firmware_path), '-C', str(extract_dir)])

        if result[0] == 0:
            self.print_success("TAR extracted successfully")
            # Process LZ4 files if present
            for lz4_file in extract_dir.glob("*.lz4"):
                self.extract_lz4(lz4_file, extract_dir)
            return True
        return False

    def extract_lz4(self, lz4_file: Path, extract_dir: Path) -> bool:
        """Decompress LZ4 file"""
        self.print_warning(f"Decompressing {lz4_file.name}...")

        output_file = lz4_file.with_suffix('')
        result = self.run_command(['lz4', '-d', str(lz4_file), str(output_file)])

        if result[0] == 0:
            self.print_success(f"Decompressed: {output_file.name}")
            return True
        return False

    def extract_br(self, firmware_path: Path, extract_dir: Path) -> bool:
        """Extract Brotli compressed file"""
        return self.extract_dat_br(firmware_path, extract_dir)

    def extract_img(self, firmware_path: Path, extract_dir: Path) -> bool:
        """Copy image file to extract directory"""
        shutil.copy2(firmware_path, extract_dir)
        self.print_success(f"Copied: {firmware_path.name}")
        return True

    def extract_sparsechunk(self, firmware_path: Path, extract_dir: Path) -> bool:
        """Extract single sparsechunk file"""
        # Find all related sparsechunks
        base_name = firmware_path.name.split('_sparsechunk')[0]
        parent_dir = firmware_path.parent

        sparsechunks = sorted(parent_dir.glob(f"{base_name}_sparsechunk*"))
        if sparsechunks:
            return self.merge_sparsechunks(sparsechunks, extract_dir / f"{base_name}.img")
        return False

    def extract_sparse(self, firmware_path: Path, extract_dir: Path) -> bool:
        """Convert sparse image to raw"""
        output_img = extract_dir / firmware_path.name.replace('.sparse', '_raw.img')
        result = self.run_command(['simg2img', str(firmware_path), str(output_img)])

        if result[0] == 0:
            self.print_success(f"Converted to raw: {output_img.name}")
            return True
        return False

    def extract_ext4(self, firmware_path: Path, extract_dir: Path) -> bool:
        """Copy ext4 image"""
        shutil.copy2(firmware_path, extract_dir)
        self.print_success(f"Copied: {firmware_path.name}")
        return True

    def detect_device_info(self) -> Dict:
        """Detect device information using ADB"""
        self.print_header("Detecting Device Information")

        info = {
            'treble_supported': False,
            'vndk_version': '',
            'architecture': '',
            'binder_arch': '',
            'partition_type': '',  # A-Only or A/B
            'dynamic_partitions': False,
            'system_as_root': False,
        }

        # Check if device is connected
        result = self.run_command(['adb', 'devices'], check=False)
        if 'device' not in result[1] or result[1].count('device') < 2:
            self.print_warning("No device connected. Please connect a device via USB with USB debugging enabled.")
            return info

        # Check Treble support
        result = self.run_command(['adb', 'shell', 'getprop', 'ro.treble.enabled'], check=False)
        info['treble_supported'] = 'true' in result[1].lower()

        if info['treble_supported']:
            self.print_success("Device supports Project Treble")
        else:
            self.print_error("Device does NOT support Project Treble")
            return info

        # Get VNDK version
        result = self.run_command(['adb', 'shell', 'getprop', 'ro.vndk.version'], check=False)
        info['vndk_version'] = result[1].strip()
        if info['vndk_version']:
            self.print_success(f"VNDK Version: {info['vndk_version']}")

        # Get architecture
        result = self.run_command(['adb', 'shell', 'getprop', 'ro.product.cpu.abi'], check=False)
        info['architecture'] = result[1].strip()
        if info['architecture']:
            self.print_success(f"Architecture: {info['architecture']}")

        # Check binder architecture
        result = self.run_command(['adb', 'shell', 'getprop', 'ro.product.cpu.abilist'], check=False)
        if 'arm64' in result[1]:
            info['binder_arch'] = '64'
            self.print_success("Binder: 64-bit")
        else:
            info['binder_arch'] = '32'
            self.print_warning("Binder: 32-bit")

        # Check partition type
        result = self.run_command(['adb', 'shell', 'getprop', 'ro.build.ab_update'], check=False)
        if 'true' in result[1].lower():
            info['partition_type'] = 'A/B'
            self.print_success("Partition Type: A/B")
        else:
            info['partition_type'] = 'A-Only'
            self.print_warning("Partition Type: A-Only")

        # Check dynamic partitions
        result = self.run_command(['adb', 'shell', 'getprop', 'ro.boot.dynamic_partitions'], check=False)
        info['dynamic_partitions'] = 'true' in result[1].lower()
        if info['dynamic_partitions']:
            self.print_success("Dynamic Partitions: Yes")
        else:
            self.print_warning("Dynamic Partitions: No")

        # Check system-as-root
        result = self.run_command(['adb', 'shell', 'getprop', 'ro.build.system_root_image'], check=False)
        info['system_as_root'] = 'true' in result[1].lower()

        self.device_info = info
        return info

    def determine_gsi_type(self, device_info: Dict) -> str:
        """Determine correct GSI type for device"""
        arch = device_info.get('architecture', '')
        binder = device_info.get('binder_arch', '64')
        partition = device_info.get('partition_type', 'A-Only')

        gsi_type = ""

        # Architecture
        if 'arm64' in arch:
            gsi_type += "arm64"
        elif 'armeabi' in arch:
            gsi_type += "arm"
        elif 'x86_64' in arch:
            gsi_type += "x86_64"
        elif 'x86' in arch:
            gsi_type += "x86"

        # Binder
        if binder == '64':
            gsi_type += "_binder64"

        # Partition type
        if partition == 'A/B':
            gsi_type += "_ab"
        else:
            gsi_type += "_a"

        return gsi_type

    def build_gsi(self, system_img: Path, output_name: str = "gsi_system.img") -> bool:
        """Build GSI from extracted system image"""
        self.print_header("Building GSI")

        # Mount system image
        mount_dir = self.work_dir / "mount"
        mount_dir.mkdir(exist_ok=True)

        # Check if image is sparse
        result = self.run_command(['file', str(system_img)], check=False)
        if 'sparse' in result[1].lower():
            self.print_warning("Converting sparse image to raw...")
            raw_img = system_img.with_name(system_img.name.replace('.img', '_raw.img'))
            self.run_command(['simg2img', str(system_img), str(raw_img)])
            system_img = raw_img

        # Mount the image
        self.print_warning("Mounting system image...")
        result = self.run_command(['sudo', 'mount', '-o', 'loop', str(system_img), str(mount_dir)])

        if result[0] != 0:
            self.print_error("Failed to mount system image")
            return False

        # Create output GSI image
        output_img = self.output_dir / output_name

        # Get image size
        result = self.run_command(['du', '-sb', str(mount_dir)], check=False)
        size = int(result[1].split()[0]) if result[0] == 0 else 0
        size = max(size + (500 * 1024 * 1024), 2 * 1024 * 1024 * 1024)  # Add 500MB or min 2GB

        self.print_warning(f"Creating GSI image (size: {size // (1024*1024)}MB)...")

        # Create sparse image
        result = self.run_command([
            'sudo', 'make_ext4fs', '-s', '-l', str(size), '-a', 'system', 
            str(output_img), str(mount_dir)
        ])

        # Unmount
        self.run_command(['sudo', 'umount', str(mount_dir)])

        if result[0] == 0 and output_img.exists():
            self.print_success(f"GSI created: {output_img}")
            return True
        else:
            self.print_error("Failed to create GSI")
            return False

    def flash_gsi(self, gsi_img: Path, device_info: Dict) -> bool:
        """Flash GSI to device"""
        self.print_header("Flashing GSI")

        if not device_info.get('treble_supported'):
            self.print_error("Device does not support Treble. Cannot flash GSI.")
            return False

        # Check if device is connected
        result = self.run_command(['adb', 'devices'], check=False)
        if 'device' not in result[1] or result[1].count('device') < 2:
            self.print_error("No device connected")
            return False

        # Reboot to bootloader
        self.print_warning("Rebooting to bootloader...")
        self.run_command(['adb', 'reboot', 'bootloader'])

        input("Press Enter when device is in bootloader mode...")

        # Flash vbmeta with disabled verification
        self.print_warning("Flashing vbmeta with disabled verification...")
        vbmeta_img = gsi_img.parent / "vbmeta.img"
        if vbmeta_img.exists():
            self.run_command([
                'fastboot', '--disable-verity', '--disable-verification', 
                'flash', 'vbmeta', str(vbmeta_img)
            ])
        else:
            self.print_warning("vbmeta.img not found, skipping...")

        # Handle dynamic partitions
        if device_info.get('dynamic_partitions'):
            self.print_warning("Dynamic partitions detected. Rebooting to fastbootd...")
            self.run_command(['fastboot', 'reboot', 'fastboot'])
            input("Press Enter when device is in fastbootd mode...")

            # Delete logical partitions to make space
            self.print_warning("Deleting product partition to make space...")
            self.run_command(['fastboot', 'delete-logical-partition', 'product'])
            self.run_command(['fastboot', 'delete-logical-partition', 'product_a'])
            self.run_command(['fastboot', 'delete-logical-partition', 'product_b'])

        # Erase system
        self.print_warning("Erasing system partition...")
        self.run_command(['fastboot', 'erase', 'system'])

        # Flash GSI
        self.print_warning("Flashing GSI (this may take a while)...")
        result = self.run_command(['fastboot', 'flash', 'system', str(gsi_img)])

        if result[0] == 0:
            self.print_success("GSI flashed successfully!")

            # Wipe data
            self.print_warning("Wiping data...")
            self.run_command(['fastboot', '-w'])

            # Reboot
            self.print_warning("Rebooting device...")
            self.run_command(['fastboot', 'reboot'])

            self.print_success("Device rebooting. First boot may take several minutes.")
            return True
        else:
            self.print_error("Failed to flash GSI")
            return False

    def show_menu(self):
        """Show main menu"""
        while True:
            self.print_header("GSI Converter Tools - Main Menu")

            print(f"{Colors.CYAN}1.{Colors.ENDC} Install Dependencies")
            print(f"{Colors.CYAN}2.{Colors.ENDC} Detect Device Info")
            print(f"{Colors.CYAN}3.{Colors.ENDC} Extract Firmware")
            print(f"{Colors.CYAN}4.{Colors.ENDC} Build GSI from Extracted Firmware")
            print(f"{Colors.CYAN}5.{Colors.ENDC} Flash GSI to Device")
            print(f"{Colors.CYAN}6.{Colors.ENDC} Full Process (Extract + Build + Flash)")
            print(f"{Colors.CYAN}7.{Colors.ENDC} Check Dependencies")
            print(f"{Colors.CYAN}0.{Colors.ENDC} Exit")

            choice = input(f"\n{Colors.BOLD}Enter your choice: {Colors.ENDC}").strip()

            if choice == '1':
                self.install_dependencies()
            elif choice == '2':
                self.detect_device_info()
            elif choice == '3':
                firmware_path = input("Enter firmware file path: ").strip()
                firmware_path = Path(firmware_path)
                firmware_type = self.detect_firmware_type(firmware_path)
                if firmware_type != "unknown":
                    self.extract_firmware(firmware_path, firmware_type)
            elif choice == '4':
                system_img = input("Enter path to system.img: ").strip()
                output_name = input("Enter output name (default: gsi_system.img): ").strip() or "gsi_system.img"
                self.build_gsi(Path(system_img), output_name)
            elif choice == '5':
                gsi_img = input("Enter path to GSI image: ").strip()
                if not self.device_info:
                    self.detect_device_info()
                self.flash_gsi(Path(gsi_img), self.device_info)
            elif choice == '6':
                self.full_process()
            elif choice == '7':
                deps = self.check_dependencies()
                self.print_header("Dependency Status")
                for dep, installed in deps.items():
                    status = f"{Colors.GREEN}✓{Colors.ENDC}" if installed else f"{Colors.FAIL}✗{Colors.ENDC}"
                    print(f"{dep}: {status}")
            elif choice == '0':
                print(f"\n{Colors.GREEN}Thank you for using GSI Converter Tools!{Colors.ENDC}\n")
                break
            else:
                self.print_error("Invalid choice. Please try again.")

            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.ENDC}")

    def full_process(self):
        """Run full process: extract, build, flash"""
        self.print_header("Full Process Mode")

        # Step 1: Extract firmware
        firmware_path = input("Enter firmware file path: ").strip()
        firmware_path = Path(firmware_path)

        firmware_type = self.detect_firmware_type(firmware_path)
        if firmware_type == "unknown":
            self.print_error("Cannot detect firmware type")
            return

        if not self.extract_firmware(firmware_path, firmware_type):
            self.print_error("Firmware extraction failed")
            return

        # Find system.img
        extract_dir = self.firmware_dir / firmware_path.stem
        system_img = None

        # Search for system.img
        for img_path in extract_dir.rglob("system.img"):
            system_img = img_path
            break

        if not system_img:
            self.print_error("system.img not found in extracted firmware")
            return

        self.print_success(f"Found system.img: {system_img}")

        # Step 2: Build GSI
        output_name = input("Enter output name (default: gsi_system.img): ").strip() or "gsi_system.img"
        if not self.build_gsi(system_img, output_name):
            self.print_error("GSI build failed")
            return

        gsi_img = self.output_dir / output_name

        # Step 3: Detect device info
        if not self.device_info:
            self.detect_device_info()

        # Step 4: Flash GSI
        confirm = input(f"{Colors.WARNING}Flash GSI to device? (y/N): {Colors.ENDC}").strip().lower()
        if confirm == 'y':
            self.flash_gsi(gsi_img, self.device_info)

def main():
    parser = argparse.ArgumentParser(description='GSI Converter Tools')
    parser.add_argument('--firmware', '-f', help='Path to firmware file')
    parser.add_argument('--extract-only', '-e', action='store_true', help='Only extract firmware')
    parser.add_argument('--build-only', '-b', help='Build GSI from system.img')
    parser.add_argument('--flash-only', '-F', help='Flash GSI to device')
    parser.add_argument('--output', '-o', default='gsi_system.img', help='Output filename')
    parser.add_argument('--install-deps', '-i', action='store_true', help='Install dependencies')
    parser.add_argument('--detect-device', '-d', action='store_true', help='Detect device info')

    args = parser.parse_args()

    gsi_tools = GSITools()

    if args.install_deps:
        gsi_tools.install_dependencies()
    elif args.detect_device:
        gsi_tools.detect_device_info()
    elif args.firmware:
        firmware_type = gsi_tools.detect_firmware_type(Path(args.firmware))
        if firmware_type != "unknown":
            gsi_tools.extract_firmware(Path(args.firmware), firmware_type)
    elif args.build_only:
        gsi_tools.build_gsi(Path(args.build_only), args.output)
    elif args.flash_only:
        if not gsi_tools.device_info:
            gsi_tools.detect_device_info()
        gsi_tools.flash_gsi(Path(args.flash_only), gsi_tools.device_info)
    else:
        gsi_tools.show_menu()

if __name__ == '__main__':
    main()
