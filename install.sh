#!/bin/bash
# GSI Converter Tools - Installation Script
# Supports: Ubuntu/Debian, Arch Linux, Fedora, macOS

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/debian_version ]; then
            echo "debian"
        elif [ -f /etc/arch-release ]; then
            echo "arch"
        elif [ -f /etc/fedora-release ]; then
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

install_debian() {
    print_warning "Detected Debian/Ubuntu system"
    print_warning "Updating package list..."
    sudo apt-get update

    print_warning "Installing packages..."
    sudo apt-get install -y \
        adb \
        fastboot \
        openjdk-17-jdk \
        git \
        p7zip-full \
        p7zip-rar \
        brotli \
        lz4 \
        liblzma-dev \
        python3-pip \
        curl \
        wget \
        build-essential \
        libncurses5-dev \
        libssl-dev \
        unzip \
        zip \
        android-tools-fsutils

    print_success "System packages installed"
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
        python-pip

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
        python3-pip

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
        python@3.11

    print_success "System packages installed"
}

install_python_packages() {
    print_warning "Installing Python packages..."
    pip3 install --user protobuf pycryptodome twrpdtgen extract-dtb
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

        if [ "$OS" = "linux" ]; then
            if [ "$ARCH" = "x86_64" ]; then
                URL="https://github.com/ssut/payload-dumper-go/releases/download/1.2.2/payload-dumper-go_1.2.2_linux_amd64.tar.gz"
            elif [ "$ARCH" = "aarch64" ]; then
                URL="https://github.com/ssut/payload-dumper-go/releases/download/1.2.2/payload-dumper-go_1.2.2_linux_arm64.tar.gz"
            else
                URL="https://github.com/ssut/payload-dumper-go/releases/download/1.2.2/payload-dumper-go_1.2.2_linux_386.tar.gz"
            fi
        elif [ "$OS" = "darwin" ]; then
            if [ "$ARCH" = "x86_64" ]; then
                URL="https://github.com/ssut/payload-dumper-go/releases/download/1.2.2/payload-dumper-go_1.2.2_darwin_amd64.tar.gz"
            else
                URL="https://github.com/ssut/payload-dumper-go/releases/download/1.2.2/payload-dumper-go_1.2.2_darwin_arm64.tar.gz"
            fi
        fi

        curl -L -o "$TOOLS_DIR/payload-dumper-go.tar.gz" "$URL"
        tar -xzf "$TOOLS_DIR/payload-dumper-go.tar.gz" -C "$TOOLS_DIR"
        rm "$TOOLS_DIR/payload-dumper-go.tar.gz"
        chmod +x "$TOOLS_DIR/payload-dumper-go"
        print_success "payload-dumper-go downloaded"
    fi

    # Clone sdat2img
    if [ ! -d "$TOOLS_DIR/sdat2img" ]; then
        print_warning "Cloning sdat2img..."
        git clone --depth 1 https://github.com/xpirt/sdat2img.git "$TOOLS_DIR/sdat2img"
        print_success "sdat2img cloned"
    fi

    # Clone img2sdat
    if [ ! -d "$TOOLS_DIR/img2sdat" ]; then
        print_warning "Cloning img2sdat..."
        git clone --depth 1 https://github.com/xpirt/img2sdat.git "$TOOLS_DIR/img2sdat"
        print_success "img2sdat cloned"
    fi

    # Clone ozipdecrypt
    if [ ! -d "$TOOLS_DIR/oppo_ozip_decrypt" ]; then
        print_warning "Cloning oppo_ozip_decrypt..."
        git clone --depth 1 https://github.com/bkerler/oppo_ozip_decrypt.git "$TOOLS_DIR/oppo_ozip_decrypt"
        print_success "oppo_ozip_decrypt cloned"
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

        if ! grep -q "GSI_Tools/tools" "$SHELL_RC"; then
            echo "" >> "$SHELL_RC"
            echo "# GSI Converter Tools" >> "$SHELL_RC"
            echo 'export PATH="$PATH:$HOME/GSI_Tools/tools"' >> "$SHELL_RC"
            print_success "PATH updated in $SHELL_RC"
            print_warning "Please run: source $SHELL_RC"
        fi
    fi
}

main() {
    print_header

    OS=$(detect_os)

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
            print_error "Unsupported operating system"
            exit 1
            ;;
    esac

    install_python_packages
    download_tools
    setup_path

    print_success "Installation complete!"
    echo ""
    echo -e "${GREEN}You can now run: python3 gsi_converter_tools.py${NC}"
    echo ""
}

main "$@"
