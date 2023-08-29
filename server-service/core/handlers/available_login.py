from loguru import logger

from core.converters import ResponseConstructor
from database import Database
from core.types import ResponseType


async def available_login(request):
    if await Database.exists_login(login=request.data.login):
        return ResponseConstructor.create(ResponseType.REJECT, message="Данный логин уже используется.")
    else:
        return ResponseConstructor.create(ResponseType.ACCEPT, message="Данный логин свободен.")
