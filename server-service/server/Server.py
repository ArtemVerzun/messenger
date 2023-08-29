import asyncio
# import selectors
# import socket

from loguru import logger

from core.dispatcher.RequestManager import RequestManager
from statistics import Statistics


class Server:
    __buffer_size = 1024 * 5
    __address = None
    __port = None

    @classmethod
    async def handle(cls, reader, writer):
        ip, port = writer.get_extra_info('peername')
        await Statistics.connection(port=port)
        while True:
            try:
                data = await reader.read(cls.__buffer_size)
                if data:
                    request = data.decode('utf-8')
                    answer = await RequestManager.handle_request(
                        data=request,
                        ip=ip,
                        port=port
                    )
                    writer.write(answer)
                    await writer.drain()
                else:
                    writer.close()
                    break
            except ConnectionResetError:
                logger.warning("Принудительное закрытие соединения.")
                writer.close()
                break
        await Statistics.disconnection(port)

    @classmethod
    async def start(cls, port, address):
        cls.__port = port
        cls.__address = address
        await cls.main()

    @classmethod
    async def main(cls):
        server = await asyncio.start_server(cls.handle, cls.__address, cls.__port)

        async with server:
            logger.info(f"Начало работы сервера. Адрес: {cls.__address}. Порт: {cls.__port}")
            await server.serve_forever()

# class Server2:
#     __selector = None
#     __buffer_size = 1024 * 5
#
#     host = '127.0.0.1'
#     port = 6767
#
#     @classmethod
#     async def main(cls):
#         cls.__selector = selectors.DefaultSelector()
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         sock.bind((cls.host, cls.port))
#         sock.listen()
#         print('listening on', (cls.host, cls.port))
#         sock.setblocking(False)
#         cls.__selector.register(sock, selectors.EVENT_READ, cls.accept)
#         while True:
#             events = cls.__selector.select()
#             for key, mask in events:
#                 callback = key.data
#                 if key.data is not None:
#                     await callback(key.fileobj, mask)
#
#     @classmethod
#     async def start(cls):
#         await cls.main()
#
#     @classmethod
#     async def accept(cls, sock, mask):
#         conn, address = sock.accept()  # Should be ready
#         print('accepted', conn, 'from', address)
#         conn.setblocking(False)
#         cls.__selector.register(conn, selectors.EVENT_READ, cls.read)
#
#     @classmethod
#     async def read(cls, connection, mask):
#         try:
#             print("rec")
#             data = connection.recv(cls.__buffer_size)  # Should be ready
#             print(data)
#             if data:
#                 request = data.decode('utf-8')
#                 answer = await RequestManager.handle_request(request, '111.111.111.111')
#                 print("send")
#                 connection.send(answer)
#             else:
#                 cls.__selector.unregister(connection)
#                 connection.close()
#         except ConnectionResetError:
#             print('closing', connection)
#             cls.__selector.unregister(connection)
#             connection.close()
