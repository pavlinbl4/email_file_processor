# pip install exchangelib

import os

from dotenv import load_dotenv
from exchangelib import Credentials, Account, DELEGATE, Configuration
from exchangelib.errors import ErrorNonExistentMailbox
from loguru import logger


class EmailHandler:
    def __init__(self, server: str, username: str, password: str, primary_smtp_address: str) -> None:
        """
        Инициализация обработчика почты.
        """
        self.server = server
        self.primary_smtp_address = primary_smtp_address
        self.credentials = Credentials(username, password)

        self.config = Configuration(
            server=os.environ.get('exchange_server'),
            credentials=self.credentials
        )

        try:
            self.account = Account(
                primary_smtp_address=self.primary_smtp_address,
                credentials=self.credentials,
                autodiscover=False,
                access_type=DELEGATE,
                config=self.config
            )

        except ErrorNonExistentMailbox:
            raise ValueError("Не удалось подключиться к серверу. Проверьте учетные данные.")

    def check_mailbox(self, from_addresses=None):
        """
        Проверяет входящие письма в папке "Входящие".
        :param from_addresses: Список email-адресов отправителей для фильтрации (может быть пустым).
        :return: Список писем (объектов Message), соответствующих критериям.
        """
        inbox = self.account.inbox
        unread_emails = inbox.filter(is_read=False)

        if from_addresses:
            # Фильтруем письма по списку отправителей
            unread_emails = unread_emails.filter(sender__in=from_addresses)

        return unread_emails

    @staticmethod
    def download_attachments(email, download_dir):
        try:
            os.makedirs(download_dir, exist_ok=True)
            saved_files = []

            for attachment in email.attachments:
                if hasattr(attachment, 'content') and attachment.content:
                    file_path = os.path.join(download_dir, attachment.name)
                    with open(file_path, 'wb') as f:
                        f.write(attachment.content)
                    saved_files.append(file_path)
                else:
                    print(f"Ошибка: Вложение {attachment.name} не содержит контента.")

            return saved_files
        except Exception as e:
            print(f"Ошибка при скачивании вложений: {e}")
            return []

    @staticmethod
    def mark_as_read(email):
        """
        Отмечает письмо как прочитанное.
        """
        email.is_read = True
        email.save()


# Пример использования
# if __name__ == "__main__":
#     from config import DOWNLOAD_DIR
#     logger.info(DOWNLOAD_DIR)
#     load_dotenv()
#
#     email_handler = EmailHandler(
#         server=os.environ.get('exchange_server'),
#         username=os.environ.get('exchange_username'),
#         password=os.environ.get('exchange_password'),
#         primary_smtp_address=os.environ.get('primary_smtp_address'),
#
#     )
#
#     print("Проверяем почтовый ящик...")
#     # emails = email_handler.check_mailbox(from_addresses=["specific.sender@example.com"])
#     emails = email_handler.check_mailbox()
#
#     for email in emails:
#         print(f"Получено письмо от: {email.sender}")
#         print(f"Тема: {email.subject}")
#         print(f"Текст: {email.text_body}")
#
#         # Скачиваем вложения
#         attachments = email_handler.download_attachments(email, DOWNLOAD_DIR)
#         print(f"Скачаны файлы: {attachments}")
#
#         # Отмечаем письмо как прочитанное
#         # email_handler.mark_as_read(email)


