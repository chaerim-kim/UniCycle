from flask import render_template, url_for, flash, redirect, session, request
from app import app, db, models
from config import ADMINS
from .forms import CardDetailForm, TimeSelect, BikeIsFree, Login, CreateAccount, GivenTime, PayByCash, InputID, Cash
from random import *
from decimal import *
from io import BytesIO
import datetime, hashlib, binascii
import qrcode
import base64
import itertools
from xhtml2pdf import pisa
import matplotlib.pyplot as plt
from matplotlib.dates import (YEARLY, DateFormatter, rrulewrapper, RRuleLocator, drange)
import numpy as np

# Global variables used to pass booking information between pages
data = []
booking = None

# Displays the home page
@app.route('/')
def index():
    loggedIn= isLoggedIn()

    return render_template('home_page.html', loggedIn = loggedIn)

# Displays the about page
@app.route('/about')
def about():
    loggedIn= isLoggedIn()

    return render_template('about.html', loggedIn = loggedIn)



#  printing number of bikes available in each locations
@app.route('/location')
def location():
    loggedIn= isLoggedIn()

    form = BikeIsFree()

    location1 = 0
    location2 = 0
    location3 = 0

    for i in models.Bike.query.all():
        if i.current_location == 1:
            location1 = location1+1
        if i.current_location == 2:
            location2 = location2+1
        if i.current_location == 3:
            location3 = location3+1

    getBikeNumber = [location1, location2, location3]
    getLocationName = []

    for i in models.Location.query.all():
        getLocationName.append(i.name)

    return render_template('bicycle_location.html',
                           form=form,
                           getBikeNumber=getBikeNumber,
                           getLocationName=getLocationName,
                           loggedIn = loggedIn)

# Displays the form for the user to check
@app.route('/availability', methods=['GET', 'POST'])
def availability():
    loggedIn= isLoggedIn()

    form = TimeSelect()

    availableLocations = ["University", "City", "Headingly"]
    availableBikes =[]
    uniBike=[]
    cityBike=[]
    headingleyBike=[]


    if form.validate_on_submit():
        if form.Date.data < datetime.datetime.now().date():
            flash("Selected date is in the past. Please select a different date.")
        else:
            startDate = form.Date.data
            hirePeriod = form.HirePeriod.data
            endDate = findEndDate(startDate, int(hirePeriod))
            dateTimeValue = datetime.datetime.combine(startDate, datetime.time(int(hirePeriod),00))
            availableBikes = displayAvailability(startDate, endDate)
            if availableBikes==[]:
                flash("There are no bikes available at your chosen start date")
            else:


                for i in availableBikes:
                    if i.current_location == 1:
                        uniBike.append(i.id)

                for i in availableBikes:
                    if i.current_location == 2:
                        cityBike.append(i.id)

                for i in availableBikes:
                    if i.current_location == 3:
                        headingleyBike.append(i.id)

    return render_template('bicycle_availability.html',
                           form=form,
                           availableLocations=availableLocations,
                           uniBike=uniBike,
                           cityBike=cityBike,
                           headingleyBike=headingleyBike,
                           loggedIn = loggedIn)

# Displays the page for users to select a bicycle location, date and period to book a bicycle
@app.route('/book', methods=['GET', 'POST'])
def book():
    global data

    loggedIn= isLoggedIn()

    form = BikeIsFree()

    if form.validate_on_submit():
            enddate = findEndDate(form.Date.data, int(form.HirePeriod.data))

            if form.Date.data < datetime.datetime.now().date():
                flash("Selected date is in the past. Please select a different date.")
            else:
                try:
                    data = []
                    bicycle = checkAvailability(int(form.Location.data), form.Date.data, enddate)

                    if bicycle != -1:
                        data.append(bicycle)
                        data.append(int(form.Location.data))
                        data.append(form.Date.data)
                        data.append(enddate)
                        data.append(int(form.HirePeriod.data))

                        if request.form['action'] == 'Pay by Card':
                            return redirect(url_for('hireform'))
                        elif request.form['action'] == 'Pay by Cash':
                            return redirect(url_for('cash'))
                    else:
                        flash("There is no bicycle available at that location at the specified time.")
                except:
                    flash("An error occurred and your bicycle has not booked.")

    return render_template('bicycle_book.html',
                           form=form,
                           loggedIn = loggedIn)

