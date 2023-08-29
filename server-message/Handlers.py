from datetime import datetime

from DataTypes import Type

from loader import storage


class Handlers:
    __uptime = dict()

    @classmethod
    def init(cls, request):
        """
        Set uptime into request.
        """
        _user = request['from_id']
        if _user not in cls.__uptime:
            cls.__uptime[_user] = 0
        if cls.__uptime[_user] == request['last_update']:
            request['messages'] = storage.get_messages(
                last_message_id=request['last_message_id'],
                target_id=_user
            )
        else:
            request['messages'] = storage.get_messages(
                last_message_id=-1,
                target_id=_user
            )
        request['last_update'] = cls.__uptime[_user]
        return request

    @classmethod
    def send_message(cls, request):
        _from_id = request['from_id']
        _to_id = request['to_id']
        request['date_time'] = cls.timestamp()
        _message = request['message']
        # save message to db
        request['message_id'] = storage.save_message(
            request['from_id'],
            request['to_id'],
            request['date_time'],
            request['message']
        )
        return request

    @classmethod
    def delete_message(cls, request):
        """
        Update __uptime.
        Set uptime into request.
        """
        _from_id = request['from_id']
        _to_id = request['to_id']
        _message_id = request['message_id']
        # delete message from db
        storage.delete_message(_message_id)
        request['last_update'] = cls.__update_uptime(_from_id, _to_id)
        return request

    @classmethod
    def delete_dialog(cls, request):
        """
        Update __uptime.
        Set uptime into request.Set uptime into request.
        """
        _from_id = request['from_id']
        _to_id = request['to_id']
        # delete message history from db (for all)
        storage.delete_dialog(
            user1_id=_from_id,
            user2_id=_to_id
        )
        request['last_update'] = cls.__update_uptime(_from_id, _to_id)
        return request

    @classmethod
    def __update_uptime(cls, _from, _to):
        _time = cls.timestamp()
        cls.__uptime[_from] = _time
        cls.__uptime[_to] = _time
        return _time

    @classmethod
    def timestamp(cls):
        return datetime.now().timestamp() * 1000

    @staticmethod
    def error(info):
        return {
            'type': Type.ERROR,
            'error': info
        }
