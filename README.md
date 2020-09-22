# scrapy_ddiy
Scrapy 自定义框架组件，项目练习, 支持 Redis 爬虫

**请在项目路径下运行本项目相关程序！**  

Read the [Document](https://github.com/LZC6244/scrapy_ddiy/wiki)

## 环境需求
- Redis server 4.0.9+
- MongoDB server 4.2+

## 项目配置
本项目分为线上、测试环境，通过 `settings => ENV_FLAG_DDIY` 进行区分。  
线上环境相关配置可通过 `ddiy_settings/online_settings.py` 进行配置

## 新建爬虫
- 普通 Scrapy 爬虫请继承 `scrapy_ddiy.utils.spiders.ddiy_base.DdiyBaseSpider` 爬虫
- Redis 爬虫请继承 `scrapy_ddiy.utils.spiders.ddiy_redis.DdiyRedisSpider` 爬虫

## 运行爬虫
> python run_spider.py spider_name
  
**or**

> python run_spider.py spider_name -a xx=xx -a xx=xx

运行 Redis 爬虫前请为其灌入种子  
如运行 script/set_redis_demo_spider.py 为 redis_demo_spider 灌入种子

## 示例爬虫
- Scrapy 原生爬虫：demo_spider
- Redis 爬虫：redis_demo_spider

## 功能概览
- [x] 当请求无 User-Agent 时，为其设置随机 User-Agent
- [x] 日志文件轮询机制
  - 默认启用轮询`(settings => LOG_TIME_ROTATING)`
  - 启用轮询时默认每天`(00:00)`轮询一次日志文件，默认保留近三天轮询日志
- [x] 启用日志时可以决定是否保留输出到控制台，默认保留输出`(settings => LOG_TO_CONSOLE)`
- [x] 自动创建 `Item` ，使用 MongoDB 时不必每次定义 item ，直接 yield 解析好的 item 即可 (spider.process_parsed_item)
- [x] 默认禁用 **Telnet Console**
- [x] 异常邮件预警，钉钉自定义消息预警
- [x] **spidermiddlewares** 处理解析异常，异常保存到 **MongoDB** ...
- [ ] **downloanmiddlewares** 处理请求、响应异常（譬如重试？）
- [x] 记录爬取状态的下载中间件，设置默认 `errback`
- [x] MongoDB 管道自动创建索引`(settings => MONGO_INDEX_DICT)`
- [x] 去重队列可选择布隆过滤器  [如何使用？](https://github.com/LZC6244/scrapy_ddiy/wiki/%E5%8E%BB%E9%87%8D%E9%98%9F%E5%88%97%E4%BD%BF%E7%94%A8Redis%E5%B8%83%E9%9A%86%E8%BF%87%E6%BB%A4%E5%99%A8)

## 爬虫列表
- xxx
- xxx
- ...

## TODO
- [ ] 使用 **ORM** 添加处理 sql 数据库的管道
- [ ] 框架层面处理 Redis 爬虫中需要去重但是重试指定次数后仍失败的请求，将其从去重队列删除
- [x] 爬虫提供发送告警信息方法 (spider.send_ding_bot_msg)
- [ ] 钉钉发送预警消息时接入 `@` 某（些）人功能

## 注意事项
- `spider.process_parsed_item` 会默认通过请求计算 `_id` （当 item 传入 _id 不会将其覆盖）  
  由于 MongoDB 默认会将 _id 置为主键，当 **同一个请求中解析出多条数据** 时请注意配置   
  `spider.process_parsed_item` 不要计算 `_id` 或 为 item 传入 `_id`  
  （MongoDB 不存在 _id 时 会生成与入库时间相关的 ObjectId 作为主键）
- 非线上环境时（环境变量 'ENV_FLAG_DDIY' != 'online'），为了防止污染线上数据，会将数据库库名统一置为 `scrapy_ddiy_test`
- 使用 `-a` 传递参数时请注意该参数名是否会影响爬虫本身逻辑，Scrapy 原生会将传递的参数置为爬虫的属性
- MongoDB 管道目前仅支持单字段索引，若要创建复合索引或进行其他复杂操作，请自行在 spider.custom_init 方法中执行