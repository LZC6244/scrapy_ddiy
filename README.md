# scrapy_ddiy
scrapy 项目练习、自定义框架组件

## 环境需求
- Redis server
- MongoDB server

## 功能特点
### 随机 UA
- 当请求无 UA 时，为其设置随机 UA
### 日志文件轮询机制
- 默认启用轮询`(LOG_TIME_ROTATING参数)`
- 启用轮询时默认每天`(00:00)`轮询一次日志文件
### 启用日志时可以决定是否保留输出到控制台
- 默认保留输出`(LOG_TO_CONSOLE参数)`