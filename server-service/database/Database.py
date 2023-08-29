import asyncpg
from loguru import logger


class Database:
    __connection_pool: asyncpg.pool
    REGISTRATION_QUERY = 'INSERT INTO users(login, email, first_name, last_name, password_hash) ' \
                         'VALUES ($1, $2, $3, $4, $5)'
    LOGIN_QUERY = 'SELECT login FROM users WHERE login = $1'
    EMAIL_QUERY = 'SELECT email FROM users WHERE email = $1'

    COUNT_ALL_QUERY = 'SELECT COUNT(1) FROM users'
    USER_ID_BY_LOGIN_QUERY = 'SELECT id FROM users WHERE login = $1'
    USER_ID_BY_EMAIL_QUERY = 'SELECT id FROM users WHERE email = $1'
    USER_FIRST_NAME_QUERY = 'SELECT first_name FROM users WHERE  id = $1'
    USER_LAST_NAME_QUERY = 'SELECT last_name FROM users WHERE  id = $1'

    SEARCH_QUERY_BY_FIRST_LAST_NAME = 'SELECT id, login, first_name, last_name FROM users ' \
                                      'WHERE (lower(first_name) LIKE $1 ' \
                                      'AND lower(last_name) LIKE $2) OR ' \
                                      '(lower(first_name) LIKE $2 AND lower(last_name) LIKE $1)'
    SEARCH_QUERY = 'SELECT id, login, first_name, last_name FROM users ' \
                   'WHERE lower(login) LIKE $1 OR lower(first_name) LIKE $1 OR lower(last_name) LIKE $1'

    @classmethod
    @logger.catch
    async def get_user_first_name(cls, user_id):
        async with cls.__connection_pool.acquire() as connection:
            result = await connection.fetch(cls.USER_FIRST_NAME_QUERY, user_id)
            return result[0][0]

    @classmethod
    @logger.catch
    async def get_user_last_name(cls, user_id):
        async with cls.__connection_pool.acquire() as connection:
            result = await connection.fetch(cls.USER_LAST_NAME_QUERY, user_id)
            return result[0][0]

    @classmethod
    @logger.catch
    async def get_user_id_by_login(cls, login):
        async with cls.__connection_pool.acquire() as connection:
            result = await connection.fetch(cls.USER_ID_BY_LOGIN_QUERY, login)
            return result[0][0]

    @classmethod
    @logger.catch
    async def get_user_id_by_email(cls, email):
        async with cls.__connection_pool.acquire() as connection:
            result = await connection.fetch(cls.USER_ID_BY_EMAIL_QUERY, email)
            return result[0][0]

    @classmethod
    @logger.catch
    async def get_count(cls):
        async with cls.__connection_pool.acquire() as connection:
            result = await connection.fetch(cls.COUNT_ALL_QUERY)
            return result[0][0]

    @classmethod
    @logger.catch
    async def connect(cls, connection: asyncpg.Connection):
        cls.__connection_pool = connection

    @classmethod
    @logger.catch
    async def update_password(cls, login, password):
        try:
            async with cls.__connection_pool.acquire() as connection:
                await connection.fetch('UPDATE users SET password_hash = $1 WHERE login = $2', password, login)
                return True
        except Exception:
            return False

    @classmethod
    @logger.catch
    async def get_email(cls, login):
        async with cls.__connection_pool.acquire() as connection:
            result = await connection.fetch('SELECT email FROM users WHERE login = $1', login)
            return result[0][0]

    @classmethod
    @logger.catch
    async def get_login(cls, email):
        async with cls.__connection_pool.acquire() as connection:
            result = await connection.fetch('SELECT login FROM users WHERE email = $1', email)
            return result[0][0]

    @classmethod
    @logger.catch
    async def get_password(cls, email, login):
        async with cls.__connection_pool.acquire() as connection:
            if email:
                result = await connection.fetch('SELECT password_hash FROM users WHERE email = $1', email)
            else:
                result = await connection.fetch('SELECT password_hash FROM users WHERE login = $1', login)
            return result[0][0]

    @classmethod
    @logger.catch
    async def exists_email(cls, email):
        async with cls.__connection_pool.acquire() as connection:
            result = await connection.fetch(cls.EMAIL_QUERY, email)
            if len(result) == 0:
                return False
            return True

    @classmethod
    @logger.catch
    async def exists_login(cls, login):
        async with cls.__connection_pool.acquire() as connection:
            result = await connection.fetch(cls.LOGIN_QUERY, login)
            if len(result) == 0:
                return False
            return True

    @classmethod
    @logger.catch
    async def registration(cls, login, password, first_name, last_name, email):
        async with cls.__connection_pool.acquire() as connection:
            try:
                await connection.fetch(
                    cls.REGISTRATION_QUERY,
                    login, email, first_name, last_name, password
                )
                return True
            except asyncpg.exceptions.CheckViolationError as e:
                logger.exception(e)
            except asyncpg.exceptions.UndefinedColumnError as e:
                logger.exception(e)
            except asyncpg.exceptions.UniqueViolationError as e:
                logger.exception(e)
            return False

    @classmethod
    @logger.catch
    async def get_user_info(cls, user_id):
        async with cls.__connection_pool.acquire() as connection:
            result = await connection.fetch('SELECT login, first_name, last_name FROM users WHERE id = $1', user_id)
            return result[0]

    @classmethod
    @logger.catch
    async def search_users(cls, keyword1, keyword2=None):
        async with cls.__connection_pool.acquire() as connection:
            if not keyword2:
                result = await connection.fetch(cls.SEARCH_QUERY, keyword1.lower() + '%')
            else:
                result = await connection.fetch(
                    cls.SEARCH_QUERY_BY_FIRST_LAST_NAME,
                    keyword1.lower() + '%',
                    keyword2.lower() + '%'
                )
            return [dict(r) for r in result]
