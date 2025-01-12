from pathlib import Path


def files_in_folder(path_to_folder: str, ):
    my_path = Path(path_to_folder)
    only_image_files = (
            list(my_path.rglob("*.jpg"))
            + list(my_path.rglob("*.jpeg"))
            + list(my_path.rglob("*.png"))
            + list(my_path.rglob("*.gif")))
    print(only_image_files)


if __name__ == '__main__':
    files_in_folder('/Users/evgeniy/Pictures')
