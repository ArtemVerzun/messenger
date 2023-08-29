import envfileparser
import psycopg2
from psycopg2 import Error


class Connection:
    __connection = None

    def __init__(self):
        envs = envfileparser.get_env_from_file()
        try:
            self.__connection = psycopg2.connect(
                user=envs['DB_USER'],
                password=envs['DB_PASSWORD'],
                host=envs['DB_HOST'],
                port=envs['DB_PORT'],
                database=envs['DB_NAME']
            )

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)

    def get_connection(self):
        return self.__connection


class Storage:
    __message_index = None

    def __init__(self):
        self.__connection = Connection().get_connection()
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute("select max(index) from messages")
        _index = self.__cursor.fetchone()[0]
        self.__message_index = _index + 1 if _index else 0
        self.__connection.commit()

    def save_message(self, from_id: int, to_id: int, date_time: float, message: str) -> int:
        self.__message_index += 1
        self.__cursor.execute("INSERT INTO messages(index, id_from, id_to, date_time, message)"
                              "VALUES (%s, %s, %s, %s, %s)",
                              (self.__message_index, from_id, to_id, date_time, message)
                              )
        self.__connection.commit()
        return self.__message_index

    def get_messages(self, target_id, last_message_id):
        self.__cursor.execute(
            "SELECT index, id_from, id_to, message, date_time FROM messages "
            "WHERE index > %s and (id_from = %s OR id_to = %s)",
            (last_message_id or 0, target_id, target_id)
        )
        return [(msg[0], msg[1], msg[2], msg[3], float(msg[4])) for msg in self.__cursor.fetchall()]

    def delete_dialog(self, user1_id, user2_id):
        self.__cursor.execute(
            """
            DELETE FROM messages 
            WHERE (id_from = %s AND id_to = %s) 
            OR (id_from = %s AND id_to = %s)
            """,
            (user1_id, user2_id, user2_id, user1_id)
        )
        self.__connection.commit()

    def delete_message(self, message_id):
        self.__cursor.execute(
            """
            DELETE FROM messages 
            WHERE index = %s
            """,
            (message_id,)
        )
        self.__connection.commit()
