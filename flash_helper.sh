#!/bin/bash
# GSI Flash Helper Script
# Helper script for flashing GSI images

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}============================================${NC}"
    echo -e "${BLUE}          GSI Flash Helper${NC}"
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

check_device() {
    print_warning "Checking device connection..."

    if ! adb devices | grep -q "device$"; then
        print_error "No device connected or USB debugging not enabled"
        print_warning "Please connect device and enable USB debugging"
        exit 1
    fi

    print_success "Device connected"

    # Get device info
    DEVICE=$(adb shell getprop ro.product.model)
    ANDROID_VER=$(adb shell getprop ro.build.version.release)
    TREBLE=$(adb shell getprop ro.treble.enabled)

    echo "Device: $DEVICE"
    echo "Android Version: $ANDROID_VER"
    echo "Treble Support: $TREBLE"

    if [ "$TREBLE" != "true" ]; then
        print_error "Device does not support Project Treble!"
        exit 1
    fi
}

flash_standard() {
    local GSI_IMG=$1
    local VBMETA_IMG=$2

    print_header
    print_warning "Flashing GSI (Standard Method)"

    if [ ! -f "$GSI_IMG" ]; then
        print_error "GSI image not found: $GSI_IMG"
        exit 1
    fi

    check_device

    # Reboot to bootloader
    print_warning "Rebooting to bootloader..."
    adb reboot bootloader

    echo "Press Enter when device is in bootloader mode..."
    read

    # Flash vbmeta
    if [ -n "$VBMETA_IMG" ] && [ -f "$VBMETA_IMG" ]; then
        print_warning "Flashing vbmeta..."
        fastboot --disable-verity --disable-verification flash vbmeta "$VBMETA_IMG"
    fi

    # Erase and flash system
    print_warning "Erasing system..."
    fastboot erase system

    print_warning "Flashing GSI (this may take a while)..."
    fastboot flash system "$GSI_IMG"

    # Wipe data
    print_warning "Wiping data..."
    fastboot -w

    # Reboot
    print_warning "Rebooting..."
    fastboot reboot

    print_success "GSI flashed successfully!"
    print_warning "First boot may take 5-15 minutes"
}

flash_dynamic() {
    local GSI_IMG=$1
    local VBMETA_IMG=$2

    print_header
    print_warning "Flashing GSI (Dynamic Partitions Method)"

    if [ ! -f "$GSI_IMG" ]; then
        print_error "GSI image not found: $GSI_IMG"
        exit 1
    fi

    check_device

    # Reboot to bootloader
    print_warning "Rebooting to bootloader..."
    adb reboot bootloader

    echo "Press Enter when device is in bootloader mode..."
    read

    # Flash vbmeta
    if [ -n "$VBMETA_IMG" ] && [ -f "$VBMETA_IMG" ]; then
        print_warning "Flashing vbmeta..."
        fastboot --disable-verity --disable-verification flash vbmeta "$VBMETA_IMG"
    fi

    # Reboot to fastbootd
    print_warning "Rebooting to fastbootd..."
    fastboot reboot fastboot

    echo "Press Enter when device is in fastbootd mode..."
    read

    # Delete logical partitions to make space
    print_warning "Deleting product partition..."
    fastboot delete-logical-partition product 2>/dev/null || true
    fastboot delete-logical-partition product_a 2>/dev/null || true
    fastboot delete-logical-partition product_b 2>/dev/null || true

    print_warning "Deleting system_ext partition..."
    fastboot delete-logical-partition system_ext 2>/dev/null || true
    fastboot delete-logical-partition system_ext_a 2>/dev/null || true
    fastboot delete-logical-partition system_ext_b 2>/dev/null || true

    # Erase and flash system
    print_warning "Erasing system..."
    fastboot erase system

    print_warning "Flashing GSI (this may take a while)..."
    fastboot flash system "$GSI_IMG"

    # Reboot to recovery for factory reset
    print_warning "Rebooting to recovery..."
    fastboot reboot recovery

    print_success "GSI flashed!"
    print_warning "Please perform factory reset in recovery, then reboot"
}

