from datetime import datetime

from database import Database


class Statistics:
    __online_users = dict()
    __online_ports = dict()
    __last_seen = dict()
    __all = 0

    @classmethod
    async def online_status(cls, user_id) -> (bool, float):
        if user_id in cls.__online_users:
            return True, None
        elif user_id not in cls.__last_seen:
            return False, -1
        else:
            return False, cls.__last_seen[user_id]

    @classmethod
    async def connection(cls, port, user_id=None):
        if user_id:
            if user_id not in cls.__online_users:
                cls.__online_users[user_id] = set()
            cls.__online_users[user_id].add(port)
        cls.__online_ports[port] = user_id

    @classmethod
    async def disconnection(cls, port):
        if port in cls.__online_ports:
            user_id = cls.__online_ports[port]
            del cls.__online_ports[port]
            if user_id:
                cls.__online_users[user_id].discard(port)
                if len(cls.__online_users[user_id]) == 0:
                    del cls.__online_users[user_id]
                    cls.__last_seen[user_id] = (datetime.now().timestamp() * 1000)

    @classmethod
    async def update_all(cls):
        cls.__all = await Database.get_count()

    @classmethod
    def get_offline_count(cls):
        _count = cls.__all - len(cls.__online_users)
        return _count if _count > 0 else 0

    @classmethod
    def get_online_count(cls):
        return len(cls.__online_users)
