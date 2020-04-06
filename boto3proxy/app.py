import datetime
import json
import typing
from functools import lru_cache

import boto3
from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Route


@lru_cache
def get_client(service):
    return boto3.client(service)


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat() + 'Z'
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        return super().default(obj)


class CustomJSONResponse(Response):
    media_type = "application/json"
    json_encoder = CustomJsonEncoder(
        ensure_ascii=False,
        allow_nan=False,
        indent=None,
        separators=(",", ":"),
    )

    def render(self, content: typing.Any) -> bytes:
        return self.json_encoder.encode(content).encode('utf-8')


async def client_endpoint(request):
    service = request.path_params['service']
    method = request.path_params['method']
    body = await request.body()
    payload = json.loads(body.decode('utf-8')) if body else {}
    client = get_client(service)
    client_method = getattr(client, method)
    resp = client_method(**payload)
    return CustomJSONResponse(resp)


def startup():
    print('Ready to go')


routes = [
    Route('/client/{service}/{method}', client_endpoint, methods=['GET', 'POST']),
]

app = Starlette(debug=True, routes=routes, on_startup=[startup])
