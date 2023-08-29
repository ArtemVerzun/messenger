from loguru import logger

from core.converters import ResponseConstructor
from core.security import Cryptographer, PasswordManager
from database import Database
from core.types import ResponseType
from statistics import Statistics


async def authentication(request):
    if request.data.email and not await Database.exists_email(email=request.data.email):
        logger.info(
            f"Отклонена аутентификация (Неверный адрес электронной почты.) "
            f"{request.data.email}: "
            f"{request.ip}")
    elif request.data.login and not await Database.exists_login(login=request.data.login):
        logger.info(
            f"Отклонена аутентификация (Неверный логин.) "
            f"{request.data.login}: "
            f"{request.ip}")
    elif not request.data.login and not request.data.email:
        logger.warning(
            f"Отклонена аутентификация (Пустой логин и пароль.) "
            f"{request.data.login}: "
            f"{request.ip}")
    else:
        try:
            password_from_request = Cryptographer.decrypt(request.data.password)
        except ValueError:
            logger.warning(
                f"Ошибка расшифровки пароля пользователя "
                f"{request.data.login or request.data.email}:"
                f" {request.ip}"
            )
            return ResponseConstructor.create(ResponseType.ERROR, message='Пароль отклонён системой безопасности.')

        # получение пароля из базы данных
        password_hash = await Database.get_password(login=request.data.login, email=request.data.email)
        if PasswordManager.verification(password_hash=password_hash, password=password_from_request):
            logger.info(
                f"Подтверждена аутентификация "
                f"{request.data.login or request.data.email}: "
                f"{request.ip}")
            if request.data.login:
                user_id = await Database.get_user_id_by_login(login=request.data.login)
            else:
                user_id = await Database.get_user_id_by_email(email=request.data.email)
            login = request.data.login or await Database.get_login(email=request.data.email)
            first_name = await Database.get_user_first_name(user_id=user_id)
            last_name = await Database.get_user_last_name(user_id=user_id)
            await Statistics.connection(port=request.port, user_id=user_id)
            return ResponseConstructor.create(ResponseType.AUTH_COMPLETE,
                                              message='Аунтентификация подтверждена',
                                              user_id=user_id,
                                              first_name=first_name,
                                              last_name=last_name,
                                              login=login
                                              )
        else:
            logger.info(
                f"Отклонена аутентификация (Неверный пароль.) "
                f"{request.data.login or request.data.email}: "
                f"{request.ip}")

    return ResponseConstructor.create(ResponseType.REJECT, message='Неверный логин или пароль.')
