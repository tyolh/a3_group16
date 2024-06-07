from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateField, TimeField, IntegerField, DecimalField, SelectField
from wtforms.validators import InputRequired, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

#Create new event
class EventForm(FlaskForm):
  name = StringField('Event Name', validators=[InputRequired()])
  date = DateField('Start Date', format='%Y-%m-%d')
  start_time = TimeField('Start Time')
  location = TextAreaField('Location', validators=[InputRequired()])
  description = TextAreaField('Description', validators=[InputRequired()])
  sports = ['AFL', 'Basketball', 'Boxing', 'Cricket', 'Golf', 'Tennis']
  sport = SelectField(label='Status', choices=sports)
  price = IntegerField('Price', render_kw={'Ticket Price': 'Enter the ticket price'})
  state = ['Open', 'Cancelled']
  status = SelectField(label='Status', choices=state)
  image = FileField('Event Image', validators=[FileRequired(message='Image cannot be empty'),FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])
  submit = SubmitField("Create")

# Booking the Event Form
class BookEvent(FlaskForm):
    emailid=StringField("Email Address", validators=[InputRequired('Enter email')])
    cardnum = IntegerField('Card Number', validators=[InputRequired()])
    quantity = IntegerField('Quantity')
    expiry = StringField('Expiry Date')
    CVV =  IntegerField('Security Code')
    submit = SubmitField("Book Event")
    
#User login
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

#User register
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    
    #linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    #submit button
    submit = SubmitField("Register")

#User comment
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')


# Flask forn to update an events information
class UpdateEvent(FlaskForm):
    state = ['Open', 'Cancelled'] # created a list of options for a user to choose when upating the status of the event
    sports = ['AFL', 'Basketball', 'Boxing', 'Cricket', 'Golf', 'Tennis']
    date = DateField('Start Date', format='%Y-%m-%d')
    name = StringField('Event Title', validators=[InputRequired()])
    start_time = TimeField('Start Time')
    description = TextAreaField('Description', validators=[InputRequired()])
    location = TextAreaField('Mailing Address')
    sport = SelectField(label='Status', choices=sports)
    price =IntegerField('Price', render_kw={'TIcket Price': 'Enter the ticket price'})
    status = SelectField(label='Status', choices=state)
    submit = SubmitField('Create')
