import calculations

def populate_data(form, age_years, age_days):
    return {
        'name': form.name.data,
        'lastname': form.lastname.data,
        'dob': form.dob.data.isoformat(),
        'age_years': age_years,
        'age_days': age_days,
    }
    
def populate(form, definition):
    data = {}
    for attr, details in definition['attributes'].items():
        if 'calculation' in details:
            continue
        
        value = getattr(form, attr).data
        data[attr] = value
    return data

def populate_calculation(data, definition):
    for attr, details in definition['attributes'].items():
        if 'calculation' not in details:
            continue

        calculation_name = details['calculation']['name']
        calculation_function = getattr(calculations, calculation_name, None)

        if calculation_function is None:
            raise ValueError(f"Unknown calculation: {calculation_name}")

        calculation_definition = details['calculation']
        data[attr] = calculation_function(data, calculation_definition)