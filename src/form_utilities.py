from datetime import date

def calculate_age(born):
    today = date.today()
    years_difference = today.year - born.year
    is_before_birthday = (today.month, today.day) < (born.month, born.day)
    elapsed_years = years_difference - int(is_before_birthday)
    elapsed_days = (today - born.replace(year=today.year)).days
    return elapsed_years, elapsed_days