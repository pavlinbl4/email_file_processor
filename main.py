import time
from config import CHECK_INTERVAL, DOWNLOAD_DIR
from modules.email_handler import EmailHandler
from modules.file_processor import FileProcessor
from modules.text_processor import TextProcessor
# from modules.ftp_uploader import FTPUploader
from dotenv import load_dotenv
import os
from loguru import logger
from bs4 import BeautifulSoup



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
    # ftp_uploader = FTPUploader()

    print("Запуск программы для обработки писем...")
    count = 0
    while True:
        # Получаем письма
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
                # ftp_uploader.upload_files([processed_file], destination='/uploads/')

            # Отмечаем письмо как прочитанное
            email_handler.mark_as_read(email)

        print(f"Ожидание {CHECK_INTERVAL} секунд до следующей проверки...")
        logger.info(f'{count = }')
        logger.info(time.strftime("%H:%M:%S", time.localtime()))
        time.sleep(CHECK_INTERVAL)
        count += 1



if __name__ == "__main__":
    main()