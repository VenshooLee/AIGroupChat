-- AppleScript to create professional DMG layout
-- Run with: osascript create-dmg-layout.applescript

-- Configuration
property appName : "GroupChat"
property dmgName : "GroupChat"
property iconSize : 100

-- Get the dist folder path
set currentPath to POSIX file "/Users/bidder/Documents/groupchat/dist"
set appPath to POSIX file "/Users/bidder/Documents/groupchat/dist/GroupChat.app"

-- Create temporary mount point
set mountPoint to "/tmp/dmg-temp"

-- Create DMG
do shell script "rm -rf " & mountPoint & " GroupChat-temp.dmg && mkdir -p " & mountPoint

-- Copy app to mount point
do shell script "cp -R '/Users/bidder/Documents/groupchat/dist/GroupChat.app' '" & mountPoint & "/'"

-- Create Applications symlink
do shell script "ln -sf /Applications '" & mountPoint & "/Applications'"

-- Create DMG image
do shell script "hdiutil makehybrid -o '/tmp/GroupChat-temp.dmg' -hfs -hfs-volume-name '" & dmgName & "' '" & mountPoint & "'"

-- Convert to compressed UDZO
do shell script "hdiutil convert '/tmp/GroupChat-temp.dmg' -format UDZO -o '/Users/bidder/Documents/groupchat/dist/" & dmgName & ".dmg'"

-- Clean up
do shell script "rm -rf '/tmp/GroupChat-temp.dmg' '" & mountPoint & "'"

-- Attach the DMG for layout editing
set dmgPath to POSIX file "/Users/bidder/Documents/groupchat/dist/GroupChat.dmg"
set attachResult to do shell script "hdiutil attach '" & (POSIX path of dmgPath) & "' -mountpoint '/tmp/dmg-layout' -nobrowse"

-- Open Finder window
tell application "Finder"
    activate
    open disk "GroupChat"
end tell

display dialog "Arrange the icons as you like, then click OK to finish." buttons {"OK"} default button 1 giving up after 300

-- Detach the DMG
do shell script "hdiutil detach '/tmp/dmg-layout' -force"

display dialog "DMG created successfully at: /Users/bidder/Documents/groupchat/dist/GroupChat.dmg" buttons {"OK"} default button 1
