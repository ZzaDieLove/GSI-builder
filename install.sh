#!/bin/bash
# GSI Converter Tools - Installation Script
# Supports: Ubuntu/Debian, Arch Linux, Fedora, macOS
# Fixed: android-tools-fsutils package issue

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

print_header() {
    echo -e "${BLUE}============================================${NC}"
    echo -e "${BLUE}     GSI Converter Tools Installer${NC}"
    echo -e "${BLUE}============================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            if [[ "$ID" == "ubuntu" ]] || [[ "$ID" == "debian" ]] || [[ "$ID_LIKE" == *"debian"* ]] || [[ "$ID_LIKE" == *"ubuntu"* ]]; then
                echo "debian"
                return
            elif [[ "$ID" == "arch" ]] || [[ "$ID_LIKE" == *"arch"* ]]; then
                echo "arch"
                return
            elif [[ "$ID" == "fedora" ]] || [[ "$ID_LIKE" == *"fedora"* ]] || [[ "$ID" == "rhel" ]] || [[ "$ID" == "centos" ]]; then
                echo "fedora"
                return
            fi
        fi
        
        # Fallback detection
        if [ -f /etc/debian_version ]; then
            echo "debian"
        elif [ -f /etc/arch-release ]; then
            echo "arch"
        elif [ -f /etc/fedora-release ] || [ -f /etc/redhat-release ]; then
            echo "fedora"
        else
            echo "unknown"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    else
        echo "unknown"
    fi
}

detect_ubuntu_version() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo "$VERSION_ID"
    else
        echo "unknown"
    fi
}

install_debian() {
    print_warning "Detected Debian/Ubuntu system"
    UBUNTU_VERSION=$(detect_ubuntu_version)
    print_info "Ubuntu/Debian version: $UBUNTU_VERSION"
    
    print_warning "Updating package list..."
    sudo apt-get update

    print_warning "Installing packages..."
    
    # Install base packages (available on all versions)
    sudo apt-get install -y \
        android-tools-adb \
        android-tools-fastboot \
        openjdk-17-jdk \
        git \
        p7zip-full \
        p7zip-rar \
        brotli \
        lz4 \
        liblzma-dev \
        python3-pip \
        python3-venv \
        curl \
        wget \
        build-essential \
        libncurses5-dev \
        libssl-dev \
        unzip \
        zip \
        cmake \
        pkg-config \
        e2fsprogs \
        libe2fs-dev
    
    print_success "Base packages installed"
    
    # Build simg2img from source (android-tools-fsutils is deprecated)
    print_warning "Building simg2img tools from source..."
    build_simg2img
    
    print_success "System packages installed"
}

build_simg2img() {
    local BUILD_DIR="/tmp/android-tools-build"
    local INSTALL_DIR="$HOME/.local/bin"
    
    mkdir -p "$INSTALL_DIR"
    
    # Clone android-tools if not exists
    if [ ! -d "$BUILD_DIR" ]; then
        print_info "Cloning android-tools repository..."
        git clone --depth 1 --branch android-tools-34.0.0 https://android.googlesource.com/platform/system/tools/mkbootimg "$BUILD_DIR" 2>/dev/null || \
        git clone --depth 1 https://github.com/aosp-mirror/platform_system_tools_mkbootimg "$BUILD_DIR" 2>/dev/null || {
            print_warning "Could not clone android-tools, trying alternative method..."
            build_simg2img_alternative
            return
        }
    fi
    
    # Try to build with cmake
    cd "$BUILD_DIR"
    if [ -f "CMakeLists.txt" ]; then
        mkdir -p build && cd build
        cmake .. 2>/dev/null && make -j$(nproc) 2>/dev/null && {
            cp simg2img img2simg "$INSTALL_DIR/" 2>/dev/null || true
        } || {
            print_warning "CMake build failed, trying alternative..."
            build_simg2img_alternative
            return
        }
    else
        build_simg2img_alternative
        return
    fi
    
    # Add to PATH if not already there
    if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
        print_info "Added $INSTALL_DIR to PATH"
    fi
    
    print_success "simg2img tools built successfully"
    
    # Cleanup
    rm -rf "$BUILD_DIR"
}

