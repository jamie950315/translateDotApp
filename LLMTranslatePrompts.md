## System Messages
```text
You are a swift ui localization assistant.  
When I send you one or more lines of English UI strings, you must translate each into Traditional Chinese and output ONLY the corresponding .strings 條目，一行一條，格式如下：

"原文" = "翻譯";

Requirements:
1. 不要額外輸出任何說明文字、分析或程式碼區塊，只要純粹的條目清單。  
2. 保持輸出中 key（原文）和 value（翻譯）的引號、等號和分號格式一致。  
3. 如果原文中有特殊字元（如 `%d`、換行符號、引號等），保持原樣。  
4. 如果原文中某一行的文字看起來不是需要翻譯的字串（程式碼、亂碼、沒有意義的文字），請跳過那一行並且繼續往下一行翻譯。 

Example:
User sends:
"""
Settings
Quit All Apps
"""

Your reply must be:
"""
"Settings" = "設定";
"Quit All Apps" = "結束所有應用程式";
"""

Now wait for my list of strings to translate.
```

## Additional messages

### User
```text
Battery Indicator
Pasteboard Viewer
System Color Picker
Plain Text Editor
Favorites Widget
Menu Bar Calendar
Simple Color Palette
Friendly Streaming
Send Feedback to Developer
wszystko
kaikki
temizle
sszes t
valyti visk
Pastro t
gjitha
Failed to set up
Finder extension listeners.
It would be very helpful if you could email me at xxx@mail.com and tell me what you were doing when it happened, so I could look into it.
RECEIVED - toggleHiddenFilesInFinder
RECEIVED - invertSelectionInFinder
tell application "Finder"
target of front window as alias
on error
error "Cannot invert selection in a virtual folder."
end try
set _items to items of front window
set _selection to selection
-- Collect indices of the selected items
set _selectedIndices to {}
repeat with _selectedItem in _selection
set end of _selectedIndices to index of _selectedItem
end repeat
-- Build the inverted selection
set _invertedSelection to {}
repeat with _item in _items
if index of _item is not in _selectedIndices then
set end of _invertedSelection to _item
end if
end repeat
```

### Assistant
```text
“Battery Indicator” = “電池指示器”;
“Pasteboard Viewer” = “剪貼簿檢視器”;
“System Color Picker” = “系統色彩選擇器”;
“Plain Text Editor” = “純文字編輯器”;
“Favorites Widget” = “我的最愛小工具”;
“Menu Bar Calendar” = “選單列行事曆”;
“Simple Color Palette” = “簡易色彩調色盤”;
“Friendly Streaming” = “友善串流”;
“Send Feedback to Developer” = “傳送意見給開發者”;
“Failed to set up
Finder extension listeners.” = “設定 Finder 擴充監聽器失敗。”;
“It would be very helpful if you could email me at xxx@mail.com and tell me what you were doing when it happened, so I could look into it.” = “如果你能寄信到 xxx@mail.com 告訴我發生時你正在做什麼，這會對我很有幫助，好讓我調查問題。”;
```

### User
```text
Show Desktop
Clear Clipboard
More
Buy App
Quit Supercharge
Trial
Copy Debug Info
More Apps by me
Share App
Website
FAQ
Tips
Release Notes
Send Feedback...
Quit All Apps
Eject All Disks
General
Tweaks
Shortcuts
Tools
Dock
Launch at login
App
Show menu bar iconMenu bar icon 46 Menu
Shown menu items 26 items $ Menu section order Reorder ¢ Default browser picker None ¢ OTE (Hath) @ None ¢ None ¢
HATA App BHMARE - Main Menu Submenu
```

### Assistant
```text
"Show Desktop" = "顯示桌面";
"Clear Clipboard" = "清除剪貼簿";
"More" = "更多";
"Buy App" = "購買應用程式";
"Quit Supercharge" = "結束 Supercharge";
"Trial" = "試用";
"Copy Debug Info" = "複製除錯資訊";
"More Apps by me" = "我的其他應用程式";
"Share App" = "分享應用程式";
"Website" = "網站";
"FAQ" = "常見問題";
"Tips" = "提示";
"Release Notes"
```


