from core.types.Responses import Response, responses


class ResponseConstructor:

    @classmethod
    def create(cls, response_type, **kwargs):
        data = dict()
        for field in kwargs:
            data[field] = kwargs[field]
        return Response.construct(
            type=response_type,
            data=responses[response_type].parse_obj(data)
        ).json()
