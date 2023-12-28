import json
import os
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired, Length
from datetime import datetime
from form_utilities import calculate_age
from populate_data import populate_data
from flask import Flask
from database import saveDataToDatabase

MAX_INPUT_LENGTH = 30

#initial commit

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'    
    return app

app = create_app()

class MyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=MAX_INPUT_LENGTH)])
    lastname = StringField('Surname', validators=[DataRequired(), Length(max=MAX_INPUT_LENGTH)])
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')
        
@app.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()
    age_years = age_days = None
    if form.validate_on_submit():
        
        # Calculated Fields
        age_years, age_days = calculate_age(form.dob.data)
        
        # Save Data in JSON
        data = populate_data(form, age_years, age_days)
        
        # Save Data in Database
        saveDataToJSONFile(data)
        
        # Save Data to Database
        saveDataToDatabase(data)
                     
    return render_template('index.html', form=form, age_years=age_years, age_days=age_days)

def saveDataToJSONFile(data):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    os.makedirs('data', exist_ok=True)
    with open(f'data/data_{timestamp}.json', 'w') as f:
        json.dump(data, f)    

if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
        
