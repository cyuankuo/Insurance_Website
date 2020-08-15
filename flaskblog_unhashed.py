from flask import (
    Flask, render_template, url_for, flash, redirect, g, request, session, Blueprint
)
import mysql.connector.pooling
from forms import RegistrationForm, LoginForm , Customers, Policies, HomeIns, vehicles, payments, invoice, drivers, Home, EmpChoice, EmpHomePage,EmpChoice,CusLoginForm , CusHomePage, SelectPolicyNumber,Empdetails,Update
import os
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

db_user = "root"
db_pass = "PASSWORD"
db_url = "127.0.0.1"

cnx_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="name",
                                                         pool_size=10,
                                                         user=db_user,
                                                         password=db_pass,
                                                         autocommit=True,
                                                         host=db_url,
                                                         database='insuranceplanstest')

def login_required(f):
    @wraps(f)
    def wrapped_func(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))

        return f(**kwargs)

    return wrapped_func



def login_requiredcus(f):
    @wraps(f)
    def wrapped_func(**kwargs):
        if g.user is None:
            return redirect(url_for('logincus'))

        return f(**kwargs)

    return wrapped_func

@app.before_request
def acquire_conn():
    if 'cxn' not in g:
        print('getting connection...')
        g.cxn = cnx_pool.get_connection()



@app.before_request
def load_logged_in_user():
    loginid = session.get('loginid')
    print(loginid)
    loginuser = session.get('username')
    print(loginuser)

    if loginid is None:
        g.user = None
    else:
        cursor = g.cxn.cursor(prepared=True)
        cursor.execute(
            'SELECT username FROM employeeslogin WHERE loginID = %s', (loginid,)
        )
        g.user = cursor.fetchone()
        print("user is")
        print(g.user)

@app.teardown_request
def release_conn(exception):
    if 'cxn' in g:
        print('releasing connection...')
        g.cxn.close()

@app.route('/', methods=['GET','POST'])
def index():

    if request.method == 'POST':

        g.cxn.autocommit=False
        print('start transaction to insert user...')

        g.cxn.start_transaction()
        cursor = g.cxn.cursor(prepared=True)

        firstName = request.form['firstName']
        lastName = request.form['lastName']
        extension = request.form['extension']
        email = request.form['email']
        officeCode = request.form['officeCode']
        reportsTo = request.form['reportsTo']
        jobTitle = request.form['jobTitle']

        sql_insert_query = """ INSERT INTO employees (firstName, lastName, extension, email, officeCode, reportsTo, jobTitle)
                            VALUES (%s, %s, %s, %s, %s, %s, %s) """

        cursor.execute(sql_insert_query, (firstName, lastName, extension, email, officeCode, reportsTo, jobTitle))
        g.cxn.commit()
        g.cxn.autocommit=True
        cursor.close()

    return render_template('index.html')

@app.route('/users')
@login_required
def users():

    print('start transaction to insert user...')
    cursor = g.cxn.cursor(prepared=True)
    cursor.execute("SELECT * from employees")
    userName = cursor.fetchall()
    cursor.close()

    return render_template('users.html', userName = userName)

@app.route("/home", methods=['GET', 'POST'])
def home():
    form = Home()
    if form.validate_on_submit() and form.login.data == 'E' :
        return redirect(url_for('empchoice'))
    elif form.validate_on_submit() and form.login.data == 'C' :
        return redirect(url_for('cushome'))
    return render_template('home1.html', form=form )



@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/home/cushome", methods=['GET', 'POST'])
@login_requiredcus
def cushome():
    form = CusHomePage()
    if form.validate_on_submit() and form.choice.data == 'P' :
        return redirect(url_for('payment'))
    elif form.validate_on_submit() and form.choice.data == 'V' :
        return redirect(url_for('policyno'))

    return render_template('CusHomePage.html', form=form)

