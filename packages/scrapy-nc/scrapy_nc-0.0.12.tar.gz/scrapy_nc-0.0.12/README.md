## scrapy_nc

### 安装

```
pip install scrapy_nc
```

### 使用


目前提供三个 Pipeline:

- scrapy_nc.pipelines.AMQPPipeline 发送队列 pipeline
- scrapy_nc.pipelines.OSSPipeline 保存 OSS pipeline
- scrapy_nc.pipelines.RedisDuplicatesPipeline Redis 去重 Pipeline

AMQPPipeline 使用方法：

安装 pika

```
pip install pika
```

配置 settings.py

```

MQ_USER = 'username'
MQ_PASSWORD = 'password'
MQ_HOST = ''
MQ_PORT = '5672'
MQ_VHOST = ''
MQ_NAME_SUFFIX = 'prod' # prod/dev
```

配置 items.py
