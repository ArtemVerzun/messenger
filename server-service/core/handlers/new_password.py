from loguru import logger

from core.security import Cryptographer, PasswordManager
from database import Database
from core.converters import ResponseConstructor
from core.types import ResponseType
from core.verification import Verify


async def new_password(request):
    _email, _login = request.data.email, request.data.login
    if not _email:
        if await Database.exists_login(_login):
            _email = await Database.get_email(login=_login)
        else:
            logger.info(f'\nОтклонена смена пароля пароля {_login or _email}: {request.ip}')
            return ResponseConstructor.create(ResponseType.REJECT, message='Данный email не зарегистрирован!')
    if not _login:
        if await Database.exists_email(_email):
            _login = await Database.get_login(email=_email)
        else:
            logger.info(f'\nОтклонена смена пароля пароля {_login or _email}: {request.ip}')
            return ResponseConstructor.create(ResponseType.REJECT, message='Данный email не зарегистрирован!')

    if await Verify.is_verified(_email, _login):
        try:
            encrypted_password = Cryptographer.decrypt(request.data.password).decode()
        except ValueError:
            logger.warning(
                f"Ошибка расшифровки пароля для пользователя "
                f"{request.data.login or request.data.email}:"
                f" {request.ip}"
            )
            return ResponseConstructor.create(ResponseType.ERROR, message='Ошибка расшифровки пароля.')
        password_hash = PasswordManager.hashing(password=encrypted_password)
        if not await Database.update_password(login=_login, password=password_hash):
            logger.warning(
                f'Ошибка при обновлении пароля {_email or _login}: {request.ip}')
            return ResponseConstructor.create(ResponseType.ERROR, message='Не удалось обновить пароль.')
        else:
            logger.info(
                f'Обновлён пароль {_email or _login}: {request.ip}')
            return ResponseConstructor.create(ResponseType.ACCEPT, message='Пароль успешно обновлён.')
    else:
        logger.warning(
            f"Попытка смены пароля без подтверждения почты. "
            f"{request.data.login or request.data.email}:"
            f" {request.ip}"
        )
        return ResponseConstructor.create(ResponseType.REJECT, message='Почта не подтверждена.')