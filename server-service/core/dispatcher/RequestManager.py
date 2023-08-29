from loguru import logger

from core.converters import RequestParser, ResponseConstructor
from core.handlers import handlers
from core.types import ResponseType, RequestType


class RequestManager:
    @classmethod
    async def handle_request(cls, data, ip, port):
        to_send = None
        try:
            request = RequestParser.extract_request(data)
            request.ip, request.port = ip, port
            to_send = await handlers[RequestType(request.type)](request)
        except ValueError as err:
            logger.warning(err)
            to_send = ResponseConstructor.create(ResponseType.ERROR, message="Невалидный запрос.")
        except KeyError:
            logger.warning('Получен неизвестный тип запроса. Нет соответствующего хендлера.')
            to_send = ResponseConstructor.create(ResponseType.ERROR, message="Запрос не распознан.")
        finally:
            return bytes(to_send if to_send else ResponseConstructor.create(
                ResponseType.ERROR, message="Внутрисерверная ошибка."), encoding="utf-8")
