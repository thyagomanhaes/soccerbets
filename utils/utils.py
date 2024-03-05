from datetime import datetime


def convert_to_datetime(date, time):
    convert_month = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }

    date_parts = date.split()

    day = date_parts[1]
    day = int(day[:-2])
    month = date_parts[2]
    year = int(date_parts[3])

    month_number = convert_month.get(month)

    hour = int(time.split(':')[0])
    minute = int(time.split(':')[1])

    match_date = datetime(year, month_number, day, hour, minute, 0)

    return match_date
