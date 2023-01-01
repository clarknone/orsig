from django.http import QueryDict
import json
from rest_framework import parsers


class MultipartJsonParser(parsers.MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(
            stream,
            media_type=media_type,
            parser_context=parser_context
        )
        # find the data field and parse it
        if 'data' not in result.data:
            result.data['data'] = ''
        data = json.loads(result.data["data"])
        return parsers.DataAndFiles(data, result.files)
