import datetime

def numberOfYearsToCurrentYearCalculation(data, calculation_definition):
    reference_date_field = calculation_definition['referenceDate']
    referenceDate = data[reference_date_field]
    current_year = datetime.datetime.now().year
    return current_year - referenceDate.year

def numberOfDaysToCurrentDayCalculation(data, calculation_definition):
    reference_date_field = calculation_definition['referenceDate']
    referenceDate = data[reference_date_field]
    current_date = datetime.datetime.now().date()
    return (current_date - referenceDate).days