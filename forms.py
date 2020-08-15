from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, RadioField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')




class Customers(FlaskForm):
    customerID = StringField('Customer ID',validators=[DataRequired()])
    firstName = StringField('First Name',validators=[DataRequired(), Length(min=1, max=20)])
    lastName = StringField('Last Name',validators=[Length(min=1, max=20)])
    phone = StringField('phone',validators=[DataRequired(), Length(min=10, max=10)])
    addressLine1=StringField('Address Line 1',validators=[DataRequired(),Length(min=1, max=50)])
    addressLine2=StringField('Address Line 2',validators=[Length(min=1, max=50)])
    city=StringField('City',validators=[DataRequired(),Length(min=1, max=50)])
    state=StringField('State',validators=[DataRequired(),Length(min=2, max=2)])
    zipCode=StringField('Zipcode',validators=[DataRequired(),Length(min=1, max=15)])
    gender=RadioField('Gender',choices=[('M','Male'),('F','Female')])
    maritalStatus=RadioField('Marital Status',choices=[('S','Single'),('M','Married'),('W','Widow/Widower')])
    customerType=RadioField('Type Of Insurance',choices=[('H','Home Insurance'),('A','Auto Insurance')])
    submit = SubmitField('Next')

class Policies(FlaskForm):
    policyNumber = StringField('Policy Number',validators=[DataRequired(), Length(min=5, max=5)])
    startDate = DateField ('Start Date',validators=[DataRequired()])
    endDate = DateField ('End Date',validators=[DataRequired()])
    premium = StringField('Premium',validators=[DataRequired(), Length(min=0, max=10)])
    policyStatus=RadioField('Policy Status',choices=[('C','Current'),('P','Expired')])
    username = StringField('Customer username',validators=[ Length(min=5, max=5)])
    insuranceType = RadioField('Insurance Type',choices=[('H','Home Insurance'),('A','Auto Insurance')])
    employeeID = StringField('Employee ID',validators=[ Length(min=4, max=4)])
    submit = SubmitField('Next')

class HomeIns(FlaskForm):
    homeID = StringField('Home ID',validators=[DataRequired(), Length(min=5, max=5)])
    purchaseDate = DateField ('Purchase Date',validators=[DataRequired()])
    purchaseValue = StringField('Purchase Value ',validators=[DataRequired(), Length(min=0, max=10)])
    area = StringField('Area',validators=[DataRequired(), Length(min=0, max=8)])
    homeType = RadioField('Home Type',choices=[('S','Single Family'),('M','Multi Family'),('C','Condominium'),('T','Town House')],validators=[DataRequired()])
    autoFireNotification = RadioField('Auto Fire Notification',choices=[('1','Yes'),('0','No')],validators=[DataRequired()])
    homeSecuritySystem = RadioField('Home Security System',choices=[('1','Yes'),('0','No')],validators=[DataRequired()])
    swimmingPool = RadioField('Swimming Pool',choices=[('U','Underground'),('I','Indoor'),('O','Overground')],validators=[DataRequired()])
    basement = RadioField('Basement',choices=[('1','Yes'),('0','No')],validators=[DataRequired()])
    policyNumber = StringField('Policy Number',validators=[DataRequired(), Length(min=5, max=5)])
    insuranceType = RadioField('Insurance Type',choices=[('H','Home Insurance'),('A','Auto Insurance')])
    submit = SubmitField('Finish')


class vehicles(FlaskForm):
    vehicleNumber = StringField('Vehicles Number',validators=[DataRequired(), Length(min=5, max=5)])
    vehicleModel = StringField ('Vehicle Model',validators=[DataRequired(), Length(min=1, max=50)])
    makeModelYear = DateField ('Model Year',validators=[DataRequired()])
    status = RadioField ('Vehicle Status',choices=[('O','Owned'),('L','Leased'),('F','Financed')])
    policyNumber = StringField('Policy Number',validators=[DataRequired(), Length(min=5, max=5)])
    insuranceType = RadioField('Insurance Type',choices=[('H','Home Insurance'),('A','Auto Insurance')])
    submit = SubmitField('Next')
    #policyNumber = IntegerField('Policy Number',validators=[DataRequired(), Length(min=5, max=5)])
    #insuranceType = RadioField('Insurance Type',choices=[('Home','Home Insurance'),('Auto','Auto Insurance')])

