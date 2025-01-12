from pathlib import Path


class FilesInFolder():

    @staticmethod
    def files_in_folder(path_to_folder: str):
        my_path = Path(path_to_folder)

        if not my_path.is_dir():
            raise ValueError(f"Path {path_to_folder} is not a valid directory.")

        extensions = ['.jpg', '.png', '.tif', '.jpeg', '.tiff']
        image_files = [f for f in my_path.glob("*") if f.suffix.lower() in extensions]

        return image_files


if __name__ == '__main__':

    processor = FilesInFolder()
    _image_files = processor.files_in_folder('/Users/evgeniy/Pictures')
    for file in _image_files:
        print(file)
