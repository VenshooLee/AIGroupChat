tell application "Finder"
    activate
    delay 1
    tell disk "GroupChat"
        set current view of container window to icon view
        set the bounds of container window to {100, 100, 700, 400}
        delay 0.5
        try
            set position of item "GroupChat.app" to {100, 120}
        end try
        delay 0.5
        try
            set position of item "Applications" to {420, 120}
        end try
    end tell
end tell
