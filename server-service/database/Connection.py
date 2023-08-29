import asyncpg


class Connection:
    __pool: asyncpg.pool = None

    @classmethod
    async def create(cls, user, password, database, host):
        if cls.__pool is not None:
            cls.__pool.terminate()
        try:
            cls.__pool = await asyncpg.create_pool(
                min_size=10,
                max_size=10,
                user=user,
                password=password,
                database=database,
                host=host
            )
        except asyncpg.exceptions.InvalidPasswordError as e:
            print(f"{str(e).capitalize()}.")

        return cls.__pool

    @classmethod
    async def close(cls):
        await cls.__pool.terminate()
