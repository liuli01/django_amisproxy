import re
import requests

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class AmisProxyAPIView(APIView):
    """
    通用 amis 请求代理视图（适配 djangorestframework 接口）
    - 支持 GET / POST / PUT / PATCH / DELETE
    - 自动转化分页结构
    - 支持 POST 批量删除（路径如: /model/batch-delete/）
    """

    def forward(self, method, path, request):
        # 批量删除特殊处理
        if method.lower() == 'post' and path.endswith('batch-delete/'):
            return self.handle_batch_delete(path, request)

        # 目标 API 地址
        api_base = getattr(settings, 'API_PROXY_TARGET', 'http://localhost:8000/api/')
        target_url = api_base.rstrip('/') + '/' + path.lstrip('/')

        headers = {k: v for k, v in request.headers.items() if k.lower() != 'host'}
        data = request.data if method in ['post', 'put', 'patch'] else None
        params = request.query_params if method == 'get' else None

        try:
            response = requests.request(
                method=method,
                url=target_url,
                headers=headers,
                json=data,
                params=params,
                timeout=10,
            )

            try:
                result = response.json()
            except Exception:
                return Response({'status': 1, 'msg': '非 JSON 响应'}, status=response.status_code)

            # 分页结构处理
            if isinstance(result, dict) and 'results' in result and 'count' in result:
                return Response({
                    'status': 0,
                    'msg': 'ok',
                    'data': {
                        'items': result['results'],
                        'total': result['count'],
                        'next': result.get('next'),
                        'previous': result.get('previous'),
                    }
                }, status=response.status_code)

            # 普通结构直接包裹
            return Response({
                'status': 0,
                'msg': 'ok',
                'data': result
            }, status=response.status_code)

        except requests.RequestException as e:
            return Response({'status': 1, 'msg': str(e)}, status=status.HTTP_502_BAD_GATEWAY)
    def handle_batch_delete(self, path, request):
        """
        POST /amis-api/<model>/batch-delete/
        请求体支持以下格式：
        - {"ids": "1,2,3"}（逗号分隔字符串）
        - {"ids": [1, 2, 3]}（列表）
        - [{"id": 1}, {"id": 2}]（列表对象）
        """
        match = re.match(r'(?P<model_path>.+)/batch-delete/?$', path)
        if not match:
            return Response({'status': 1, 'msg': '无效路径'}, status=400)

        model_path = match.group('model_path')
        raw_ids = request.data.get('ids')

        # 兼容不同格式
        ids = []
        if isinstance(raw_ids, str):
            ids = [int(i) for i in raw_ids.split(',') if i.strip().isdigit()]
        elif isinstance(raw_ids, list):
            ids = raw_ids
        elif isinstance(request.data, list):  # 对象数组
            ids = [item.get('id') for item in request.data if isinstance(item, dict) and 'id' in item]

        if not isinstance(ids, list) or not ids:
            return Response({'status': 1, 'msg': '缺少有效的 ID 列表'}, status=400)

        api_base = getattr(settings, 'API_PROXY_TARGET', 'http://localhost:8000/api/')
        headers = {k: v for k, v in request.headers.items() if k.lower() != 'host'}

        results = []
        for _id in ids:
            delete_url = f"{api_base.rstrip('/')}/{model_path}/{_id}/"
            try:
                resp = requests.delete(delete_url, headers=headers, timeout=10)
                results.append({
                    'id': _id,
                    'status_code': resp.status_code,
                    'success': resp.status_code in [200, 204]
                })
            except requests.RequestException as e:
                results.append({
                    'id': _id,
                    'status_code': 500,
                    'error': str(e),
                    'success': False
                })

        return Response({
            'status': 0,
            'msg': '批量删除完成',
            'data': results
        })
    # 映射 HTTP 方法
    def get(self, request, path=''):
        return self.forward('get', path, request)

    def post(self, request, path=''):
        return self.forward('post', path, request)

    def put(self, request, path=''):
        return self.forward('put', path, request)

    def patch(self, request, path=''):
        return self.forward('patch', path, request)

    def delete(self, request, path=''):
        return self.forward('delete', path, request)
