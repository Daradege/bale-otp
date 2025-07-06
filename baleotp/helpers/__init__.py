from ..exceptions import PhoneFormatError

def transform_number(phone_number:str) -> str:
    if phone_number.startswith("98") and len(phone_number) == 12:
        return phone_number
    elif phone_number.startswith("0") and len(phone_number) == 11:
        return "98"+phone_number[1:]
    elif phone_number.startswith("9") and len(phone_number) == 10:
        return "98"+phone_number
    elif phone_number.startswith("+") and len(phone_number) == 13:
        return phone_number[1:]
    raise PhoneFormatError("The phone number is not in correct format")