from ftplib import FTP
import os


class FTPUploader:
    """
    Класс для загрузки файлов на FTP-сервер и удаления локальных файлов после успешной загрузки.
    """
    def __init__(self, host, username, password, port=21):
        """
        Инициализация подключения к FTP-серверу.
        :param host: Адрес FTP-сервера.
        :param username: Имя пользователя для авторизации.
        :param password: Пароль пользователя.
        :param port: Порт сервера (по умолчанию 21).
        """
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.ftp = FTP()

    def connect(self):
        """
        Подключается к FTP-серверу.
        """
        try:
            print(f"Подключение к FTP-серверу {self.host}:{self.port}...")
            self.ftp.connect(self.host, self.port)
            self.ftp.login(self.username, self.password)
            print(f"Успешное подключение к {self.host}")
        except Exception as e:
            raise ConnectionError(f"Ошибка подключения к FTP-серверу: {e}")

    def upload_file(self, file_path, remote_dir="/"):
        """
        Загружает файл на FTP-сервер.
        :param file_path: Локальный путь к файлу.
        :param remote_dir: Удаленный каталог на сервере.
        """
        try:
            self.ftp.cwd(remote_dir)  # Переход в нужный каталог на сервере
        except Exception:
            raise FileNotFoundError(f"Удаленный каталог {remote_dir} не найден.")

        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as file:
            print(f"Загрузка файла {file_name} в каталог {remote_dir}...")
            self.ftp.storbinary(f"STOR {file_name}", file)
            print(f"Файл {file_name} успешно загружен.")

    def upload_files(self, file_paths, remote_dir="/"):
        """
        Загружает список файлов на FTP-сервер и удаляет их локально после успешной передачи.
        :param file_paths: Список локальных путей к файлам.
        :param remote_dir: Удаленный каталог на сервере.
        """
        for file_path in file_paths:
            try:
                self.upload_file(file_path, remote_dir)
                os.remove(file_path)  # Удаляем файл после успешной загрузки
                print(f"Локальный файл {file_path} удален.")
            except Exception as e:
                print(f"Ошибка при загрузке файла {file_path}: {e}")

    def disconnect(self):
        """
        Отключается от FTP-сервера.
        """
        try:
            self.ftp.quit()
            print("Отключение от FTP-сервера.")
        except Exception as e:
            print(f"Ошибка при отключении от FTP-сервера: {e}")


# Пример использования
if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    ftp_uploader = FTPUploader(
        host=os.environ.get('ftp_host'),
        username=os.environ.get('FTP_LOGIN'),
        password=os.environ.get('FTP_PASS'),
        port=int(os.environ.get('ftp_port', 21))
    )

    try:
        ftp_uploader.connect()
        test_files = [
            "/Users/evgeniy/Downloads/KSP_018174_01733_1h.jpg",  # Замените на пути к вашим тестовым файлам
            # "example2.jpeg"
        ]
        ftp_uploader.upload_files(test_files, remote_dir="/PHOTO/INBOX/SHOOTS/BEZ_AVTORA/KSP_018175")
    finally:
        ftp_uploader.disconnect()