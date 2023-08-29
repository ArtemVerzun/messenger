import selectors
import socket
from Dispatcher import Dispatcher
from Clients import Clients


class Server:
    __selector = selectors.DefaultSelector()
    __BUFFER_SIZE = 1024 * 100
    __BACKLOG = 100
    __PORT = None
    __ADDRESS = None

    @classmethod
    def __init(cls):
        sock = socket.socket()
        sock.bind((cls.__ADDRESS, cls.__PORT))
        sock.listen(cls.__BACKLOG)
        sock.setblocking(False) # Включаем неблокирующий режим
        cls.__selector.register(sock, selectors.EVENT_READ, cls.accept)  # Регистрация клиента для прослуш событий

    @classmethod
    def start(cls, port, address):
        cls.__PORT, cls.__ADDRESS = port, address
        cls.__init()
        print(f'Starting server on port {cls.__PORT} and address {cls.__ADDRESS}')
        while True:
            events = cls.__selector.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

    @classmethod
    def accept(cls, sock, mask):
        connection, addr = sock.accept()  # Should be ready
        Clients.set_connection(connection, connection.fileno())  # save client socket
        connection.setblocking(False)
        cls.__selector.register(connection, selectors.EVENT_READ, cls.read)

    @classmethod
    def read(cls, connection, mask):
        try:
            data = connection.recv(cls.__BUFFER_SIZE)  # Should be ready
            if data:
                receivers, answer_data = Dispatcher.handle(data, connection.fileno())
                for r in receivers:
                    for user_fd in Clients.get_user(r):
                        try:
                            Clients.connections[user_fd][Clients.CONNECTION].sendall(answer_data)
                        except KeyError:
                            Clients.remove_connection(user_fd)
            else:
                cls.close(connection)
        except OSError as err:
            print(err)
            cls.close(connection)

    @classmethod
    def close(cls, connection):
        Clients.remove_connection(connection.fileno())
        connection.close()
        cls.__selector.unregister(connection)
