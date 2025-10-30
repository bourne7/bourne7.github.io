# Gradle 笔记

## 删除文件和文件夹

```gradle
task myDeleteFolders(type: Delete) {
    delete 'src/main/resources/base'
}

task myDeleteFiles(type: Delete) {
    delete fileTree("src").matching {
        include "main/resources/base/*.*"
    }
}
```