def populate_data(form, age_years, age_days):
    return {
        'name': form.name.data,
        'lastname': form.lastname.data,
        'dob': form.dob.data.isoformat(),
        'age_years': age_years,
        'age_days': age_days,
    }