from datetime import datetime


class Token:
    """
    This generate user tokens.
    """

    def __init__(self) -> None:
        pass

    def get(self, user_id: str, user_dob: str) -> str:
        """
        get() will return generated user token in string format.

        Args:
            user_id (str): User ID (NIC / Passport / Birth Certificate)
            user_dob (str): User's date of birth

        Returns:
            str: Generated token (Format -> NIC/PASSPORT + A/C (ADULT/CHILD))
        """

        try:
            this_year = datetime.today().year

            age_key = "A" if (int(this_year) - int(user_dob[0:4])) > 18 else "C"

            return f"{user_id}{age_key}"

        except Exception as e:

            print(f"\nAn Error occured : {e}\n")

            return False
