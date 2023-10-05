from werkzeug.utils import secure_filename
import sqlite3
import json
import os


class DatabaseHelper:
    """
    This help to manage databases.
    """

    def __init__(self) -> None:
        pass

    def save_image(self, main_dir: str, user_token: str, images: dict) -> bool:
        """
        save_image() will save given images to given path.

        Args:
            main_dir (str): Main directory
            user_token (str): Sub directory (image directory)
            images (dict): Set of images

        Returns:
            bool:  Return code (False -> Failed, True -> Success)
        """
        try:
            os.mkdir(f"{main_dir}/{user_token}")

            for img in images:
                img_name, img_ext = os.path.splitext(
                    secure_filename(images[img].filename)
                )

                images[img].filename = f"{img}{img_ext}"

                location = os.path.join(main_dir, user_token, images[img].filename)

                images[img].save(location)

            return True  # Success

        except Exception as e:
            print(f"An Error occured : {e}")

            return False  # Failure
