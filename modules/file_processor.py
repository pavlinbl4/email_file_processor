import os
from venv import logger

import exiftool
from PIL import Image


class FileProcessor:
    """
    Модуль для обработки файлов. Проверяет тип файлов, конвертирует в JPEG и добавляет метаданные.
    """

    def __init__(self):
        pass

    @staticmethod
    def is_image(file_path):
        """
        Проверяет, является ли файл изображением.
        :param file_path: Путь к файлу.
        :return: True, если файл является изображением, иначе False.
        """
        try:
            with Image.open(file_path) as img:
                img.verify()  # Проверяем, является ли файл корректным изображением
            return True
        except (IOError, SyntaxError):
            return False

    @staticmethod
    def convert_to_jpeg(file_path):
        """
        Конвертирует файл в формат JPEG, если это необходимо.
        :param file_path: Путь к файлу.
        :return: Путь к файлу в формате JPEG.
        """
        base_name, ext = os.path.splitext(file_path)
        jpeg_file_path = f"{base_name}.jpg"

        if ext.lower() in ['.jpg', '.jpeg']:
            # Файл уже в формате JPEG, ничего не делаем
            return file_path

        try:
            with Image.open(file_path) as img:
                rgb_image = img.convert('RGB')  # Конвертируем в RGB для совместимости
                rgb_image.save(jpeg_file_path, 'JPEG')
                logger.info(f"Файл {file_path} конвертирован в JPEG: {jpeg_file_path}")
            return jpeg_file_path
        except Exception as e:
            logger.error(f"Ошибка при конвертации файла {file_path}: {e}")
            return None

    @staticmethod
    def add_xmp_metadata(file_path, caption):
        """
        Добавляет XMP-метаданные в изображение.
        :param file_path: Путь к файлу.
        :param metadata: Словарь с метаданными для добавления.
        """
        try:

            with exiftool.ExifTool() as et:
                et.execute(
                    '-XMP:Label= Purple',
                    f'-XMP:Description = {caption}'.encode("utf-8"),
                    '-overwrite_original',
                    file_path.encode('utf-8')

                )

            logger.info(f"Добавлены метаданные в файл {file_path}: {caption}")
        except Exception as e:
            logger.error(f"Ошибка при добавлении метаданных в файл {file_path}: {e}")


# Пример использования
if __name__ == "__main__":
    processor = FileProcessor()

    test_file = "/Users/evgeniy/PycharmProjects/email_file_processor/downloads/20241130_pavl_IMG_1126.jpeg"  # Укажите путь к тестовому изображению
    if processor.is_image(test_file):
        print(f"{test_file} — это изображение.")

        # Конвертация в JPEG
        jpeg_file = processor.convert_to_jpeg(test_file)

        # Добавление метаданных
        if jpeg_file:
            caption = "Lazy dog"
            processor.add_xmp_metadata(jpeg_file, caption)
    else:
        print(f"{test_file} — это не изображение.")
