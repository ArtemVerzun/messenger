import asyncio

import envfileparser

from loader import DatabaseLoader, MailLoader, LoggerLoader, CryptographerLoader, StatisticLoader
from server import Server


async def main():
    envs = envfileparser.get_env_from_file()
    LoggerLoader.start()
    CryptographerLoader.start()
    await DatabaseLoader.start()
    await MailLoader.start()
    await StatisticLoader.start()
    await Server.start(port=int(envs['SERVER_PORT']), address=envs['SERVER_HOST'])

asyncio.run(main())
