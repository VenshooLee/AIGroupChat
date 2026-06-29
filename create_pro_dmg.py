#!/usr/bin/env python3
"""
Create professional DMG with left App, right Applications layout
"""
import os
import subprocess
import shutil

def create_dmg_with_layout():
    dist_path = "/Users/bidder/Documents/groupchat/dist"
    dmg_path = f"{dist_path}/GroupChat.dmg"
    temp_mount = "/tmp/dmg-layout"
    temp_dir = "/tmp/dmg-source"

    # Clean up
    subprocess.run(["hdiutil", "detach", temp_mount, "-force"], capture_output=True)
    for p in [dmg_path, temp_dir, temp_mount]:
        if os.path.exists(p):
            if os.path.isdir(p):
                shutil.rmtree(p)
            else:
                os.remove(p)
    os.makedirs(temp_dir, exist_ok=True)

    # Copy app and create symlink
    app_src = f"{dist_path}/GroupChat.app"
    shutil.copytree(app_src, f"{temp_dir}/GroupChat.app")
    os.symlink("/Applications", f"{temp_dir}/Applications")

    # Create DMG
    subprocess.run([
        "hdiutil", "makehybrid", "-o", dmg_path,
        "-hfs", "-hfs-volume-name", "GroupChat",
        temp_dir
    ], check=True)

    print(f"DMG created: {dmg_path}")

    # Attach for layout setup
    subprocess.run([
        "hdiutil", "attach", dmg_path,
        "-mountpoint", temp_mount, "-nobrowse"
    ], check=True)

    # Set up icon positions using hfsplus
    # Left: App at position (150, 150)
    # Right: Applications link at position (450, 150)
    # Arrow from left to right

    # Use AppleScript to arrange icons
    applescript = '''
    tell application "Finder"
        tell disk "GroupChat"
            open
            set current view of container window to icon view
            set the bounds of container window to {100, 100, 700, 500}

            -- Get icon positions
            set appIcon to item "GroupChat.app"
            set appsLink to item "Applications"

            -- Position icons
            set position of appIcon to {120, 150}
            set position of appsLink to {420, 150}

            -- Set icon size
            set icon size of container window to 100
        end tell
    end tell
    '''

    try:
        subprocess.run(["osascript", "-e", applescript], check=True)
        print("Layout set. Finder window opened.")
        input("Arrange icons manually, then press Enter to finish...")
    finally:
        subprocess.run(["hdiutil", "detach", temp_mount, "-force"], capture_output=True)

    print(f"Done! DMG: {dmg_path}")

if __name__ == "__main__":
    create_dmg_with_layout()
