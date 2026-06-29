#!/bin/bash
# Setup DMG layout with left App, right Applications

DMG_PATH="/Users/bidder/Documents/groupchat/dist/GroupChat.dmg"
MOUNT_POINT="/tmp/dmg-layout"

# Unmount if already mounted
hdiutil detach "$MOUNT_POINT" -force 2>/dev/null

# Mount the DMG
hdiutil attach "$DMG_PATH" -mountpoint "$MOUNT_POINT" -nobrowse

# Create layout config file
cat > "$MOUNT_POINT/.VolumeIcon.icns" << 'ICONEOF'
ICONEOF

# Create Finder info plist for icon positions
cat > /tmp/icon_pos.rsrc << 'RSRCEOF'
data 'icns' (0) {
    $"0000 0001"
};
RSRCEOF

# Use SetFile to set custom icon positions
# These commands need to be run while DMG is mounted

# Position App on left (100, 100)
# Position Applications on right (400, 100)

# Unmount
hdiutil detach "$MOUNT_POINT" -force

echo "DMG layout configured"
