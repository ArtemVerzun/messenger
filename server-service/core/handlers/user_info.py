from core.converters import ResponseConstructor
from core.types import ResponseType
from database import Database
from statistics import Statistics


async def user_info(request):
    info = await Database.get_user_info(request.data.user_id)
    return ResponseConstructor.create(
        ResponseType.USER_INFO,
        user_id=request.data.user_id,
        login=info[0],
        first_name=info[1],
        last_name=info[2]
    )
