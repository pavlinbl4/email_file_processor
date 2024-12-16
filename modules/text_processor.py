import re
from loguru import logger


class TextProcessor:
    """
    Модуль для обработки текста писем. Удаляет приветствия, подписи и прочий ненужный текст.
    """

    # Предопределенные шаблоны для поиска приветствий и подписей
    GREETINGS = [
        r"^Добр.+\s.*$",  # Пример: Dear John
        # r"^Коллеги, доброе утро!",  # Пример: Hello,
        # r"^Доброе ",  # Пример: Hi,
        # r"^Добрый вечер. Просьба добавить в базу",  # Пример: Greetings,
        # r"^Здравствуйте,",  # Пример: Здравствуйте,
        # r"^Добрый день,",  # Пример: Добрый день,
        # r"^Привет,",  # Пример: Привет,
        r"Коллеги,+\s.*$",  # Пример: Коллеги,
    ]

    SIGNATURES = [
        r"Best\sregards,",  # Пример: Best regards,
        r"Kind\sregards,",  # Пример: Kind regards,
        r"Yours\sfaithfully,",  # Пример: Yours faithfully,
        r"С уважением,",  # Пример: С уважением,
        r"С наилучшими пожеланиями,",  # Пример: С наилучшими пожеланиями,
        r"--\n",  # Пример: текст после "---"
    ]

    def __init__(self):
        """
        Инициализация модуля.
        """
        self.greetings_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.GREETINGS]
        self.signatures_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.SIGNATURES]

    def extract_clean_text(self, email_text):
        """
        Извлекает содержательный текст из тела письма, удаляя приветствия и подписи.
        :param email_body: Текст письма.
        :return: Очищенный текст письма.
        """


        if not email_text:
            return ""

        # Разделяем текст построчно
        lines = email_text.splitlines()
        cleaned_lines = []
        # logger.info(cleaned_lines[0])

        # Удаляем приветствие (первые строки письма)
        greeting_removed = False
        for line in lines:
            if not greeting_removed:
                # Проверяем, является ли строка приветствием
                if any(pattern.match(line.strip()) for pattern in self.greetings_patterns):
                    greeting_removed = True
                    continue
            cleaned_lines.append(line)

        # Удаляем подпись (конец письма)
        cleaned_text = "\n".join(cleaned_lines)
        for pattern in self.signatures_patterns:
            cleaned_text = re.split(pattern, cleaned_text, maxsplit=1)[0]

        # Очищаем лишние пробелы и переносы строк
        cleaned_text = cleaned_text.strip()

        return cleaned_text


# Пример использования
if __name__ == "__main__":
    email_text = """

 
Доброе солнечное утро, коллеги! Добавьте, пожалуйста, порцию Беглова в наш архив



Фото: пресс-служба Администрации губернатора Санкт-Петербурга
 
Подписать можно: Прямая линия с губернатором Санкт-Петербурга Александром Бегловым
 
С уважением,
Аня
    """

    processor = TextProcessor()
    clean_text = processor.extract_clean_text(email_text)
    print("Очищенный текст:")
    print(clean_text)