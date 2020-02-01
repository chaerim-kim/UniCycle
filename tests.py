import os
import unittest
from app import db, models
import datetime
from decimal import *
# from views import makeBooking

def validPassword( password ):
    if len(password) >= 6:
        if any(char.isdigit() for char in password) and any(char.isupper() for char in password) and any(char.islower() for char in password):
            return True
    return False

def validEmailAddress( email ):
    from email.utils import parseaddr
    if ('@' in parseaddr(email)[1]) and ('.' in parseaddr(email)[1]) == True:
        return True
    else:
        return False

#function to test bike location page
def editBikeID( bike_id ):
    bike = models.Bike(id=50, current_location=1)
    db.session.add(bike)
    bike = models.Bike.query.get(50)
    bike.id = bike_id
    db.session.add(bike)

    p = models.Bike.query.get(int(bike_id))

    if p.id == int(bike_id):
        return True
    else:
        return False

def editBikeLocation(location):
    bike = models.Bike(id=85, current_location=1)
    db.session.add(bike)
    bike = models.Bike.query.get(85)
    bike.current_location = int(location)
    db.session.add(bike)

    if bike.current_location == int(location):
        return True
    else:
        return False

def registerAccount(surname, username, firstName, password ): #fails if database does not have surname
    user = models.Account(surname=surname, username=username, firstname=firstName, password=password, account_type=3)
    for account in models.Account.query.all():
        if account.username == username:
            return False
        else:
            db.session.add(user)
            return True

def login(username, password):
    user = models.Account(surname="test1", username="abc@yahoo.co.in", firstname="test", password="Pass2345", account_type=3)
    db.session.add(user)

    for account in models.Account.query.all():
        if account.username == username and account.password == password:
            return True
    return False

def makeBooking(bike_id, start_time, start_location):
    try:
        newBooking = models.Booking(bike_id=bike_id, start_time=start_time, start_location=start_location)
        db.session.add(newBooking)
        return True
    except:
        return False

def price(priceTest, hirePeriod):
    daysRented = hirePeriod
    rate = 2.50
    priceCalculated = 0
    dayCount = daysRented

    while dayCount != 0:
        priceCalculated += rate
        rate -= 0.1
        dayCount -= 1

    priceCalculated = round(Decimal(priceCalculated), 2)
    priceTest = round(Decimal(priceTest), 2)

    if priceCalculated == priceTest:
        return True
    else:
        return False

def cardDetails(cardholder_name, card_type, card_number, card_expiry_date, card_address1, card_postcode, card_address2, card_city):
    try:
        card = models.Card(cardholder_name=cardholder_name, card_type=card_type, card_number=card_number, card_expiry_date=card_expiry_date, card_address1=card_address1, card_postcode=card_postcode, card_address2=card_address2, card_city=card_city)
        db.session.add(card)
        return True
    except:
        return False

def addBike(location):
    try:
        newBike = models.Bike(current_location=location)
        db.session.add(newBike)
        return True
    except:
        return False

def addLocation(name, address):

    newLocation = models.Location(name=name, address=address)
    db.session.add(newLocation)

    for location in models.Location.query.all():
        if location.name == name and location.address == address:
            return False
        else:
            return True
################################################################################
class AddLocation(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        db.session.rollback()
        pass

    def test_addLocation_successfully(self):
        assert addLocation('Hyde Park', 'Round the Corner') == True


    def test_addLocation_unsuccessfully(self):
        assert addLocation('University', 'Roger Stevens') == False

class AddBike(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        db.session.rollback()
        pass

    def test_addBike_successfully_1(self):
        assert addBike(1) == True

    def test_addBike_successfully_2(self):
        assert addBike(2) == True

    def test_addBike_successfully_3(self):
        assert addBike(3) == True


class CardDetails(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        db.session.rollback()
        pass

    def test_card_correct(self):
        assert cardDetails("S Smith", 1, 1234123412341234, datetime.datetime(2019,9,8,12,0), "91 Clovelly Rd", "2193", "Greenside", "Johannesburg") == True

    def test_card_no_address2(self):
        assert cardDetails("S Smith", 1, 1234123412341234, datetime.datetime(2019,9,8,12,0), "91 Clovelly Rd", "2193", None, "Johannesburg") == True

    def test_card_no_city(self):
        assert cardDetails("S Smith", 1, 1234123412341234, datetime.datetime(2019,9,8,12,0), "91 Clovelly Rd", "2193", "Greenside", None) == True

    def test_card_no_city_no_add2(self):
        assert cardDetails("S Smith", 1, 1234123412341234, datetime.datetime(2019,9,8,12,0), "91 Clovelly Rd", "2193", None, None) == True

class Price(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        db.session.rollback()
        pass

    def test_price_1day(self):
        assert price(2.50, 1) == True

    def test_price_1day_incorrect(self):
        assert price(2.00, 1) == False

    def test_price_2days(self):
        assert price(4.90, 2) == True

    def test_price_2days_incorrect(self):
        assert price(2.00, 2) == False

    def test_price_7days(self):
        assert price(15.40, 7) == True

    def test_price_7days_incorrect(self):
        assert price(2.00, 7) == False


class MakeBooking(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        db.session.rollback()
        pass

    def test_booking_correct(self):
        assert makeBooking(1,datetime.datetime(2018,1,1,12,0),1) == True

class RegisterAccount(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        db.session.rollback()
        pass

    def test_register_correctly(self):
        assert registerAccount("testSurname", "test@gmail.com", "testFirstname", "Rainbow123") == True

class Login(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        db.session.rollback()
        pass

    def test_login_correctly(self):
        assert login("abc@yahoo.co.in", "Pass2345") == True

    def test_login_incorrect_password(self):
        assert login("abc@yahoo.co.in", "wrong1234pass") == False

    def test_login_incorrect_email(self):
        assert login("def@yahoo.co.in", "Pass2345") == False

class EditBikeID(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        db.session.rollback()
        pass

    def test_edit_id(self):
        assert editBikeID("99") == True

class EditBikeLocation(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        db.session.rollback()
        pass

    def test_edit_location(self):
        assert editBikeLocation("2") == True

class ValidEmailAddress(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        db.session.rollback()
        pass

    def test_valid_email(self):
        assert validEmailAddress("test@yahoo.com") == True

    def test_valid_email1(self):
        assert validEmailAddress("test@yahoo.co.uk") == True

    def test_valid_email_invalid(self):
        assert validEmailAddress("notanemail-google.com") == False

    def test_valid_email_invalid1(self):
        assert validEmailAddress("notanemail@@google.com") == False

    def test_valid_email_invalid2(self):
        assert validEmailAddress("") == False


class ValidPassword(unittest.TestCase): #need to test again when models is complete
    def setUp(self):
        pass

    def tearDown(self):
        db.session.rollback()
        pass

    def test_password_correct(self):
        assert validPassword( "Abcde1" ) == True

    def test_password_incorrect_length(self):
        assert validPassword( "Abcd1" ) == False

    def test_password_incorrect_upper(self):
        assert validPassword( "abcde1" ) == False

    def test_password_incorrect_lower(self):
        assert validPassword( "ABCDE1" ) == False

    def test_password_incorrect_number(self):
        assert validPassword( "Abcdef" ) == False


if __name__ == '__main__':
    unittest.main()
# hello@gmail.com
# Hiya123
