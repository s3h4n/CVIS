from flask import request


class FormReceiver:
    """
    This will get data from the frontend.
    """

    def __init__(self) -> None:
        pass

    def get_data(self, field_names: list) -> dict or bool:
        """
        get_data() can get data from html forms and return it.

        Args:
            field_names (list): Values of name attribute of html form elements.

        Returns:
            dict or int: If there are no errors, form data will return as python
                         dictionary (key => value). Errors will return False.
        """

        data = {}

        try:
            for field in field_names:
                data[field] = request.form[field]

            return data

        except Exception as e:
            print(f"An Error occured : {e}")

            return False

    def get_files(self, field_names: list) -> dict or bool:
        """
        get_files() can get giles from html forms and return it.

        Args:
            field_names (list): Values of name attribute of html form file elements.

        Returns:
            dict or int: If there are no errors, form data will return as python
                        dictionary (key => value). Errors will return False.
        """

        data = {}

        try:
            for field in field_names:
                data[field] = request.files[field]

            return data

        except Exception as e:
            print(f"An Error occured : {e}")

            return False
