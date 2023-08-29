import json
from json import JSONDecodeError

from core.types import Request, requests, RequestType


class RequestParser:
    @classmethod
    def extract_request(cls, request) -> Request:
        json_request = json.loads(request)
        try:
            parsed_request = Request.construct(
                type=json_request['type'],
                data=requests[RequestType(json_request['type'])].parse_obj(json_request['data']),
                ip=None
            )
        except JSONDecodeError:
            raise ValueError('Получен невалидный запрос.')
        return parsed_request
