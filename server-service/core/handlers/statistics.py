from core.converters import ResponseConstructor
from core.types import ResponseType
from statistics import Statistics


async def statistics(_):
    return ResponseConstructor.create(
        ResponseType.STATS,
        online=Statistics.get_online_count(),
        offline=Statistics.get_offline_count()
    )
