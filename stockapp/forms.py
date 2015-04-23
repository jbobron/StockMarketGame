from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, ValidationError, PasswordField, validators
from models import db, User, Portfolio, Stock, Group, UserGroups

class ContactForm(Form):
  name = TextField("Name",  [validators.Required("Please enter your name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  subject = TextField("Subject",  [validators.Required("Please enter a subject.")])
  message = TextAreaField("Message",  [validators.Required("Please enter a message.")])
  submit = SubmitField("Send")

class SignupForm(Form):
  firstname = TextField("First name",  [validators.Required("Please enter your first name.")])
  lastname = TextField("Last name",  [validators.Required("Please enter your last name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Create account")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      self.email.errors.append("That email is already taken")
      return False
    else:
      return True

class SigninForm(Form):
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Sign In")
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user and user.check_password(self.password.data):
      return True
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False


class MakeTradeForm(Form):
  ticker = TextField("Ticker", [validators.Required("Please enter a  ticker")])
  quantity = TextField("Quantity", [validators.Required("Please enter a quantity")])
  submit = SubmitField("Make Trade")
  
  # def __init__(self, *args, **kwargs):
  #   Form.__init__(self, *args, **kwargs)
 
  # def validate(self):
  #   if not Form.validate(self):
  #     return False
# class MakeGameForm(Form):
#   game = TextField("Game Name",  [validators.Required("Please enter your game name.")])
#   startDate = TextField("Start Date",  [validators.Required("Please enter your start date.")])
#   endDate = TextField("End Date",  [validators.Required("Please enter your end date.")])
#   startingCash = TextField("Starting Cash",  [validators.Required("Please enter your starting cash.")])
#   submit = SubmitField("Create game")

#   def __init__(self, *args, **kwargs):
#     Form.__init__(self, *args, **kwargs)
 
#   def validate(self):
#     if not Form.validate(self):
#       return False
     
#     group = Group.query.filter_by(groupname = self.groupname.data.lower()).first()
#     if user:
#       self.email.errors.append("That group name is already taken")
#       return False
#     else:
#       return True