@app.route("/home/cushome/policyno", methods=['GET', 'POST'])
#@login_requiredcus
def policyno():
    form = SelectPolicyNumber()
    if form.validate_on_submit():
        cursor=g.cxn.cursor(prepared=True)
        cursor.execute("SELECT * from policies where policyNumber = (%s)",(form.policyNumber.data,))
        userName=cursor.fetchall()
        cursor.close()
        return render_template('users2.html', userName=userName)

    return render_template('selectpolicynumber.html', form=form)

@app.route("/home/cushome/payment", methods=['GET', 'POST'])
#@login_requiredcus
def payment():
    form=payments()
    if request.method == 'POST':
        conn = getattr(g,'cnx_pool.get_connection()',None)
        print('start transaction to insert user...')
        g.cxn.start_transaction()
        cursor = g.cxn.cursor(prepared=True)

        paymentNumber  = request.form['paymentNumber']
        paymentMethod = request.form['paymentMethod']
        paymentDate = request.form['paymentDate']
        amount = request.form['amount']
        invoiceNumber = request.form['invoiceNumber']



        sql_insert_query = """ INSERT INTO payments (  paymentNumber , paymentMethod , paymentDate , amount  , invoiceNumber)
                            VALUES (%s, %s, %s, %s, %s) """

        cursor.execute(sql_insert_query, ( paymentNumber , paymentMethod , paymentDate , amount  , invoiceNumber))
        g.cxn.commit()
        cursor.close()
    if form.validate_on_submit():
        return redirect(url_for('cushome'))
    return render_template('payment.html', title='New Customer Info', form=form)


    #return render_template('selectpolicynumber.html',form=form)

@app.route("/home/empchoice", methods=['GET', 'POST'])
@login_required
def empchoice():
    form = EmpChoice()
    if form.validate_on_submit() and form.choice.data == 'I' :
        return redirect(url_for('Invoice'))
    elif form.validate_on_submit() and form.choice.data == 'V' :
        return redirect(url_for('selectPolicy'))
    elif form.validate_on_submit() and form.choice.data == 'D' :
        return redirect(url_for('deletePolicy'))
    elif form.validate_on_submit() and form.choice.data == 'R' :
        return redirect(url_for('register'))
    elif form.validate_on_submit() and form.choice.data == 'U' :
        return redirect(url_for('update'))
    return render_template('empchoice.html', form=form)


@app.route("/home/empchoice/empinfo", methods=['GET','POST'])
#@login_required
def empinfo():
    form = Empdetails()
    if form.validate_on_submit():
        cursor=g.cxn.cursor(prepared=True)
        cursor.execute("select a.employeeID, a.lastName,a.firstName,a.extension, a.officeCode, a.reportsTo,a.jobTitle , b.city,b.phone,b.addressLine1,b.addressLine2,b.state,b.postalCode from employees a join offices b on a.officeCode=b.officeCode where a.employeeID=%s",(form.username.data,))
        userName=cursor.fetchall()
        cursor.close()
        return render_template('users3.html', userName=userName)
    #return render_template('selectpolicynumber.html', form=form)
    #if form.validate_on_submit():

    return render_template('empinfo.html', form=form)



@app.route("/home/empchoice/update", methods=['GET','POST'])
#@login_required
def update():
    form = Policies()
    if request.method == 'POST':
        conn = getattr(g,'cnx_pool.get_connection()',None)
        print('start transaction to insert user...')
        g.cxn.start_transaction()
        cursor = g.cxn.cursor(prepared=True)
        #print(request.form['username'])
        policyNumber  = request.form['policyNumber']
        startDate = request.form['startDate']
        endDate = request.form['endDate']
        premium = request.form['premium']
        policyStatus = request.form['policyStatus']
        customerID = request.form['username']
        insuranceType = request.form['insuranceType']
        employeeID = request.form['employeeID']
            #cursor.execute('SELECT customerID FROM customerslogin where username = %s', (customerID, ))
            #user = cursor.fetchone() #returns list
            #sql_insert_query = """ UPDATE policies SET policyNumber=policyNumber,startDate=startDate,endDate=endDate,premium=premium,policyStatus=policyStatus,customerID=customerID,insuranceType=insuranceType,employeeID=employeeID)
            #                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """

        cursor.execute('UPDATE policies SET startDate=startDate,endDate=endDate,premium=premium,policyStatus=policyStatus,customerID=customerID,insuranceType=insuranceType,employeeID=employeeID where policyNumber=policyNumber')
        g.cxn.commit()
        cursor.close()
        return render_template('updatepolicies.html',form=form)


