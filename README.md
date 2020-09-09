# scrapy_ddiy
scrapy 项目练习、自定义框架组件  

Read the [Document](https://github.com/LZC6244/scrapy_ddiy/wiki)

目前正在全力完善自定义框架，有时间的话会逐渐完善文档...

## 环境需求
- Redis server
- MongoDB server

## 运行爬虫
> python run_spider.py spider_name
  
**or**

> python run_spider.py spider_name -a xx=xx -a xx=xx

运行 Redis 爬虫前请为其灌入种子  
如运行 script/set_redis_demo_spider.py 为 redis_demo_spider 灌入种子

## 功能概览
- [x] 当请求无 User-Agent 时，为其设置随机 User-Agent
- [x] 日志文件轮询机制
  - 默认启用轮询`(LOG_TIME_ROTATING参数)`
  - 启用轮询时默认每天`(00:00)`轮询一次日志文件
- [x] 启用日志时可以决定是否保留输出到控制台，默认保留输出`(LOG_TO_CONSOLE参数)`
- [x] 自动创建 `Item` ，使用 nosql 时不必每次定义 item
- [x] 默认禁用 **Telnet Console**
- [ ] 预警功能，暂定钉钉和邮件
- [ ] **spidermiddlewares** 处理解析异常，异常保存到 **MongoDB** ...
- [ ] **downloanmiddlewares** 处理请求、响应异常
- [x] **Redis** 基本爬虫
- [x] 记录爬取状态的下载中间件，设置默认 `errback`

## 爬虫列表
- 自定义框架完善的差不多后将会逐渐添加练习爬虫...

## TODO
- [ ] 使用 **ORM** 添加处理 sql 数据库的管道
- [ ] 去重队列可选择使用布隆过滤器
- [ ] 框架层面处理 Redis 爬虫中需要去重但是重试指定次数后仍失败的请求，将其从去重队列删除
- [x] 爬虫提供发送告警信息方法
- [ ] 钉钉提醒时接入 `@` 某（些）人功能

## 注意事项
- 使用 `-a` 传递参数时请注意该参数名是否会影响爬虫本身逻辑，scrapy 原生会将传递的参数置为爬虫的属性