# Displays the form for users to fill in to pay for a booking by cash
@app.route('/cash', methods=['GET', 'POST'])
def cash():

    form = PayByCash()

    loggedIn= isLoggedIn()

    for account in models.Account.query.all():
        if loggedIn != 0 and session['sessionid'] ==  account.id and account.account_type == 3:
            form.FirstName.data = account.firstname
            form.LastName.data = account.surname
            form.Email.data = account.username

            break

    if form.validate_on_submit():
        if validEmailAddress(form.Email.data) == False:
            flash("Invalid email address.")
        else:
            try:
                daysRented = data[4]
                rate = 2.50
                price = 0
                dayCount = daysRented

                while dayCount != 0:
                    price += rate
                    rate -= 0.1
                    dayCount -= 1

                price = round(Decimal(price), 2)

                book = makeBooking(data[0], data[2], data[3], data[1], str(price), False)
                location = getLocation(data[1])

                img = qrcode.make("Booking ID: " + str(book))
                buffered = BytesIO()
                img.save(buffered, format="png")

                img_str = base64.b64encode(buffered.getvalue())

                sendEmail("Your UniCycle Booking Receipt", ADMINS[0], [form.Email.data], str(book),
                          render_template("receipt.html",
                                          name=form.FirstName.data,
                                          bicycle=data[0],
                                          start=data[2],
                                          end=data[3],
                                          location=location,
                                          qr=img_str.decode('utf-8'),
                                          price=str(price)))

                return render_template('booking_confirm.html',
                                       bicycle=data[0],
                                       start=data[2],
                                       end=data[3],
                                       location=location,
                                       price=str(price),
                                       loggedIn=loggedIn)
            except:
                flash("An error occurred and your bicycle has not been booked.")


    return render_template('cash_payment.html',
                           form=form,
                           loggedIn=loggedIn)

# Displays the form for users to fill in to pay for a booking by card
@app.route('/hireform', methods=['GET', 'POST'])
def hireform():
    global data

    loggedIn= isLoggedIn()

    form = CardDetailForm()

    if request.method == 'GET':
        for card in models.Card.query.all():
            for account in models.Account.query.all():
                if loggedIn != 0 and session['sessionid'] ==  card.user_id and card.user_id == account.id:
                    form.CustomerFirstName.data = account.firstname
                    form.CustomerLastName.data = account.surname
                    form.CustomerEmail.data = account.username
                    form.CustomerAddress1.data = card.card_address1
                    form.CustomerPostcode.data = card.card_postcode
                    form.CardType.data = str(card.card_type)
                    form.CardHolderName.data = card.cardholder_name
                    form.CardNumber.data = card.card_number
                    form.CardExpireDate.data = card.card_expiry_date.date()

                    break

    if form.validate_on_submit():
        try:
            check_cvv = int(form.CardCVV.data)
            valid_cvv=True
        except:
            valid_cvv=False
            flash("CVV must contain digits only")

        if validEmailAddress(form.CustomerEmail.data) == False:
            flash("Invalid email address.")
        elif form.CardExpireDate.data <= datetime.datetime.now().date():
            flash("Your card has expired. Please use a different card.")
        elif len(str(form.CardNumber.data)) != 16:
            flash("Card number must be 16 digits long.")
        elif len(form.CardCVV.data) != 3:
            flash("CVV must be 3 digits long.")
        else:
            try:
                if valid_cvv == True:
                    if form.SaveCard.data:
                        storeCardDetails(form.CardHolderName.data,
                                         form.CardNumber.data,
                                         form.CardExpireDate.data,
                                         int(form.CardType.data),
                                         form.CustomerAddress1.data,
                                         form.CustomerAddress2.data,
                                         form.CustomerCity.data,
                                         form.CustomerPostcode.data)

                    daysRented = data[4]
                    rate = 2.50
                    price = 0
                    dayCount = daysRented

                    while dayCount != 0:
                        price += rate
                        rate -= 0.1
                        dayCount -= 1

                    price = round(Decimal(price), 2)

                    book = makeBooking(data[0], data[2], data[3], data[1], str(price), True)
                    location = getLocation(data[1])

                    img = qrcode.make("Booking ID: " + str(book))
                    buffered = BytesIO()
                    img.save(buffered, format="png")

                    img_str = base64.b64encode(buffered.getvalue())

                    sendEmail("Your UniCycle Booking Receipt", ADMINS[0], [form.CustomerEmail.data], str(book),
                              render_template("receipt.html",
                                              name=form.CustomerFirstName.data,
                                              bicycle=data[0],
                                              start=data[2],
                                              end=data[3],
                                              location=location,
                                              qr=img_str.decode('utf-8'),
                                              price=str(price)))

                    return render_template('booking_confirm.html',
                                           bicycle=data[0],
                                           start=data[2],
                                           end=data[3],
                                           location=location,
                                           price=str(price),
                                           loggedIn=loggedIn)
            except:
                flash("An error occurred and your bicycle has not been booked.")

    return render_template('booking_form.html',
                           form=form,
                           loggedIn=loggedIn)

