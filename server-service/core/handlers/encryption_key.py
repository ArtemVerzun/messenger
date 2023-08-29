from loguru import logger

from core.converters import ResponseConstructor
from core.types import ResponseType
from core.security import Cryptographer
from database import Database

__all__ = ['encryption_key']


async def encryption_key(request):
    if request.data.login and not await Database.exists_login(request.data.login):
        answer = ResponseConstructor.create(ResponseType.REJECT, message='Несуществующий логин.')
        logger.info(f'Попытка получения ключа шифрования по несуществующему логину '
                    f'{request.data.login}: {request.ip}')
    elif request.data.email and not await Database.exists_email(request.data.email):
        answer = ResponseConstructor.create(ResponseType.REJECT, message='Несуществующий адрес электронной почты.')
        logger.info(f'Попытка получения ключа шифрования по несуществующему адресу электронной почты '
                    f'{request.data.login}: {request.ip}')
    else:
        answer = ResponseConstructor.create(ResponseType.KEY, key=Cryptographer.get_public_key())
        logger.info(f'Выдан публичный ключ: {request.ip}')
    return answer
