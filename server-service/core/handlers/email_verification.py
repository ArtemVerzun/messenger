from loguru import logger

from database import Database
from core.converters import ResponseConstructor
from core.types import ResponseType
from core.verification import Verify


async def email_verification(request):
    if await Database.exists_email(request.data.email):
        logger.info(f'Отклонено подтверждение почты нового пользователя {request.data.email}: {request.ip}')
        return ResponseConstructor.create(ResponseType.REJECT, message='Данный email уже зарегистрирован!')
    if await Database.exists_login(request.data.login):
        logger.info(f'Отклонено подтверждение логина нового пользователя {request.data.login}: {request.ip}')
        return ResponseConstructor.create(ResponseType.REJECT, message='Данный логин уже зарегистрирован!')
    try:
        await Verify.add_code(email=request.data.email, login=request.data.login)
    except ValueError as err:
        raise
        logger.error(err)
        return ResponseConstructor.create(
            ResponseType.ERROR, message='Не удалось отправить код подтверждения на указанный адрес электронной почты.')
    logger.info(f'Отправлен код подтверждения почты {request.data.email}: {request.ip}')
    return ResponseConstructor.create(ResponseType.ACCEPT, message='Отправлен код на указанный адрес электронной почты.')