# Displays the page to create a user account
@app.route('/register', methods=['GET','POST'])
def register():

    loggedIn= isLoggedIn()

    form = CreateAccount()

    if form.validate_on_submit():
        try:
            if validEmailAddress(form.EmailAddress.data) == True:
                if checkEmail(form.EmailAddress.data) == True:
                    if form.Password.data == form.ConfirmPassword.data:
                        if validPassword(form.Password.data):
                            addAccount(form.Surname.data,form.FirstName.data,form.EmailAddress.data,form.Password.data)

                            return redirect(url_for('register_confirm'))
                    else:
                        flash("Your passwords don't match, your account has not been created.")
            else:
                flash("Invalid email address.")
        except:
            flash("An error occurred and your account has not been created.")

    return render_template('register_form.html',
                           form=form,
                           loggedIn=loggedIn)

# Displays confirmation that a user account has been created
@app.route('/register_confirm')
def register_confirm():

    loggedIn= isLoggedIn()

    return render_template('register_confirm.html',
                           loggedIn=loggedIn)

# Logs users in
@app.route('/login', methods=['GET','POST'])
def login():

    loggedIn= isLoggedIn()

    form = Login()

    if form.validate_on_submit():
        try:
            if loginCheckUser(form.EmailAddress.data,form.Password.data) == True :
                accountID =  getIdForSession(form.EmailAddress.data, form.Password.data)
                session['sessionid'] = accountID
                return redirect(url_for('availability'))
        except:
            flash("Incorrect username or password has been provided. \nPlease try again.")

    return render_template('login.html',
                           form=form,
                           loggedIn=loggedIn)

@app.route('/staff_login', methods=['GET','POST'])
def staff_login():

    loggedIn= isLoggedIn()

    form = Login()

    if form.validate_on_submit():
        try:
            if loginCheckStaff(form.EmailAddress.data,form.Password.data) == True:
                accountID =  getIdForSession(form.EmailAddress.data, form.Password.data)
                session['sessionid'] = accountID
                return redirect(url_for('availability'))
        except:
            flash("Incorrect username or password has been provided. \nPlease try again.")

    return render_template('staff_login.html',
                           form=form,
                           loggedIn=loggedIn)


# Displays a logged in user's previous bookings
@app.route('/profile')
def profile():

    loggedIn = isLoggedIn()

    accountID =  session['sessionid']
    bookings = models.Booking.query.filter_by(user_id=accountID)
    accountBook = []

    for i in bookings:
        accountBook.append(i)

    return render_template('profile.html',
                           loggedIn=loggedIn,
                           accountBook=accountBook)

# Employee can display customer booking receipts
@app.route('/view_receipts')
def view_receipts():

    loggedIn = isLoggedIn()

    accountID =  session['sessionid']
    bookings = models.Booking.query.all()
    accountBook = []

    for i in bookings:
        accountBook.append(i)

    return render_template('view_receipts.html',
                           loggedIn=loggedIn,
                           accountBook = accountBook)



# Logs the user out
@app.route('/logout')
def logout():
    session.pop('sessionid',None)

    return redirect(url_for('index'))

# Employee retrieves cash booking
@app.route('/take_payment', methods=['GET', 'POST'])
def take_payment():
    global booking

    loggedIn = isLoggedIn()
    form = InputID()

    if form.validate_on_submit():
        booking = models.Booking.query.get(form.bookingId.data)
        try:
            if booking.paid == False:
                return redirect(url_for('cash_calculation'))
            else:
                flash("Booking has already been paid for")
        except:
            flash("Booking does not exist")

    return render_template('take_payment.html',
                           form=form,
                           loggedIn=loggedIn)

