# 软件使用技巧总结

### Visual Studio Code

> Ctrl+Shift+L

Select all occurrences of current selection
editor.action.selectHighlights

> Ctrl+F2 

Select all occurrences of current word
editor.action.changeAll

### kindle Calibre

使用Calibre轉換TXT電子書(含目錄)並傳送至Kindle Paperwhite操作全攻略

> http://jdev.tw/blog/4388/kindle-with-calibre-conversion

### windows terminal

透明效果

```json
    "profiles": {
        "defaults": {
            "useAcrylic": true,
            "acrylicOpacity": 0.6
        }
    }
```


### idea file size

> https://stackoverflow.com/questions/23057988/file-size-exceeds-configured-limit-2560000-code-insight-features-not-availabl

On older versions, there's no GUI to do it. But you can change it if you edit the IntelliJ IDEA Platform Properties file:

```
#---------------------------------------------------------------------
# Maximum file size (kilobytes) IDE should provide code assistance for.
# The larger file is the slower its editor works and higher overall system memory requirements are
# if code assistance is enabled. Remove this property or set to very large number if you need
# code assistance for any files available regardless their size.
#---------------------------------------------------------------------
idea.max.intellisense.filesize=2500
```