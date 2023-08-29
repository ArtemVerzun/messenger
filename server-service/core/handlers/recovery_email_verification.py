from loguru import logger

from database import Database
from core.converters import ResponseConstructor
from core.types import ResponseType
from core.verification import Verify


async def recovery_email_verification(request):
    _email, _login = request.data.email, request.data.login
    if not await Database.exists_email(request.data.email) and _email:
        logger.info(f'\nОтклонено подтверждение почты для восстановления пароля {request.data.email}: {request.ip}')
        return ResponseConstructor.create(ResponseType.REJECT, message='Данный email не зарегистрирован!')
    if not await Database.exists_login(request.data.login) and _login:
        logger.info(f'\nОтклонено подтверждение логина для восстановления пароля {request.data.login}: {request.ip}')
        return ResponseConstructor.create(ResponseType.REJECT, message='Данный логин не зарегистрирован!')
    try:
        if not request.data.email:
            _email = await Database.get_email(login=request.data.login)
        else:
            _login = await Database.get_login(email=request.data.email)
        await Verify.add_code(
            email=_email,
            login=_login
        )
    except ValueError as err:
        logger.error(err)
        return ResponseConstructor.create(
            ResponseType.ERROR, message='\nНе удалось отправить код подтверждения на указанный адрес электронной почты.')
    logger.info(f'\nОтправлен код подтверждения почты {_email or _login}: {request.ip}')
    return ResponseConstructor.create(ResponseType.ACCEPT,
                                      message='Отправлен код на указанный адрес электронной почты.')
