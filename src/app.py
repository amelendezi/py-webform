import json
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired, Length
from populate_data import populate, populate_calculation
from flask import Flask
from database import saveDataToDatabase

MAX_INPUT_LENGTH = 30

#initial commit

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'    
    return app

app = create_app()

class PersonForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=MAX_INPUT_LENGTH)])
    lastname = StringField('Surname', validators=[DataRequired(), Length(max=MAX_INPUT_LENGTH)])
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')
        
@app.route('/', methods=['GET', 'POST'])
def index():
    
    # Load table schema from JSON file
    with open('./src/definitions/person.json', 'r') as f:
        definition = json.load(f)
                
    form = PersonForm()
    
    data = {}
    if form.validate_on_submit():
                    
        # Populate Data                                     
        data  = populate(form, definition)
        
        #Populate Calculated Fields
        populate_calculation(data, definition)
        
        # Save Data to Database
        saveDataToDatabase(data, definition)
                     
    return render_template('index.html', form=form, age_years=data.get('age_years'), age_days=data.get('age_days'))

if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
        
