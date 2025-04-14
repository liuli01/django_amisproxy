# django-amisproxy

============
django-amisproxy
============

django-amisproxy 将django_rest_admin自动生成的drf标准api接口转换成amis后端服务接口应用，方便amis前端直接使用。

## django-amis-render  管理前端自动生成文档
https://pypi.org/project/django-amis-render/

## django_rest_admin 管理后端自动生成文档
https://pypi.org/project/django-rest-admin/


Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "django-amisproxy",
    ]

``django-rest-admin``的服务地址
API_PROXY_TARGET = 'http://localhost:8000/api/'

2. Include the django-amisproxy URLconf in your project urls.py like this::

    path('amis-api/', include('amisproxy.urls')),

3. Run ``python manage.py migrate`` to create the models.

4. Start the development server and visit the admin to create a poll.

5. Visit the ``/amis-api/`` 替换 ``django-rest-admin``的服务地址``/api/``进行访问