# Employee calculates change for customer and marks cash cooking as being paid
@app.route('/cash_calculation', methods=['GET', 'POST'])
def cash_calculation():
    global booking

    loggedIn = isLoggedIn()
    form = Cash()

    if form.validate_on_submit():
        localBooking = models.Booking.query.get(booking.id)
        localBooking.paid = True
        db.session.commit()
        return redirect(url_for('payment_confirm'))

    return render_template('cash_calculation.html',
                           form=form,
                           loggedIn=loggedIn,
                           bicycle=booking.bike_id,
                           location=booking.start_location,
                           start=booking.start_time,
                           end=booking.end_time,
                           price=booking.price)

# Displays confirmation that a user has made a booking
@app.route('/payment_confirm')
def payment_confirm():

    loggedIn= isLoggedIn()

    return render_template('payment_confirm.html',
                           loggedIn=loggedIn)

# Allows admin users to view bicycle number statistics by location
@app.route('/compare_location', methods=['GET', 'POST'])
def compare_location():



    loggedIn= isLoggedIn()

    form = GivenTime()


    startDate = form.StartDate.data
    endDate = form.EndDate.data


    values,values1,values2,values3,dates = [],[],[],[],[]
    yGrid=0

    bookings = models.Booking.query.filter(models.Booking.start_time.between(startDate,endDate))

    i = startDate
    while i != endDate:


        localHired = 0
        dates.append(i)
        for book in bookings:
                if book.paid == True:
                    if book.start_time.date() == i:
                        localHired = localHired + 1
        values.append(localHired)
        localHired = 0
        for book in bookings:
                if book.paid == True:
                    if book.start_time.date() == i:
                        if book.start_location == 1:
                            localHired = localHired + 1
        values1.append(localHired)
        localHired = 0
        for book in bookings:
                if book.paid == True:
                    if book.start_time.date() == i:
                        if book.start_location == 2:
                            localHired = localHired + 1
        values2.append(localHired)
        localHired = 0
        for book in bookings:
                if book.paid == True:
                    if book.start_time.date() == i:
                        if book.start_location == 3:
                            localHired = localHired + 1
        values3.append(localHired)

        i = i + datetime.timedelta(days = 1)

    try:
        yGrid=max(values)+1
    except:
        yGrid=1

    plt.figure(1, figsize=(20, 4))
    plt.xlabel('Date')
    plt.ylabel('Bikes Hired')
    plt.bar(dates, values)
    plt.suptitle('Overall bikes hired')
    plt.savefig('app/static/images/graphs/OverallGraph.png')
    plt.cla()
    plt.axis([startDate, endDate, 0, yGrid])
    plt.xlabel('Dates')
    plt.ylabel('Bikes Hired')
    plt.bar(dates, values1)
    plt.suptitle('University bikes hired')
    plt.savefig('app/static/images/graphs/Location1Graph.png')
    plt.cla()
    plt.axis([startDate, endDate, 0, yGrid])
    plt.xlabel('Dates')
    plt.ylabel('Bikes Hired')
    plt.bar(dates, values2)
    plt.suptitle('City bikes hired')
    plt.savefig('app/static/images/graphs/Location2Graph.png')
    plt.cla()
    plt.axis([startDate, endDate, 0, yGrid])
    plt.xlabel('Dates')
    plt.ylabel('Bikes Hired')
    plt.bar(dates, values3)
    plt.suptitle('Headingly bikes hired')
    plt.savefig('app/static/images/graphs/Location3Graph.png')
    plt.cla()
    overallIncome = 0
    availableLocations = ["University", "City", "Headingly"]

    overallHired = 0

    for book in bookings:
        if book.paid == True:
            overallHired = overallHired + 1

    LIArray = []

    for place in models.Location.query.all():
        localHired = 0
        for book in bookings:
            if book.start_location == place.id:
                if book.paid == True:
                    localHired = localHired + 1
        LIArray.append(str(place.name) + "  :  " + str(localHired))

    plt.clf()

    return render_template('compare_location.html',
                            form=form,
                            loggedIn=loggedIn,
                            overallHired=overallHired,
                            LIArray=LIArray)

