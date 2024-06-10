from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired



def validate_size(form, field):
    if field.data == '':
        raise ValidationError('Please select a shirt size.')

class CheckoutForm(FlaskForm):
    shirt_size = SelectField('Shirt Size', choices=[
        ('', 'Select a size'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large')
    ], validators=[DataRequired(), validate_size])
    submit = SubmitField('Buy Now')