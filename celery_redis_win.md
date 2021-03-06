## 环境准备
- python3.5.4
- [windows redis](https://github.com/MicrosoftArchive/redis/releases)
- ```pip install celery```
- ```pip install redis```

### windows下启动redirs server
- ```redis-server.exe redis.windows.conf```
![image.png](https://upload-images.jianshu.io/upload_images/2231755-5e48f3f31e4198d6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### celery配置

- 项目的settings.py文件修改：

 ```
# celery 设置
# celery中间人 redis://redis服务所在的ip地址:端口/数据库号
BROKER_URL = 'redis://127.0.0.1:6379/0'
# celery结果返回，可用于跟踪结果
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

# celery内容等消息的格式设置
CELERY_ACCEPT_CONTENT = ['application/json', ]
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# celery时区设置，使用settings中TIME_ZONE同样的时区
CELERY_TIMEZONE = TIME_ZONE

```

- 项目文件夹下添加celery.py文件：

```
# coding:utf-8
from __future__ import absolute_import, unicode_literals

from celery import Celery
from django.conf import settings
import os

# 获取当前文件夹名，即为该Django的项目名
project_name = os.path.split(os.path.abspath('.'))[-1]
project_settings = '%s.settings' % project_name

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', project_settings)

# 实例化Celery,网上很多教程这里都是没有设置broker造成启动失败
app = Celery('tasks', broker='redis://127.0.0.1:6379/0')

# 使用django的settings文件配置celery
app.config_from_object('django.conf:settings')

# Celery加载所有注册的应用
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

```
- 项目的init.py文件修改：

```
# 引入celery实例对象
from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app
__all__ = ['celery_app]
```

### 测试代码
- 如：在app01（项目名）／tasks.py：
- 关于task，并不是一定要把所有的task放在tasks.py，可以放在其他类里面，只要在函数上加@task即可

```
import time
from celery import task
@task
def add(a,b):
    print("这是任务开始")
    print(a+b)
    time.sleep(10)
    print("这是任务结束")
```

- url配置如下：
```
    path('add', views.add, name="add")
```

- view代码

```
from . import tasks
def add(request,*args,**kwargs):
    tasks.add.delay(1,2)
    result = {'code': 0, 'msg': '这是一个后台任务'}
    return JsonResponse(result)
```

### 再次配置
- 在manger.py目录执行下面的代码，注意网上的资料大部分执行的命令有问题，造成启动报错，比如这个就是错误的，```python manage.py celery -A celery worker --loglevel=info```，请用下面的命令

```
celery -A djangoApi worker --pool=solo -l info
```

-  启动项目,```python manager.py runserver 0.0.0.0:8081```

### 运行项目 

- 访问add
![image.png](https://upload-images.jianshu.io/upload_images/2231755-b8f4120501e54ad7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 查看关键日志
```
[tasks]
  . api.base.BaseViewTask.task_run
  . api.tasks.add

[2019-04-07 13:26:02,855: INFO/MainProcess] Connected to redis://127.0.0.1:6379/0
[2019-04-07 13:26:02,869: INFO/MainProcess] mingle: searching for neighbors
[2019-04-07 13:26:03,911: INFO/MainProcess] mingle: all alone
[2019-04-07 13:26:03,926: WARNING/MainProcess] e:\app\python35\lib\site-packages\celery\fixups\django.py:202: UserWarning: Using settings.DEBUG leads to a memory leak, never use this setting in production environments!
  warnings.warn('Using settings.DEBUG leads to a memory leak, never '
[2019-04-07 13:26:03,926: INFO/MainProcess] celery@PC-20181208QWQO ready.
[2019-04-07 13:29:56,889: INFO/MainProcess] Received task: api.tasks.add[9fd98fd0-50ae-427f-8f33-52d1e4b43068]
[2019-04-07 13:29:56,894: WARNING/MainProcess] 这是任务开始
[2019-04-07 13:29:56,895: WARNING/MainProcess] 3
[2019-04-07 13:30:06,896: WARNING/MainProcess] 这是任务结束
[2019-04-07 13:30:06,898: INFO/MainProcess] Task api.tasks.add[9fd98fd0-50ae-427f-8f33-52d1e4b43068] succeeded in 10.0s: None

```

## 其他
- 如何结合前端，如ajax来联合使用？
  - 表中我加了个extend字段，每次在执行耗时任务后，页面按钮根据extend字段值进行判断
  - 如1表示执行中，0表示没有执行，2执行完成，来判定按钮是否可以再次点击等