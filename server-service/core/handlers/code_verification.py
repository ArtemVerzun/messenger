from loguru import logger

from core.converters import ResponseConstructor
from core.types import ResponseType
from core.verification import Verify


async def code_verification(request):
    if await Verify.verification(email=request.data.email, code=request.data.code):
        logger.info(f'Подтверждён код из почты для нового пользователя {request.data.email}: {request.ip}')
        return ResponseConstructor.create(ResponseType.ACCEPT, message='Адрес электронной почты подтверждён.')
    else:
        logger.info(f'Отклонён код подтверждения для нового пользователя '
                    f'{request.data.email} - {request.data.code}: {request.ip}')
        return ResponseConstructor.create(ResponseType.REJECT, message='Неверный код!')
