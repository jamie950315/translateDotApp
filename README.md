### get all strings from MyApp.app and then store to all_strings.txt
```bash
strings MyApp.app/Contents/MacOS/MyApp > all_strings.txt
```

### filter, make the file more clean
```bash
grep -E '^[A-Za-z0-9[:punct:] ]{2,}$' all_strings.txt \
  | grep ' ' > ui_strings.txt
```

### sign the app to use it
```bash
codesign --force --deep --sign - MyApp.app
```