@app.route("/home/empchoice/register", methods=['GET'])
#@login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print('show registration form')
        flash(f'Account created for {form.username.data}!', 'success')

    return render_template('register.html', title='Register', form=form)

@app.route('/home/empchoice/register', methods=['POST'])
#@login_required
def register_handle():
    if request.method == 'POST':

        print('start transaction to insert user...')
        # g.cxn.start_transaction()
        cursor = g.cxn.cursor(prepared=True)

        username = request.form['username']
        password = request.form['password']


        sql_insert_query = """ INSERT INTO customerslogin (username, password)
                            VALUES (%s, %s) """

        cursor.execute(sql_insert_query, (username, password))
        g.cxn.commit()
        cursor.close()
        print('handled register form data')

    return redirect(url_for('customers'))

@app.route("/home/empchoice/register/customers", methods=['GET', 'POST'])
#@login_required
def customers():
    form = Customers()
    if request.method == 'POST':

        g.cxn.autocommit=False
        print('start transaction to insert user...')
        g.cxn.start_transaction()
        cursor = g.cxn.cursor(prepared=True)


        username  = request.form['customerID']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        phone = request.form['phone']
        addressLine1 = request.form['addressLine1']
        addressLine2 = request.form['addressLine2']
        city = request.form['city']
        state = request.form['state']
        zipCode = request.form['zipCode']
        gender = request.form['gender']
        maritalStatus = request.form['maritalStatus']
        customerType = request.form['customerType']

        sql_insert_query = """ INSERT INTO customers (firstName,lastName,phone,addressLine1,addressLine2,city,state,zipCode,gender,maritalStatus,customerType)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
      
        sql_insert_customers = " UPDATE customerslogin SET customerslogin.customerID = LAST_INSERT_ID() WHERE username = %s "

        cursor.execute(sql_insert_query, (firstName,lastName,phone,addressLine1,addressLine2,city,state,zipCode,gender,maritalStatus,customerType))
        cursor.execute(sql_insert_customers, (username, ))
        data=cursor.fetchone()
        g.cxn.commit()
        g.cxn.autocommit=True
        cursor.close()

    if form.validate_on_submit():
        return redirect(url_for('policies'))
    return render_template('customers.html', title='New Customer Info', form=form)


@app.route("/home/empchoice/register/customers/policies", methods=['GET', 'POST'])
def policies():
    form = Policies()
    if request.method == 'POST':

        conn = getattr(g,'cnx_pool.get_connection()',None)
        print('start transaction to insert user...')
        g.cxn.start_transaction()
        cursor = g.cxn.cursor(prepared=True)
        print(request.form['username'])
        policyNumber  = request.form['policyNumber']
        startDate = request.form['startDate']
        endDate = request.form['endDate']
        premium = request.form['premium']
        policyStatus = request.form['policyStatus']
        customerID = request.form['username']
        insuranceType = request.form['insuranceType']
        employeeID = request.form['employeeID']
        cursor.execute('SELECT customerID FROM customerslogin where username = %s', (customerID, ))
        user = cursor.fetchone() #returns list
        sql_insert_query = """ INSERT INTO policies (policyNumber,startDate,endDate,premium,policyStatus,customerID,insuranceType,employeeID)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """

        cursor.execute(sql_insert_query, (policyNumber,startDate,endDate,premium,policyStatus,user[0],insuranceType,employeeID))
        g.cxn.commit()
        cursor.close()
    if form.validate_on_submit() and form.insuranceType.data == 'H' :
        return redirect(url_for('homeIns'))
    elif form.validate_on_submit() and form.insuranceType.data == 'A' :
        return redirect(url_for('Vehicles'))

    return render_template('policies.html', title='New Customer Info', form=form)

@app.route("/home/empchoice/register/customers/policies/homeIns", methods=['GET', 'POST'])
def homeIns():
    form = HomeIns()
    if request.method == 'POST':
        conn = getattr(g,'cnx_pool.get_connection()',None)
        print('start transaction to insert user...')
        g.cxn.start_transaction()
        cursor = g.cxn.cursor(prepared=True)

        homeID = request.form ['homeID']
        purchaseDate = request.form['purchaseDate']
        purchaseValue = request.form['purchaseValue']
        area = request.form['area']
        homeType = request.form['homeType']
        autoFireNotification = request.form['autoFireNotification']
        homeSecuritySystem = request.form['homeSecuritySystem']
        swimmingPool = request.form['swimmingPool']
        basement = request.form['basement']
        policyNumber = request.form['policyNumber']
        insuranceType = request.form['insuranceType']


        sql_insert_query = """ INSERT INTO home (homeID,purchaseDate,purchaseValue,area,homeType,autoFireNotification,homeSecuritySystem,swimmingPool,basement,policyNumber,insuranceType)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """

        cursor.execute(sql_insert_query, (homeID , purchaseDate , purchaseValue , area ,homeType , autoFireNotification , homeSecuritySystem , swimmingPool , basement,policyNumber,insuranceType))
        g.cxn.commit()
        cursor.close()
    if form.validate_on_submit():
        return redirect(url_for('emphome'))
    return render_template('homeIns.html', title='Policy Info', form=form)


@app.route("/home/empchoice/register/customers/policies/Vehicles", methods=['GET', 'POST'])
def Vehicles():

    form = vehicles()
    if request.method == 'POST':
        conn = getattr(g,'cnx_pool.get_connection()',None)
        print('start transaction to insert user...')
        g.cxn.start_transaction()
        cursor = g.cxn.cursor(prepared=True)

        vehicleNumber = request.form ['vehicleNumber']
        vehicleModel = request.form['vehicleModel']
        makeModelYear = request.form['makeModelYear']
        status = request.form['status']
        policyNumber = request.form['policyNumber']
        insuranceType = request.form['insuranceType']


        sql_insert_query = """ INSERT INTO vehicles (vehicleNumber , vehicleModel , makeModelYear , status , policyNumber , insuranceType)
                            VALUES (%s, %s, %s, %s, %s, %s) """

        cursor.execute(sql_insert_query, (vehicleNumber , vehicleModel , makeModelYear , status , policyNumber , insuranceType))
        g.cxn.commit()
        cursor.close()
    if form.validate_on_submit():

        return redirect(url_for('Drivers'))
    return render_template('vehicles.html', title='New Customer Info', form=form)



@app.route("/home/empchoice/register/customers/policies/Vehicles/Drivers", methods=['GET', 'POST'])
def Drivers():
    form = drivers()
    if request.method == 'POST':

        conn = getattr(g,'cnx_pool.get_connection()',None)
        print('start transaction to insert user...')
        g.cxn.start_transaction()
        cursor = g.cxn.cursor(prepared=True)

        licenseNumber  = request.form['licenseNumber']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        dob = request.form['dob']

        sql_insert_query = """ INSERT INTO drivers ( licenseNumber , firstName , lastName  , dob)
                            VALUES (%s, %s, %s, %s) """

        cursor.execute(sql_insert_query, ( licenseNumber , firstName , lastName  , dob))
        g.cxn.commit()
        cursor.close()
    if form.validate_on_submit():
        return redirect(url_for('emphome'))
    return render_template('driver.html', title='New Customer Info', form=form)



@app.route("/home/empchoice/Invoice", methods=['GET', 'POST'])
def Invoice():
    form = invoice()
    if request.method == 'POST':
        conn = getattr(g,'cnx_pool.get_connection()',None)
        print('start transaction to insert user...')
        g.cxn.start_transaction()
        cursor = g.cxn.cursor(prepared=True)

        invoiceNumber  = request.form['invoiceNumber']
        dueDate = request.form['dueDate']
        amount = request.form['amount']
        policyNumber = request.form['policyNumber']
        insuranceType = request.form['insuranceType']

        sql_insert_query = """ INSERT INTO invoices ( invoiceNumber , dueDate  , amount  , policyNumber , insuranceType)
                            VALUES (%s, %s, %s, %s, %s) """

        cursor.execute(sql_insert_query, (invoiceNumber , dueDate  , amount  , policyNumber , insuranceType))
        g.cxn.commit()
        cursor.close()
    if form.validate_on_submit():
        return redirect(url_for('empchoice'))
    return render_template('invoice.html', title='New Customer Info', form=form)


@app.route("/home/empchoice/selectPolicy", methods=['GET', 'POST'])
def selectPolicy():

    form = SelectPolicyNumber()

    if form.validate_on_submit():
        cursor=g.cxn.cursor(prepared=True)
        cursor.execute("SELECT * from policies where policyNumber = (%s)",(form.policyNumber.data,))
        userName=cursor.fetchall()
        cursor.close()
        return render_template('users2.html', userName=userName)
    return render_template('selectpolicynumber.html', form=form)

@app.route("/home/empchoice/deletePolicy", methods=['GET', 'POST'])
def deletePolicy():
    form = SelectPolicyNumber()
    if form.validate_on_submit():
        cursor=g.cxn.cursor(prepared=True)
        cursor.execute("DELETE from policies where policyNumber = (%s)",(form.policyNumber.data,))
        cursor.close()
        g.cxn.commit()
        #flash('Account had been Deleted!', 'success')
    return render_template('delete.html', form=form)

@app.route("/login/Invoice/Payment", methods=['GET', 'POST'])
def Payment():
    form = payments()
    return render_template('payment.html', title='New Customer Info', form=form)


@app.route("/login", methods=['GET'])

def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/login", methods=['POST'])
def login_handler():
    if request.method == 'POST':

        print('start transaction to check user...')

        cursor = g.cxn.cursor(prepared=True)

        username = request.form['email']
        password = request.form['password']

        sql_select_query = 'SELECT * FROM employeeslogin where username = %s'
        error = None

        cursor.execute(sql_select_query, (username, ))
        user = cursor.fetchone() #returns list

        for (loginID, username, password) in cursor:
            print('user inserted: login_id={} user_id={} password={}'.format(loginID,username, password))

        if user is None:
            error = 'Incorrect username'
            flash(error)
        elif user[2] != password:
            error = 'Incorrect password'
            flash(error)
            return redirect(url_for('login'))


        if error is None:
            session.clear()
            session['loginid'] = user[0]
            session['username'] = user[1]


        cursor.close()
        print('handled login form data')

    return redirect(url_for('empchoice'))

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('home'))



@app.route("/logincus", methods=['GET'])

def logincus():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logincus", methods=['POST'])
def login_handlercus():
    if request.method == 'POST':

        print('start transaction to check user...')

        cursor = g.cxn.cursor(prepared=True)

        username = request.form['email']
        password = request.form['password']

        sql_select_query = 'SELECT * FROM customerslogin where username = %s'
        error = None

        cursor.execute(sql_select_query, (username, ))
        user = cursor.fetchone() #returns list

        for (loginID, username, password) in cursor:
            print('user inserted: login_id={} user_id={} password={}'.format(loginID,username, password))

        if user is None:
            error = 'Incorrect username'
            flash(error)
        elif user[2] != password:
            error = 'Incorrect password'
            flash(error)
            return redirect(url_for('logincus'))


        if error is None:
            session.clear()
            session['loginid'] = user[0]
            session['username'] = user[1]


        cursor.close()
        print('handled login form data')

    return redirect(url_for('cushome'))

@app.route('/logoutcus', methods=['POST'])
def logoutcus():
    session.clear()
    return redirect(url_for('home'))




if __name__ == '__main__':
    app.run(debug=True, port=6900)
