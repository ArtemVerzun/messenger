from PySide6.QtCore import QObject, Signal, Slot, Property
from typing import Optional

from core.system import Network, Storage
from core.protocols import RequestType, ResponseType
from core.converters import RequestConstructor, ResponseParser
from core.tools import Security, UserData, MessageData


class Service(Network):
    # Error info.
    __server_message = None
    __server_message: Optional[str]
    __default_server_message = 'Нет подключения к серверу.'
    __server_error = True

    __online = None
    __offline = None

    __auth_complete = False

    def __init__(self):
        super(Service, self).__init__(address='127.0.0.1', port=9077)
        self.socket.connected.connect(self.__get_encryption_key)
        self.socket.connected.connect(self.__update_authentication)
        self._Network__create_connection()
        MessageData.set_get_user_info(self.getUserInfo)

    @Slot(result=bool)
    def isError(self):
        return self.__server_error

    @Slot(result=int)
    def getMyId(self):
        return UserData.get_my_id()

    @Slot(result=str)
    def getMyFirstName(self):
        return UserData.get_my_first_name()

    @Slot(result=str)
    def getMyLastName(self):
        return UserData.get_my_last_name()

    @Slot(result=str)
    def getMyLogin(self):
        return UserData.get_my_login()

    @Slot(result=str)
    def getServerMessage(self):
        return self.__get_server_message()

    @Slot(str, str, str, str, str, result=bool)
    def registration(self, login, email, password, first_name, last_name):
        if not Security.key_is_set() or not self._send(
                RequestConstructor.create(
                    request_type=RequestType.REGISTRATION,
                    login=login,
                    password=Security.encrypt(password),
                    first_name=first_name,
                    last_name=last_name,
                    email=email)):
            return False
        return ResponseType(self.receive().type) == ResponseType.ACCEPT

    @Slot(str, str, result=bool)
    def emailVerification(self, email, login):
        self._send(
            RequestConstructor.create(
                request_type=RequestType.EMAIL_VERIFICATION,
                email=email,
                login=login
            ))
        return ResponseType(self.receive().type) == ResponseType.ACCEPT

    @Slot(str, str, result=bool)
    def codeVerification(self, email, code):
        self._send(
            RequestConstructor.create(
                request_type=RequestType.CODE_VERIFICATION,
                email=email,
                code=code
            ))
        return ResponseType(self.receive().type) == ResponseType.ACCEPT

    @Slot(int, result=float)
    def getUserOnlineStatus(self, user_id):
        self._send(
            RequestConstructor.create(
                request_type=RequestType.USER_STATUS,
                user_id=user_id
            )
        )
        response = self.receive()
        if response.data.is_online == True:
            return 0
        else:
            return response.data.last_seen

    @Slot(result=int)
    def getOnline(self):
        self._send(
            RequestConstructor.create(
                request_type=RequestType.STATS
            )
        )
        response = self.receive()
        self.__online = response.data.online if response is not None else 0
        self.__offline = response.data.offline if response is not None else 0
        return self.__online + 1 or 0

    @Slot(result=int)
    def getOffline(self):
        return self.__offline or 0

    def getUserInfo(self, user_id):
        self._send(
            RequestConstructor.create(
                request_type=RequestType.USER_INFO,
                user_id=user_id
            )
        )
        response = self.receive()
        return response.data

    @Slot(result=list)
    def updateContacts(self):
        contacts = sorted(MessageData.chat_users.values(), key=lambda item: item['message_id'] or 0)
        return [[c['contact_name'], c['contact_login'], c['contact_id']] for c in contacts]

    @Slot()
    def logout(self):
        UserData.clear()
        Storage.clear()
        self._send(RequestConstructor.create(
            request_type=RequestType.LOGOUT
        ))
        self.receive()

    @Slot(str, result=list)
    def search(self, keywords):
        response, keywords = [], keywords.split()
        if len(keywords) == 1:
            self._send(RequestConstructor.create(
                request_type=RequestType.SEARCH,
                keyword1=keywords[0]
            ))
            response = self.receive().data.users
        elif len(keywords) == 2:
            self._send(RequestConstructor.create(
                request_type=RequestType.SEARCH,
                keyword1=keywords[0],
                keyword2=keywords[1]
            ))
            response = self.receive().data.users
        return [[u['id'], u['login'], u['first_name'], u['last_name']] for u in response]

    def __update_authentication(self):
        if self.__auth_complete and not self.autoAuthentication():
            self.__server_error = True
            self.__server_message = 'Необходима повторная аутентификация!'

    @Slot(result=bool)
    def autoAuthentication(self):
        password = UserData.get_temporary_password()
        return self.authentication(
            login=UserData.get_my_login(),
            email=UserData.get_my_email(),
            password=Security.encrypt(password) if password else UserData.get_password(),
            save_password=True
        )

    @Slot(str, str, str, bool, result=bool)
    def authentication(self, login, email, password, save_password):
        if not Security.key_is_set() or not self._send(
                RequestConstructor.create(
                    request_type=RequestType.AUTHENTICATION,
                    login=login,
                    password=Security.encrypt(password) if isinstance(password, str) else password,
                    email=email
                )):
            return False
        response = self.receive()
        if ResponseType(response.type) == ResponseType.AUTH_COMPLETE:
            self.__auth_complete = True
            UserData.save_password_temporarty(password if isinstance(password, str) else '')
            UserData.save(
                my_id=response.data.user_id,
                first_name=response.data.first_name,
                last_name=response.data.last_name,
                login=response.data.login
            )
            if save_password:
                UserData.save(
                    password=Security.encrypt(password) if isinstance(password, str) else password,
                    email=email
                )
            MessageData.init(UserData.get_my_id())
            return True
        else:
            print("1")
            UserData.clear()
            return False

    @Slot(str, result=bool)
    def availableEmail(self, email):
        self._send(RequestConstructor.create(
            request_type=RequestType.AVAILABLE_EMAIL,
            email=email
        ))
        return ResponseType(self.receive().type) == ResponseType.ACCEPT

    @Slot(str, result=bool)
    def availableLogin(self, login):
        self._send(RequestConstructor.create(
            request_type=RequestType.AVAILABLE_LOGIN,
            login=login
        ))
        return ResponseType(self.receive().type) == ResponseType.ACCEPT

    @Slot(str, str, result=bool)
    def recoveryEmailVerification(self, email, login):
        self._send(RequestConstructor.create(
            request_type=RequestType.RECOVERY_EMAIl_VERIFICATION,
            login=login,
            email=email
        ))
        return ResponseType(self.receive().type) == ResponseType.ACCEPT

    @Slot(str, str, str, result=bool)
    def recoveryCodeVerification(self, email, login, code):
        self._send(RequestConstructor.create(
            request_type=RequestType.RECOVERY_CODE_VERIFICATION,
            login=login,
            email=email,
            code=code
        ))
        return ResponseType(self.receive().type) == ResponseType.ACCEPT

    @Slot(str, str, str, result=bool)
    def newPassword(self, email, login, password):
        if not Security.key_is_set() or not self._send(
                RequestConstructor.create(
                    request_type=RequestType.NEW_PASSWORD,
                    login=login,
                    email=email,
                    password=Security.encrypt(password)
                )): return False
        return ResponseType(self.receive().type) == ResponseType.ACCEPT

    def __encryption_key_verify(self):
        if not Security.key_is_set():
            return False

    def __get_encryption_key(self):
        answer = None
        try:
            self._send(RequestConstructor.create(request_type=RequestType.ENCRYPTION_KEY))
            answer = ResponseParser.extract_response(self._receive())
        except IOError:
            self.__set_server_message(answer)
            return None
        if ResponseType(answer.type) != ResponseType.KEY:
            raise TypeError("Ошибка при получении ключа шифрования!")
        self.__set_server_message(answer)
        return Security.update_encryption_key(new_key=answer.data.key)

    def receive(self):
        answer = None
        try:
            answer = ResponseParser.extract_response(self._receive())
        except IOError as err:
            pass
        finally:
            self.__set_server_message(answer)
            return answer

    def __set_server_message(self, answer):
        if answer is None or self._Network__alive == False:
            self.__server_message = 'Сервер не доступен!'
            self.__server_error = True
            return
        elif answer.type == ResponseType.ERROR:
            self.__server_error = True
        else:
            self.__server_error = False
        self.__server_message = answer.data.message

    def __get_server_message(self):
        msg = self.__server_message if self.__server_message else self.__default_server_message
        self.__server_message = None
        return msg
