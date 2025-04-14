
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

