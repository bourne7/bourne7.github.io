# Java Tools 工具类

## JMC (Java Mission Control) 

高版本的的 JMC 启动会出问题, 原因是 jdk 版本太低了, 需要提高到 11 或者 17, 不能用 8. 如果这个时候我们不想修改全局的环境变量, 可以单独修改 JMC 的运行 JDK 版本.

```
jmc.ini

-vm
D:/java-17/bin/java
```