class drivers(FlaskForm):
    licenseNumber = StringField('License Number',validators=[DataRequired(), Length(min=5, max=5)])
    firstName = StringField('First Name',validators=[DataRequired(), Length(min=1, max=20)])
    lastName = StringField('Last Name',validators=[DataRequired(), Length(min=1, max=20)])
    dob = DateField ('Date of Birth',validators=[DataRequired()])
    submit = SubmitField('Finish')

class payments(FlaskForm):
    paymentNumber = StringField('Payment Number',validators=[DataRequired(), Length(min=5, max=5)])
    paymentMethod = RadioField ('Vehicle Status',choices=[('PayPal','PayPal'),('Credit','Credit'),('Debit','Debit'),('Check','Check')])
    paymentDate = DateField ('Payment Date',validators=[DataRequired()])
    amount = StringField('Payment Amount',validators=[DataRequired(), Length(min=1, max=10)])
    invoiceNumber = StringField('Invoice Number',validators=[DataRequired(), Length(min=5, max=5)])
    submit = SubmitField('Thank You for Your Payment')

class invoice(FlaskForm):
    invoiceNumber = StringField('Invoice Number',validators=[DataRequired(), Length(min=5, max=5)])
    dueDate = DateField ('Due Date',validators=[DataRequired()])
    amount = StringField('Payment Amount',validators=[DataRequired(), Length(min=1, max=10)])
    submit = SubmitField('Finish ')
    policyNumber = StringField('Policy Number',validators=[DataRequired(), Length(min=5, max=5)])
    insuranceType = RadioField('Insurance Type',choices=[('H','Home Insurance'),('A','Auto Insurance')])


class employees(FlaskForm):
    employeeID = StringField('Employee ID',validators=[DataRequired(), Length(min=5, max=5)])
    firstName = StringField('First Name',validators=[DataRequired(), Length(min=1, max=20)])
    lastName = StringField('Last Name',validators=[DataRequired(), Length(min=1, max=20)])
    reportsTo = StringField('Reports to Employee: ',validators=[Length(min=5, max=5)])
    jobTitle = StringField('First Name',validators=[DataRequired(), Length(min=1, max=20)])
    submit = SubmitField('Next')

class offices(FlaskForm):
    officeCode = StringField('Office Code',validators=[DataRequired(), Length(min=1, max=5)])
    phone = StringField('phone',validators=[DataRequired(), Length(min=10, max=10)])
    addressLine1=StringField('Address Line 1',validators=[DataRequired(),Length(min=1, max=50)])
    addressLine2=StringField('Address Line 2',validators=[Length(min=1, max=50)])
    city=StringField('City',validators=[DataRequired(),Length(min=1, max=50)])
    state=StringField('State',validators=[Length(min=1, max=50)])
    postalCode=StringField('Postal code',validators=[DataRequired(),Length(min=1, max=15)])
    submit = SubmitField('Next')


class Home(FlaskForm):
    login = RadioField ('Login',choices=[('E','Employee Login'),('C','Customer Login')])
    submit = SubmitField('Next')


class EmpLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class CusLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class Empdetails(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Login')


class Update(FlaskForm):
    policyNumber = StringField('policyNumber', validators=[DataRequired()])
    submit = SubmitField('Login')

class next(FlaskForm):
    submit = SubmitField('Login')

class EmpHomePage(FlaskForm):
    choice = RadioField ('',choices=[('R','Register a new customer'),('V','View an existing Policy')])
    submit = SubmitField('Next')


class CusHomePage(FlaskForm):
    choice = RadioField ('What do you want to do?',choices=[('P','Payment'),('V','View an existing Policy')])
    submit = SubmitField('Next')

class SelectPolicyNumber(FlaskForm):
    policyNumber = StringField('Policy Number',validators=[DataRequired(), Length(min=5, max=5)])
    submit = SubmitField('Next')

class EmpChoice(FlaskForm):
    choice = RadioField ('What do you want to do?',choices=[('R','Register a New Customer'),('V','View Existing Policy Details'),('I','Generate Invoice'),('D','Delete Policy'),('U','Update an Existing Policy'),('E','View Employee Info')])
    submit = SubmitField('Next')

class EmpCusLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