flash_with_resize() {
    local GSI_IMG=$1
    local VBMETA_IMG=$2

    print_header
    print_warning "Flashing GSI with Partition Resize"

    if [ ! -f "$GSI_IMG" ]; then
        print_error "GSI image not found: $GSI_IMG"
        exit 1
    fi

    check_device

    # Get GSI size
    GSI_SIZE=$(stat -f%z "$GSI_IMG" 2>/dev/null || stat -c%s "$GSI_IMG" 2>/dev/null)
    print_warning "GSI size: $((GSI_SIZE / 1024 / 1024)) MB"

    # Reboot to bootloader
    print_warning "Rebooting to bootloader..."
    adb reboot bootloader

    echo "Press Enter when device is in bootloader mode..."
    read

    # Flash vbmeta
    if [ -n "$VBMETA_IMG" ] && [ -f "$VBMETA_IMG" ]; then
        print_warning "Flashing vbmeta..."
        fastboot --disable-verity --disable-verification flash vbmeta "$VBMETA_IMG"
    fi

    # Reboot to fastbootd
    print_warning "Rebooting to fastbootd..."
    fastboot reboot fastboot

    echo "Press Enter when device is in fastbootd mode..."
    read

    # Get current system partition size
    print_warning "Current partitions:"
    fastboot getvar all 2>&1 | grep -E "(partition-size|logical-block-size)"

    # Delete partitions to make maximum space
    print_warning "Deleting unnecessary partitions..."
    fastboot delete-logical-partition product 2>/dev/null || true
    fastboot delete-logical-partition product_a 2>/dev/null || true
    fastboot delete-logical-partition product_b 2>/dev/null || true
    fastboot delete-logical-partition system_ext 2>/dev/null || true
    fastboot delete-logical-partition system_ext_a 2>/dev/null || true
    fastboot delete-logical-partition system_ext_b 2>/dev/null || true
    fastboot delete-logical-partition odm 2>/dev/null || true
    fastboot delete-logical-partition odm_a 2>/dev/null || true
    fastboot delete-logical-partition odm_b 2>/dev/null || true

    # Erase system
    print_warning "Erasing system..."
    fastboot erase system

    # Flash GSI
    print_warning "Flashing GSI (this may take a while)..."
    fastboot flash system "$GSI_IMG"

    if [ $? -eq 0 ]; then
        print_success "GSI flashed successfully!"
        print_warning "Rebooting to recovery for factory reset..."
        fastboot reboot recovery
    else
        print_error "Failed to flash GSI"
        print_warning "GSI might be too large for your device"
        exit 1
    fi
}

show_help() {
    echo "GSI Flash Helper"
    echo ""
    echo "Usage:"
    echo "  $0 standard <gsi.img> [vbmeta.img]    - Flash using standard method"
    echo "  $0 dynamic <gsi.img> [vbmeta.img]     - Flash with dynamic partitions"
    echo "  $0 resize <gsi.img> [vbmeta.img]      - Flash with partition resize"
    echo "  $0 info                               - Show device information"
    echo "  $0 help                               - Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 standard system.img vbmeta.img"
    echo "  $0 dynamic system.img"
    echo "  $0 info"
}

show_info() {
    print_header
    check_device

    echo ""
    echo "=== Device Information ==="
    echo "Model: $(adb shell getprop ro.product.model)"
    echo "Manufacturer: $(adb shell getprop ro.product.manufacturer)"
    echo "Android Version: $(adb shell getprop ro.build.version.release)"
    echo "SDK: $(adb shell getprop ro.build.version.sdk)"
    echo "VNDK: $(adb shell getprop ro.vndk.version)"
    echo "Architecture: $(adb shell getprop ro.product.cpu.abi)"
    echo "Treble: $(adb shell getprop ro.treble.enabled)"
    echo "A/B Update: $(adb shell getprop ro.build.ab_update)"
    echo "Dynamic Partitions: $(adb shell getprop ro.boot.dynamic_partitions)"
    echo "System as Root: $(adb shell getprop ro.build.system_root_image)"
}

main() {
    case $1 in
        standard)
            flash_standard "$2" "$3"
            ;;
        dynamic)
            flash_dynamic "$2" "$3"
            ;;
        resize)
            flash_with_resize "$2" "$3"
            ;;
        info)
            show_info
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            show_help
            ;;
    esac
}

main "$@"
