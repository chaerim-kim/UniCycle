from flask_wtf import Form
from wtforms import TextField, RadioField, IntegerField, TimeField, SelectField, PasswordField, BooleanField, DecimalField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired

class CardDetailForm(Form):
    CardHolderName = TextField('cardname', validators=[DataRequired()])
    CardNumber = IntegerField('cardnumber', validators=[DataRequired()])
    CardCVV = TextField('cardcvv', validators=[DataRequired()])
    CardExpireDate = DateField('cardexpiredate', validators=[DataRequired()])
    CardType = RadioField('cardtype', choices=[('1','Mastercard'),('2','VISA')], validators=[DataRequired()])
    SaveCard = BooleanField('Save Card Details')

    CustomerFirstName = TextField('customerfirstname', validators=[DataRequired()])
    CustomerLastName = TextField('customerlastname', validators=[DataRequired()])
    CustomerEmail = TextField('customeremail', validators=[DataRequired()])
    CustomerAddress1 = TextField('customeraddress1', validators=[DataRequired()])
    CustomerAddress2 = TextField('customeraddress2')
    CustomerCity = TextField('customercity')
    CustomerPostcode = TextField('customerpostcode', validators=[DataRequired()])

class TimeSelect(Form):
    Date = DateField('date', validators=[DataRequired()])
    HirePeriod = SelectField('days',choices=[('1', '1 day'), ('2', '2 days'), ('3', '3 days'), ('4', '4 days'), ('5', '5 days'), ('6', '6  days'), ('7', '7  days')])


class BikeIsFree(Form):
    Location = SelectField('location', choices=[('1', 'University'), ('2', 'City'), ('3', 'Headingley')])
    Date = DateField('date', validators=[DataRequired()])
    HirePeriod = SelectField('days',choices=[('1', '1 day'), ('2', '2 days'), ('3', '3 days'), ('4', '4 days'), ('5', '5 days'), ('6', '6  days'), ('7', '7  days')])

class Login(Form):
    EmailAddress = TextField('username', validators=[DataRequired()])
    Password = PasswordField('loginpassword', validators=[DataRequired()])

class CreateAccount(Form):
    Title = SelectField('title',choices=[('mr','Mr'), ('mrs','Mrs'), ('miss','Miss'), ('ms','Ms')])
    FirstName = TextField('firstname', validators=[DataRequired()])
    Surname = TextField('surname', validators=[DataRequired()])
    EmailAddress = TextField('email', validators=[DataRequired()])
    Password = PasswordField('newpassword', validators=[DataRequired()])
    ConfirmPassword = PasswordField('confirmpassword', validators=[DataRequired()])


class GivenTime(Form):
    StartDate = DateField('date', validators=[DataRequired()])
    EndDate = DateField('date', validators=[DataRequired()])

class InputID(Form):
    bookingId = IntegerField('bookingId', validators=[DataRequired()])

class Cash(Form):
    cash_received = DecimalField('cash_received', places = 2, rounding = None, validators=[DataRequired()])

class PayByCash(Form):
    FirstName = TextField('customerfirstname', validators=[DataRequired()])
    LastName = TextField('customerlastname', validators=[DataRequired()])
    Email = TextField('customeremail', validators=[DataRequired()])
