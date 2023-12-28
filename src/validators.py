from wtforms.validators import ValidationError
from datetime import date

class NotInFuture(object):
    def __init__(self, message=None):
        if not message:
            message = 'Date must not be in the future.'
        self.message = message

    def __call__(self, form, field):
        if field.data > date.today():
            raise ValidationError(self.message)