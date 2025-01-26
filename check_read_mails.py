import os

from dotenv import load_dotenv
from loguru import logger
import chardet

from modules.email_handler import EmailHandler


def main():
    # Создаем экземпляры обработчиков
    load_dotenv()

    email_handler = EmailHandler(
        server=os.environ.get('exchange_server'),
        username=os.environ.get('exchange_username'),
        password=os.environ.get('exchange_password'),
        primary_smtp_address=os.environ.get('primary_smtp_address'),

    )

    emails = email_handler.get_all_mails()

    for email in emails:
        # if chardet.detect(email.body.encode())['encoding'] != 'utf-8':
        logger.info(f"Получено письмо от:\n"
                    f"{email.sender.email_address}\n{email.subject}\n{email.datetime_received}\n{chardet.detect(email.body.encode())['encoding']}")


if __name__ == '__main__':
    main()
