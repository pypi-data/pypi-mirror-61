## scrapy_nc

### 安装

```
pip install scrapy_nc
```

### 使用

目前提供以下基础数据:

- scrapy_nc.item.BaseItem 基础 item
- scrapy_nc.pipelines.AMQPPipeline 发送队列 pipeline
- scrapy_nc.pipelines.OSSPipeline 保存 OSS pipeline
- scrapy_nc.pipelines.RedisDuplicatesPipeline Redis 去重 Pipeline

### BaseItem

```
from scrapy_nc.item import BaseItem

class XiaoyusanItem(BaseItem):
    pass
```

### AMQPPipeline

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

ITEM_PIPELINES = {
    'scrapy_nc.pipelines.AMQPPipeline': 302,
}

```

配置 items.py

```

from scrapy_nc.item import BaseItem

class XiaoyusanItem(BaseItem):
    test = scrapy.Field()

    def queue_names(self):
        return ['spider.medical.ncov_community.xiaoyusan'] # 需要发送的队列

```