# Allows admin users to view income statistics by location
@app.route('/income', methods=['GET', 'POST'])
def income():


    form = GivenTime()

    loggedIn= isLoggedIn()

    startDate = form.StartDate.data


    endDate = form.EndDate.data


    values,values1,values2,values3,dates = [],[],[],[],[]

    bookings = models.Booking.query.filter(models.Booking.start_time.between(startDate,endDate))

    i = startDate
    while i != endDate:
        localIncome = 0
        dates.append(i)
        for book in bookings:
                if book.paid == True:
                    if book.start_time.date() == i:
                        localIncome = localIncome + Decimal(book.price)
        values.append(localIncome)
        localIncome = 0
        for book in bookings:
                if book.paid == True:
                    if book.start_time.date() == i:
                        if book.start_location == 1:
                            localIncome = localIncome + Decimal(book.price)
        values1.append(localIncome)
        localIncome = 0
        for book in bookings:
                if book.paid == True:
                    if book.start_time.date() == i:
                        if book.start_location == 2:
                            localIncome = localIncome + Decimal(book.price)
        values2.append(localIncome)
        localIncome = 0
        for book in bookings:
                if book.paid == True:
                    if book.start_time.date() == i:
                        if book.start_location == 3:
                            localIncome = localIncome + Decimal(book.price)
        values3.append(localIncome)

        i = i + datetime.timedelta(days = 1)

    try:
        yGrid = int(max(values)+1)
    except:
        yGrid=1



    plt.figure(1, figsize=(20, 4))
    plt.xlabel('Date')
    plt.ylabel('Income (£)')
    plt.axis([startDate, endDate, 0, yGrid])
    plt.bar(dates, values)
    plt.suptitle('Overall Income')
    plt.savefig('app/static/images/graphs/OverallGraph.png')
    plt.cla()
    plt.axis([startDate, endDate, 0, yGrid])
    plt.bar(dates, values1)
    plt.suptitle('University Income')
    plt.savefig('app/static/images/graphs/Location1Graph.png')
    plt.cla()
    plt.axis([startDate, endDate, 0, yGrid])
    plt.bar(dates, values2)
    plt.suptitle('City Income')
    plt.savefig('app/static/images/graphs/Location2Graph.png')
    plt.cla()
    plt.axis([startDate, endDate, 0, yGrid])
    plt.bar(dates, values3)
    plt.suptitle('Headingly Income')
    plt.savefig('app/static/images/graphs/Location3Graph.png')
    plt.cla()
    overallIncome = 0
    availableLocations = ["University", "City", "Headingly"]

    for book in bookings:
        if book.paid == True:
            overallIncome = overallIncome + Decimal(book.price)

    LIArray = []

    for place in models.Location.query.all():
        localIncome = 0
        for book in bookings:
            if book.start_location == place.id:
                if book.paid == True:
                    localIncome = localIncome + Decimal(book.price)
        LIArray.append(str(place.name) + "  :  £" + str(localIncome))

    plt.clf()

    return render_template('income.html',
                           form=form,
                           loggedIn=loggedIn,
                           overallIncome=overallIncome,
                           LIArray=LIArray)


@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Checks if a bicycle is not booked at the specified location during the desired booking period
def checkAvailability(location, start_date, end_date):
    from app import db, models

    bicycles = models.Bike.query.filter_by(current_location=location)

    for bicycle in bicycles:
        booked = False
        bookings = models.Bike.query.get(bicycle.id).book

        for booking in bookings:
            if ((start_date - datetime.timedelta(days = 6)) <= booking.start_time.date() <= end_date) and (start_date <= booking.end_time.date() <= (end_date + datetime.timedelta(days = 6))):
                booked = True
                break

        if booked == False:
            return bicycle.id

    return -1

def displayAvailability(start_date, end_date):
    from app import db, models

    bicycles = models.Bike.query.all()
    availableBikes = []

    for bicycle in bicycles:
        booked = False
        availableBikes.append(bicycle)
        #where there is a booking with the specific bike id
        bookings = models.Bike.query.get(bicycle.id).book

        for booking in bookings:
            if ((start_date - datetime.timedelta(days = 6)) <= booking.start_time.date() <= end_date) and (start_date <= booking.end_time.date() <= (end_date + datetime.timedelta(days = 6))):
                if availableBikes != []:
                    booked = True
                    availableBikes.remove(bicycle)

    return availableBikes