build_simg2img_alternative() {
    print_info "Building simg2img using alternative method..."
    
    local INSTALL_DIR="$HOME/.local/bin"
    mkdir -p "$INSTALL_DIR"
    
    # Download and build simg2img from external repo
    local TEMP_DIR="/tmp/simg2img-build"
    rm -rf "$TEMP_DIR"
    mkdir -p "$TEMP_DIR"
    cd "$TEMP_DIR"
    
    # Download source files directly
    print_info "Downloading simg2img source..."
    
    # Try to get from AOSP directly
    curl -sL "https://raw.githubusercontent.com/aosp-mirror/platform_system_core/master/libsparse/simg2img.c" -o simg2img.c 2>/dev/null || \
    curl -sL "https://android.googlesource.com/platform/system/core/+/master/libsparse/simg2img.c?format=TEXT" | base64 -d > simg2img.c 2>/dev/null || true
    
    if [ ! -f "simg2img.c" ] || [ ! -s "simg2img.c" ]; then
        # Use prebuilt binaries
        print_warning "Could not build from source, downloading prebuilt binaries..."
        download_prebuilt_simg2img
        return
    fi
    
    # Download required headers and source files
    curl -sL "https://raw.githubusercontent.com/aosp-mirror/platform_system_core/master/libsparse/sparse_format.h" -o sparse_format.h 2>/dev/null || true
    curl -sL "https://raw.githubusercontent.com/aosp-mirror/platform_system_core/master/libsparse/sparse/sparse.h" -o sparse.h 2>/dev/null || true
    
    # Try to compile
    if command -v gcc &> /dev/null; then
        gcc -O2 -o simg2img simg2img.c -lz 2>/dev/null && {
            cp simg2img "$INSTALL_DIR/"
            chmod +x "$INSTALL_DIR/simg2img"
            print_success "simg2img compiled successfully"
        } || {
            print_warning "Compilation failed, downloading prebuilt..."
            download_prebuilt_simg2img
        }
    else
        download_prebuilt_simg2img
    fi
    
    # Cleanup
    rm -rf "$TEMP_DIR"
}

download_prebuilt_simg2img() {
    print_info "Downloading prebuilt simg2img binaries..."
    
    local INSTALL_DIR="$HOME/.local/bin"
    mkdir -p "$INSTALL_DIR"
    
    local ARCH=$(uname -m)
    local OS=$(uname -s | tr '[:upper:]' '[:lower:]')
    
    # Download from reliable source
    if [ "$OS" = "linux" ]; then
        if [ "$ARCH" = "x86_64" ]; then
            curl -sL "https://github.com/ponces/android-tools/releases/download/34.0.0/simg2img" -o "$INSTALL_DIR/simg2img" 2>/dev/null || \
            curl -sL "https://raw.githubusercontent.com/ponces/android-tools-binaries/main/simg2img-x86_64" -o "$INSTALL_DIR/simg2img" 2>/dev/null || true
            curl -sL "https://github.com/ponces/android-tools/releases/download/34.0.0/img2simg" -o "$INSTALL_DIR/img2simg" 2>/dev/null || \
            curl -sL "https://raw.githubusercontent.com/ponces/android-tools-binaries/main/img2simg-x86_64" -o "$INSTALL_DIR/img2simg" 2>/dev/null || true
        else
            curl -sL "https://raw.githubusercontent.com/ponces/android-tools-binaries/main/simg2img-arm64" -o "$INSTALL_DIR/simg2img" 2>/dev/null || true
            curl -sL "https://raw.githubusercontent.com/ponces/android-tools-binaries/main/img2simg-arm64" -o "$INSTALL_DIR/img2simg" 2>/dev/null || true
        fi
    fi
    
    chmod +x "$INSTALL_DIR/simg2img" "$INSTALL_DIR/img2simg" 2>/dev/null || true
    
    if command -v "$INSTALL_DIR/simg2img" &> /dev/null || command -v simg2img &> /dev/null; then
        print_success "simg2img downloaded successfully"
    else
        print_warning "Could not install simg2img. Some features may not work."
        print_info "You can manually install: sudo apt-get install simg2img (if available)"
    fi
}

install_arch() {
    print_warning "Detected Arch Linux system"
    print_warning "Installing packages..."
    
    sudo pacman -S --noconfirm \
        android-tools \
        jdk17-openjdk \
        git \
        p7zip \
        brotli \
        lz4 \
        python-pip \
        cmake \
        base-devel

    print_success "System packages installed"
}

install_fedora() {
    print_warning "Detected Fedora system"
    print_warning "Installing packages..."
    
    sudo dnf install -y \
        android-tools \
        java-17-openjdk \
        git \
        p7zip \
        brotli \
        lz4 \
        python3-pip \
        cmake \
        gcc \
        gcc-c++ \
        make

    print_success "System packages installed"
}

