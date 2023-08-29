from core.converters import ResponseConstructor
from database import Database
from core.types import ResponseType


async def search(request):
    result = await Database.search_users(
        keyword1=request.data.keyword1,
        keyword2=request.data.keyword2
    )
    return ResponseConstructor.create(ResponseType.SEARCH_RESULTS,
                                      users=result
                                      )
