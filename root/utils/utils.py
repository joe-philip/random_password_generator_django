from datetime import date


def success(data) -> dict:
    response = {
        'status': True,
        'message': 'success'
    }
    if data is not None:
        response['data'] = data
    return response


def get_age(dob: date) -> int:
    today = date.today()
    present_birthday = date(today.year, dob.month, dob.day)
    age = present_birthday.year - dob.year
    age = age if present_birthday <= today else age - 1
    return age