# Adds a booking to the database
def makeBooking(bike_id, start_date, end_date, start_location, price, paid):
    from app import db, models

    try:
        newBooking = models.Booking(bike_id=bike_id, start_time=start_date, end_time=end_date, start_location=start_location, user_id=session['sessionid'], price=price, paid=paid)
    except:
        newBooking = models.Booking(bike_id=bike_id, start_time=start_date, end_time=end_date, start_location=start_location, price=price, paid=paid)

    db.session.add(newBooking)
    db.session.commit()
    return newBooking.id

# Gets the location name
def getLocation(location):
    from app import db, models

    locationName = models.Location.query.get(location).name

    return locationName

# Checks if an account is logged in
def isLoggedIn():
    if 'sessionid' in session:
        from app import db, models

        return models.Account.query.get(session['sessionid']).account_type
    else:
        return 0

# Sends an email receipt to the client and generate a PDF copy
def sendEmail( subject, sender, recipients, booking_id, html_body ):
    from flask_mail import Message
    from app import mail

    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = html_body

    pdfFile = open("app/static/receipts/booking_" + booking_id + ".pdf", "w+b")

    # Converts HTML to PDF
    pisaStatus = pisa.CreatePDF(
            html_body,
            dest=pdfFile)

    pdfFile.close()
    mail.send(msg)

    return pisaStatus.err

# Hashes the supplied password
def hashPassword(password):
    salt = b'MuchSecure'
    bytePassword = bytes(password, 'utf-8')
    hashedPassword = hashlib.pbkdf2_hmac('sha256', bytePassword, salt, 100000)

    return hashedPassword

# Creates an account in the database
def addAccount( surname, firstname,username,password):
    from app import db, models

    newPassword = hashPassword(password)
    account = models.Account(surname=surname, username=username, firstname=firstname, password=newPassword, account_type=3)
    db.session.add(account)
    db.session.commit()

def loginCheckUser( username, password ):
    from app import db, models

    hashedPassword = hashPassword(password)

    for account in models.Account.query.all():
        if account.username == username and account.password == hashedPassword and account.account_type == 3:
            return True

    flash("Incorrect username or password has been provided. \nPlease try again.")

    return False

def loginCheckStaff( username, password ):
    from app import db, models

    hashedPassword = hashPassword(password)

    for account in models.Account.query.all():
        if account.username == username and account.password == hashedPassword and account.account_type != 3:
            return True

    flash("Incorrect username or password has been provided. \nPlease try again.")

    return False

def checkEmail( emailaddress ):
    from app import db, models

    for account in models.Account.query.all():
        if account.username == emailaddress:
            flash("An account with that email address already exists")
            return False

    return True

def validPassword( password ):
    passwordMinChar = 6
    if len(password) >= passwordMinChar:
        if any(char.isdigit() for char in password) and any(char.isupper() for char in password) and any(char.islower() for char in password):
            return True
        flash("Password must contain at least 1 uppercase, 1 lowercase and 1 number.")
    else:
        flash("Password is too short")
    return False

def getIdForSession( username, password ):
    from app import db,models

    hashedPassword = hashPassword(password)

    for account in models.Account.query.all():
        if account.username == username and account.password == hashedPassword:
            return account.id

    return False

def validEmailAddress( email ):
    from email.utils import parseaddr

    if ('@' in parseaddr(email)[1]) and ('.' in parseaddr(email)[1]) == True:
        return True
    else:
        return False

def findEndDate( startDate, duration ):
    date_1 = startDate
    end_date = date_1 + datetime.timedelta(days=(duration - 1))

    return end_date

# Adds card details to the database
def storeCardDetails( name, number, expire, cardType, address1, address2, city, postcode):
    from app import db, models

    if address2 == "":
        address2 = None

    if city == "":
        city = None

    cardExists = False

    for card in models.Card.query.all():
        if card.user_id == session['sessionid']:
            cardExists = True
            break

    if cardExists:
        card = models.Card.query.filter_by(user_id=session['sessionid']).first()
        card.cardholder_name = name
        card.card_type = cardType
        card.card_number = number
        card.card_expiry_date = expire
        card.card_address1 = address1
        card.card_postcode = postcode
        card.card_address2 = address2
        card.card_city = city
    else:
        card = models.Card(cardholder_name=name,
                           card_type=cardType,
                           card_number=number,
                           card_expiry_date=expire,
                           card_address1=address1,
                           card_postcode=postcode,
                           card_address2=address2,
                           card_city=city,
                           user_id=session['sessionid'])
        db.session.add(card)

    db.session.commit()
