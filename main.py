import os
import time

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from loguru import logger

from config import CHECK_INTERVAL, DOWNLOAD_DIR
from modules.email_handler import EmailHandler
from modules.file_processor import FileProcessor
from modules.ftp_uploader import FTPUploader
from modules.text_processor import TextProcessor


def main():
    # Создаем экземпляры обработчиков
    load_dotenv()


    email_handler = EmailHandler(
        server=os.environ.get('exchange_server'),
        username=os.environ.get('exchange_username'),
        password=os.environ.get('exchange_password'),
        primary_smtp_address=os.environ.get('primary_smtp_address'),

    )
    file_processor = FileProcessor()
    text_processor = TextProcessor()
    ftp_uploader = FTPUploader(
        host=os.environ.get('ftp_host'),
        username=os.environ.get('FTP_LOGIN'),
        password=os.environ.get('FTP_PASS'),
        port=int(os.environ.get('ftp_port', 21))
    )

    print("Запуск программы для обработки писем...")

    emails = email_handler.check_mailbox()

    for email in emails:
        logger.info(f"Получено письмо от: {email.sender.email_address}")
        logger.info(f"Тема: {email.subject}")


        # Скачиваем вложения
        attachments = email_handler.download_attachments(email, DOWNLOAD_DIR)
        print(f"Скачаны файлы: {attachments}")

        # извлекаю текст из html письма
        soup = BeautifulSoup(email.body, 'html.parser')
        email_text =  soup.get_text().strip()

        # Извлекаем текст письма и обрабатываем
        clean_text = text_processor.extract_clean_text(email_text)
        # print(f'{clean_text = }')

        for file in attachments:
            logger.info(f'{file = }')
            # Проверяем, является ли файл изображением
            if not file_processor.is_image(file):
                print(f"Пропущен файл: {file} (не является изображением)")
                continue

            #Конвертируем файл в JPEG, если это необходимо
            processed_file = file_processor.convert_to_jpeg(file)

            # Добавляем XMP-метаданные
            file_processor.add_xmp_metadata(processed_file, clean_text)

            # Загружаем файл на FTP
            ftp_uploader.connect()
            ftp_uploader.upload_files([processed_file], remote_dir="/PHOTO/INBOX/SHOOTS/BEZ_AVTORA/KSP_018175")

        # Отмечаем письмо как прочитанное
        email_handler.mark_as_read(email)

    # print(f"Ожидание {CHECK_INTERVAL} секунд до следующей проверки...")
    # logger.info(f'{count = }')
    logger.info(time.strftime("%H:%M:%S", time.localtime()))
        # time.sleep(CHECK_INTERVAL)
        # count += 1



if __name__ == "__main__":
    main()