from rest_framework import renderers
import json
from uuid import UUID


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


class Renderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):

        if 'ErrorDetail' in str(data):
            response = json.dumps({'isDone': False, 'data': data}, cls=UUIDEncoder)
        else:
            response = json.dumps({'isDone': True, 'data': data}, cls=UUIDEncoder)
        return response


class SimpleRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):

        if 'ErrorDetail' in str(data):
            response = json.dumps({'isDone': False}, cls=UUIDEncoder)
        else:
            response = json.dumps({'isDone': True}, cls=UUIDEncoder)
        return response
