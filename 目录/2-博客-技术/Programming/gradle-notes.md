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

## 升级项目里面的 wrapper

```bash
gradlew.bat wrapper --gradle-version latest
```