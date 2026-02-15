from phonenumber_field.phonenumber import phonenumbers
from typing import Union


def parse_phone(number_str: str, country: str) -> Union[str, None]:
    try:
        number = phonenumbers.parse(number_str, country)
        if phonenumbers.is_valid_number(number):
            foo = phonenumbers.format_number(
                number,
                phonenumbers.PhoneNumberFormat.E164
            )
            return foo
    except phonenumbers.NumberParseException:
        return None
