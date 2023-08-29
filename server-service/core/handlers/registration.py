from loguru import logger

from core.security import Cryptographer, PasswordManager
from database import Database
from core.converters import ResponseConstructor
from core.types import ResponseType
from core.verification import Verify
from statistics import Statistics


async def registration(request):
    if await Verify.is_verified(request.data.email, request.data.login):
        if await Database.exists_login(login=request.data.login) or await Database.exists_email(email=request.data.email):
            logger.warning(
                f"Попытка регистрации существующего пользователя "
                f"{request.data.login or request.data.email}:"
                f" {request.ip}"
            )
            return ResponseConstructor.create(ResponseType.REJECT, message='Почта или логин уже зарегестрированы!.')
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
        db_answer = await Database.registration(
            login=request.data.login,
            password=password_hash,
            first_name=request.data.first_name,
            last_name=request.data.last_name,
            email=request.data.email
        )
        if db_answer:
            logger.info(f"Зарегистрирован новый пользователь {request.data.email}: {request.ip}")
            await Statistics.update_all()
            return ResponseConstructor.create(ResponseType.ACCEPT, message='Регистрация завершена.')
        else:
            logger.info(
                f'Отклонена регистрация нового пользователя (Недопустимые данные.) {request.data.email}: {request.ip}')
            return ResponseConstructor.create(ResponseType.REJECT, message='Недопустимые данные.')
    else:
        logger.warning(
            f'Отклонена регистрация нового пользователя (Почта или логин не подтверждены.) '
            f'{request.data.email or request.data.login}: {request.ip}')
        return ResponseConstructor.create(ResponseType.REJECT, message='Почта или логин не подтверждены.')
