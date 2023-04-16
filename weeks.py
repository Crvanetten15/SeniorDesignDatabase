import datetime

def get_week_number(date_str):
    # Convert date string to datetime object
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

    # Get the ISO week number of the date
    iso_year, iso_week_num, iso_day = date.isocalendar()

    # If the ISO week number is 53, check if the date is part of the previous year's last week
    if iso_week_num == 53:
        prev_year_last_week = datetime.date(date.year - 1, 12, 28).isocalendar()[1]
        if prev_year_last_week == 53:
            iso_week_num = 1

    return iso_week_num

# date_str = '2023-06-29'
# week_num = get_week_number(date_str)
# print(f"The week number of {date_str} is {week_num}.")