from django.urls import re_path
from .views import AmisProxyAPIView

urlpatterns = [
    re_path(r'^(?P<path>.*)$', AmisProxyAPIView.as_view()),
]
