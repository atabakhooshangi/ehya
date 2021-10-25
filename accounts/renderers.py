from rest_framework import renderers
import json


class Renderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):

        if 'ErrorDetail' in str(data):
            l_data = dict()
            l_data['isDone'] = False
            l_data['data'] = data
            response = json.dumps(l_data)
        else:
            l_data = dict()
            l_data['isDone'] = True
            l_data['data'] = data
            response = json.dumps(l_data)
        return response
