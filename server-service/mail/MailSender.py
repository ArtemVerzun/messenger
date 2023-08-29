from logging import getLogger

import googleapiclient.errors
from loguru import logger

from .MailService import MailService
from .MailBuilder import MailBuilder


class MailSender:
    service: MailService
    INSTANCE = False

    @logger.catch
    def __init__(self):
        self.service = MailService()

    @classmethod
    @logger.catch
    def create(cls):
        if cls.INSTANCE:
            raise Exception('Singleton mail core!')
        cls.INSTANCE = True
        return MailSender()

    async def send(self, destination, subject, body):
        try:
            self.service.service.users().messages().send(
                userId="me",
                body=MailBuilder.create(destination, subject, body, '')
            ).execute()
        except googleapiclient.errors.HttpError as e:
            error_message = f"Не удалось отпраить электронное сообщение по адресу {destination}"
            # raise ValueError(error_message)
            getLogger().exception(str(e), exc_info=e)
