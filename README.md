
# django-amisproxy
============ django-amisproxy 标准模板============ 

django-amisproxy 将django_rest_admin自动生成的drf标准api接口转换成amis后端服务接口应用，方便amis前端直接使用BI。

# 快速设置
1. "amisproxy" 在 INSTALLED_APPS setting 加入 :

INSTALLED_APPS = [ ..., "amisproxy", ]

2. 必须设置Drf分页查询
```
REST_FRAMEWORK = {
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ]
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination', 
    'PAGE_SIZE': 10, # 每页显示个数
}

API_PROXY_TARGET = 'http://localhost:8000/api/'

```
3. 项目路由mysite/urls.py:
```
path('amis-api/', include('amisproxy.urls')),
````
4. 数据迁移
```
manage.py migrate 
```
5. 登录django管理 /admin 完成数据配置
```
/amis-api/ 替换 django-rest-admin的服务地址/api/进行访问
```


# 前后端全局配合使用

## 1、安装
```
pip install django-amis-render django-amis-render django-amisproxy
```
### django-amis-render
管理前端自动生成文档https://pypi.org/project/django-amis-render/
### django-rest-admin
管理后端自动生成文档https://pypi.org/project/django-rest-admin/
### django-amisproxy
drf转amis后端服务文档 https://pypi.org/project/django-amisproxy/
```
django-admin startproject mysite .
django-admin startapp rest_admin_app

mkdir -p myRenderApp/static/amis_json
```


## 2、修改设置 mysite/setting.py

```
INSTALLED_APPS = [
    'amisproxy',
    
    'rest_framework',
    'django_filters',
    'django_rest_admin',

    'rest_admin_app',
    "django_amis_render",
    "myRenderApp",
]

# DJANGO_REST_ADMIN 自动生成restful应用地址
API_PROXY_TARGET = 'http://localhost:8000/api/'
# DJANGO_REST_ADMIN 自动生成restful应用目录
DJANGO_REST_ADMIN_TO_APP='rest_admin_app'


REST_FRAMEWORK = {
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination', #分页
    'PAGE_SIZE': 10, # 每页显示个数
}

# 修改中文
LANGUAGE_CODE = 'zh-hans'
# 修改上海时间
TIME_ZONE = 'Asia/Shanghai'
```

## 3、修改路由mysite/urls.py
```
urlpatterns = [
    path('admin/', admin.site.urls),
    path('front/', include('django_amis_render.urls')),
    path('render/', include('myRenderApp.urls')),
    path('api/', include('rest_admin_app.urls')),
    path('amis-api/', include('amisproxy.urls')),
]

```
## 4、创建示例模型rest_admin_app/models.py
```
class FisrtModel(models.Model):
    created = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    code = models.TextField(blank=True, null=True)
    linenos = models.BooleanField(auto_created=True, default=False)

    class Meta:
        managed = True
        db_table = 'fisrt_model'
```

## 5、 创建示例前端CURD表单 myRenderApp/static/amis_json/curd_bak.json  
```
https://gitee.com/liulipython/file/raw/master/amis_json/curd_bk.json

```

```
## 创建迁移文件
python manage.py makemigrations
python manage.py migrate
``
## 创建用户
```
python manage.py createsuperuser --username admin --email 525334480@qq.com
## 修改密码
```
python manage.py changepassword admin
```
## 最终访问
/admin 生成rest服务，生成json服务
/amis-api/ 替换 django-rest-admin的服务地址/api/进行访问