# &nbsp;&nbsp;&nbsp;Libras

> 基于[Flask]()框架的Web服务框架

简单封装了Flask框架，并提供了如下功能：

* 提供了`yaml | yml`格式文件配置，且配置文件可与工程分离，达到不同环境的配置更加灵活，

* 重写了`Flask`类，定义了统一异常处理、配置类、请求日志输出等。

* 实现对`blueprint`的包路径扫描机制，开发只需在对应包中，按规定格式实现 api接口，框架会自动注册到`flask blueprint`中。

* 使用外观模式，简化程序启动入口，只需一行代码即可启动。

## 使用方式

```
# 入口

from Libras import Application

if __name__ == '__main__':
    Application(packages='app.api', profile='/').run(host='0.0.0.0', port=9003)
```

其中参数说明：

1. packages: 指定`blueprint`的包路径，启动时会自动扫描并注册

2. profile: 指定配置文件所有目录 