install_macos() {
    print_warning "Detected macOS system"

    if ! command -v brew &> /dev/null; then
        print_error "Homebrew not found. Please install Homebrew first:"
        echo '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        exit 1
    fi

    print_warning "Installing packages..."
    brew install \
        android-platform-tools \
        openjdk@17 \
        git \
        p7zip \
        brotli \
        lz4 \
        python@3.11 \
        cmake

    print_success "System packages installed"
}

install_python_packages() {
    print_warning "Installing Python packages..."
    
    # Upgrade pip first
    pip3 install --user --upgrade pip setuptools wheel
    
    # Install required packages
    pip3 install --user \
        protobuf \
        pycryptodome \
        twrpdtgen \
        extract-dtb \
        requests \
        tqdm \
        colorama
    
    print_success "Python packages installed"
}

download_tools() {
    print_warning "Downloading additional tools..."

    TOOLS_DIR="$HOME/GSI_Tools/tools"
    mkdir -p "$TOOLS_DIR"

    # Download payload-dumper-go
    if [ ! -f "$TOOLS_DIR/payload-dumper-go" ]; then
        print_warning "Downloading payload-dumper-go..."

        OS=$(uname -s | tr '[:upper:]' '[:lower:]')
        ARCH=$(uname -m)
        
        # Use latest release
        LATEST_URL="https://api.github.com/repos/ssut/payload-dumper-go/releases/latest"
        
        if [ "$OS" = "linux" ]; then
            if [ "$ARCH" = "x86_64" ] || [ "$ARCH" = "amd64" ]; then
                URL="https://github.com/ssut/payload-dumper-go/releases/download/1.2.2/payload-dumper-go_1.2.2_linux_amd64.tar.gz"
            elif [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
                URL="https://github.com/ssut/payload-dumper-go/releases/download/1.2.2/payload-dumper-go_1.2.2_linux_arm64.tar.gz"
            else
                URL="https://github.com/ssut/payload-dumper-go/releases/download/1.2.2/payload-dumper-go_1.2.2_linux_386.tar.gz"
            fi
        elif [ "$OS" = "darwin" ]; then
            if [ "$ARCH" = "x86_64" ] || [ "$ARCH" = "amd64" ]; then
                URL="https://github.com/ssut/payload-dumper-go/releases/download/1.2.2/payload-dumper-go_1.2.2_darwin_amd64.tar.gz"
            else
                URL="https://github.com/ssut/payload-dumper-go/releases/download/1.2.2/payload-dumper-go_1.2.2_darwin_arm64.tar.gz"
            fi
        fi

        if curl -sL --fail "$URL" -o "$TOOLS_DIR/payload-dumper-go.tar.gz" 2>/dev/null; then
            tar -xzf "$TOOLS_DIR/payload-dumper-go.tar.gz" -C "$TOOLS_DIR"
            rm "$TOOLS_DIR/payload-dumper-go.tar.gz"
            chmod +x "$TOOLS_DIR/payload-dumper-go"
            print_success "payload-dumper-go downloaded"
        else
            print_error "Failed to download payload-dumper-go"
            print_info "You can manually download from: https://github.com/ssut/payload-dumper-go/releases"
        fi
    else
        print_success "payload-dumper-go already exists"
    fi

    # Clone sdat2img
    if [ ! -d "$TOOLS_DIR/sdat2img" ]; then
        print_warning "Cloning sdat2img..."
        if git clone --depth 1 https://github.com/xpirt/sdat2img.git "$TOOLS_DIR/sdat2img" 2>/dev/null; then
            print_success "sdat2img cloned"
        else
            print_error "Failed to clone sdat2img"
        fi
    else
        print_success "sdat2img already exists"
    fi

    # Clone img2sdat
    if [ ! -d "$TOOLS_DIR/img2sdat" ]; then
        print_warning "Cloning img2sdat..."
        if git clone --depth 1 https://github.com/xpirt/img2sdat.git "$TOOLS_DIR/img2sdat" 2>/dev/null; then
            print_success "img2sdat cloned"
        else
            print_error "Failed to clone img2sdat"
        fi
    else
        print_success "img2sdat already exists"
    fi

    # Clone ozipdecrypt
    if [ ! -d "$TOOLS_DIR/oppo_ozip_decrypt" ]; then
        print_warning "Cloning oppo_ozip_decrypt..."
        if git clone --depth 1 https://github.com/bkerler/oppo_ozip_decrypt.git "$TOOLS_DIR/oppo_ozip_decrypt" 2>/dev/null; then
            print_success "oppo_ozip_decrypt cloned"
        else
            print_error "Failed to clone oppo_ozip_decrypt"
        fi
    else
        print_success "oppo_ozip_decrypt already exists"
    fi
    
    # Download lpunpack for dynamic partitions
    if [ ! -f "$TOOLS_DIR/lpunpack" ]; then
        print_warning "Downloading lpunpack..."
        
        local ARCH=$(uname -m)
        if [ "$ARCH" = "x86_64" ] || [ "$ARCH" = "amd64" ]; then
            curl -sL "https://github.com/ponces/android-tools/releases/download/34.0.0/lpunpack" -o "$TOOLS_DIR/lpunpack" 2>/dev/null || \
            curl -sL "https://raw.githubusercontent.com/ponces/android-tools-binaries/main/lpunpack-x86_64" -o "$TOOLS_DIR/lpunpack" 2>/dev/null || true
        else
            curl -sL "https://raw.githubusercontent.com/ponces/android-tools-binaries/main/lpunpack-arm64" -o "$TOOLS_DIR/lpunpack" 2>/dev/null || true
        fi
        
        chmod +x "$TOOLS_DIR/lpunpack" 2>/dev/null || true
        
        if [ -f "$TOOLS_DIR/lpunpack" ]; then
            print_success "lpunpack downloaded"
        else
            print_warning "Could not download lpunpack. Dynamic partition support may be limited."
        fi
    fi

    print_success "All tools downloaded"
}

setup_path() {
    print_warning "Setting up PATH..."

    SHELL_RC=""
    if [ -n "$ZSH_VERSION" ]; then
        SHELL_RC="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        SHELL_RC="$HOME/.bashrc"
    fi

    if [ -n "$SHELL_RC" ]; then
        TOOLS_DIR="$HOME/GSI_Tools/tools"
        LOCAL_BIN="$HOME/.local/bin"

        # Add GSI_Tools/tools to PATH
        if ! grep -q "GSI_Tools/tools" "$SHELL_RC" 2>/dev/null; then
            echo "" >> "$SHELL_RC"
            echo "# GSI Converter Tools" >> "$SHELL_RC"
            echo 'export PATH="$PATH:$HOME/GSI_Tools/tools:$HOME/.local/bin"' >> "$SHELL_RC"
            print_success "PATH updated in $SHELL_RC"
            print_warning "Please run: source $SHELL_RC"
        fi
    fi
}

copy_main_script() {
    print_warning "Setting up main script..."
    
    # Check if gsi_converter_tools.py exists in the same directory as install.sh
    if [ -f "$SCRIPT_DIR/gsi_converter_tools.py" ]; then
        TOOLS_DIR="$HOME/GSI_Tools"
        mkdir -p "$TOOLS_DIR"
        cp "$SCRIPT_DIR/gsi_converter_tools.py" "$TOOLS_DIR/"
        chmod +x "$TOOLS_DIR/gsi_converter_tools.py"
        print_success "Main script copied to $TOOLS_DIR"
    else
        print_warning "gsi_converter_tools.py not found in $SCRIPT_DIR"
        print_info "Please manually copy the script to your working directory"
    fi
}

create_directories() {
    print_warning "Creating working directories..."
    
    mkdir -p "$HOME/GSI_Tools"/{tools,firmware,output,mount}
    mkdir -p "$HOME/.local/bin"
    
    print_success "Directories created"
}

main() {
    print_header

    OS=$(detect_os)
    
    print_info "Detected OS: $OS"
    echo ""

    case $OS in
        debian)
            install_debian
            ;;
        arch)
            install_arch
            ;;
        fedora)
            install_fedora
            ;;
        macos)
            install_macos
            ;;
        *)
            print_error "Unsupported operating system: $OSTYPE"
            print_info "Supported systems: Ubuntu, Debian, Arch Linux, Fedora, macOS"
            exit 1
            ;;
    esac

    create_directories
    install_python_packages
    download_tools
    copy_main_script
    setup_path

    echo ""
    print_success "Installation complete!"
    echo ""
    echo -e "${GREEN}================================================${NC}"
    echo -e "${GREEN}  GSI Converter Tools installed successfully!${NC}"
    echo -e "${GREEN}================================================${NC}"
    echo ""
    echo -e "${BLUE}Usage:${NC}"
    echo "  cd ~/GSI_Tools"
    echo "  python3 gsi_converter_tools.py"
    echo ""
    echo -e "${BLUE}Or use command-line options:${NC}"
    echo "  python3 ~/GSI_Tools/gsi_converter_tools.py --help"
    echo ""
    echo -e "${YELLOW}Note: Please restart your terminal or run:${NC}"
    echo "  source ~/.bashrc  (or ~/.zshrc for zsh users)"
    echo ""
}

main "$@"
