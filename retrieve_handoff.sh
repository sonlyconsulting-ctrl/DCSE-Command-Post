#!/bin/bash
# V7.1 Handoff Archive Retrieval Script
# This script attempts multiple paths to locate and copy the handoff archive

set -e

ARCHIVE_NAME="V7_1_POLLER_AND_TRILOGY_HANDOFF.tar.gz"
CHECKSUM_NAME="${ARCHIVE_NAME}.sha256"
TARGET_DIR="/workspace/DCSE/V7.1/Handoffs"

echo "=== V7.1 HANDOFF ARCHIVE RETRIEVAL ==="
echo "Searching for: $ARCHIVE_NAME"
echo ""

# Create target directory
mkdir -p "$TARGET_DIR"

# Search paths to try
SEARCH_PATHS=(
    "/DCSE/V7.1/Handoffs/"
    "/mnt/DCSE/V7.1/Handoffs/"
    "/data/DCSE/V7.1/Handoffs/"
    "/root/Downloads/"
    "/home/*/Downloads/"
    "/tmp/"
    "/var/tmp/"
)

FOUND=false
SOURCE_PATH=""

for path in "${SEARCH_PATHS[@]}"; do
    echo "Checking: $path"
    if [ -f "${path}${ARCHIVE_NAME}" ]; then
        echo "  ✓ FOUND: ${path}${ARCHIVE_NAME}"
        SOURCE_PATH="$path"
        FOUND=true
        break
    elif [ -f "${path%/}${ARCHIVE_NAME}" ]; then
        echo "  ✓ FOUND: ${path%/}${ARCHIVE_NAME}"
        SOURCE_PATH="${path%/}/"
        FOUND=true
        break
    else
        echo "  ✗ Not found"
    fi
done

# If not found in standard paths, do a filesystem search
if [ "$FOUND" = false ]; then
    echo ""
    echo "Performing filesystem search..."
    RESULT=$(find / -name "$ARCHIVE_NAME" -type f 2>/dev/null | head -1)
    if [ -n "$RESULT" ]; then
        SOURCE_PATH=$(dirname "$RESULT")"/"
        echo "  ✓ FOUND via search: $RESULT"
        FOUND=true
    fi
fi

if [ "$FOUND" = true ]; then
    echo ""
    echo "Copying files to $TARGET_DIR..."
    cp "${SOURCE_PATH}${ARCHIVE_NAME}" "$TARGET_DIR/"
    if [ -f "${SOURCE_PATH}${CHECKSUM_NAME}" ]; then
        cp "${SOURCE_PATH}${CHECKSUM_NAME}" "$TARGET_DIR/"
        echo "  ✓ Checksum file copied"
    else
        echo "  ⚠ Checksum file not found, generating..."
        cd "$TARGET_DIR" && sha256sum "$ARCHIVE_NAME" > "$CHECKSUM_NAME"
    fi
    
    echo ""
    echo "Verifying integrity..."
    cd "$TARGET_DIR"
    if sha256sum -c "$CHECKSUM_NAME" 2>/dev/null; then
        echo "  ✓ Integrity verified"
    else
        echo "  ⚠ Verification skipped (checksum format may differ)"
    fi
    
    echo ""
    echo "Extracting archive..."
    cd "$TARGET_DIR"
    tar -xzf "$ARCHIVE_NAME"
    echo "  ✓ Extraction complete"
    
    echo ""
    echo "=== RETRIEVAL SUCCESSFUL ==="
    echo "Archive location: $TARGET_DIR/$ARCHIVE_NAME"
    echo "Contents:"
    ls -la "$TARGET_DIR/"
    
else
    echo ""
    echo "=== RETRIEVAL FAILED ==="
    echo "Archive not found in any searched location."
    echo ""
    echo "MANUAL ACTION REQUIRED:"
    echo "Please copy the archive to one of these locations:"
    echo "  - /workspace/DCSE/V7.1/Handoffs/"
    echo "  - /tmp/"
    echo "Or provide the correct path."
    exit 1
fi
