from loguru import logger

from core.converters import ResponseConstructor
from core.types import ResponseType
from core.verification import Verify
from database import Database


async def recovery_code_verification(request):
    _email, _login = request.data.email, request.data.login
    if not await Database.exists_email(request.data.email) and _email:
        logger.info(f'\nОтклонено подтверждение кода для восстановления пароля {request.data.email}: {request.ip}')
        return ResponseConstructor.create(ResponseType.REJECT, message='Данный email не зарегистрирован!')
    if not await Database.exists_login(request.data.login) and _login:
        logger.info(f'\nОтклонено подтверждение кода для восстановления пароля {request.data.login}: {request.ip}')
        return ResponseConstructor.create(ResponseType.REJECT, message='Данный логин не зарегистрирован!')
    if not request.data.email:
        _email = await Database.get_email(login=_login)
    if await Verify.verification(
            email=_email,
            code=request.data.code
    ):
        logger.info(f'\nПодтверждён код из почты для восстановления пароля {request.data.email}: {request.ip}')
        return ResponseConstructor.create(ResponseType.ACCEPT, message='Восстановление пароля подтверждёно.')
    else:
        logger.info(f'\nОтклонён код подтверждения для восстановления пароля '
                    f'{_email or _login} - {request.data.code}: {request.ip}')
        return ResponseConstructor.create(ResponseType.REJECT, message='Неверный код!')
