from loguru import logger

from core.converters import ResponseConstructor
from core.types import ResponseType
from statistics import Statistics


async def logout(request):
    await Statistics.disconnection(port=request.port)
    logger.info(f'Выход из учётной записи. {request.port}: {request.ip}')
    return ResponseConstructor.create(ResponseType.ACCEPT, message="Выход выполнен")
