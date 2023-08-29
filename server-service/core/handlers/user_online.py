from loguru import logger

from core.converters import ResponseConstructor
from core.types import ResponseType
from statistics import Statistics


async def user_online(request):
    is_online, last_seen = await Statistics.online_status(request.data.user_id)
    return ResponseConstructor.create(
        ResponseType.USER_STATUS,
        is_online=is_online,
        last_seen=last_seen,
        message="Статус пользователя."
    )
