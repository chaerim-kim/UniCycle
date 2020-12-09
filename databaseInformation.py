import os
from app import db,models
import datetime

# Delete database file if it exists currently
if os.path.exists('app.db'):
    os.remove('app.db')

db.create_all()

l1 = models.Location(name='University', address='Roger Stevens')
b1 = models.Bike(current_location=1)
l2 = models.Location(name='City', address='Headrow')
b2 = models.Bike(current_location=2)
l3 = models.Location(name='Headingley', address='Otley Road')
b3 = models.Bike(current_location=3)
b4 = models.Bike(current_location=1)
b5 = models.Bike(current_location=1)
b6 = models.Bike(current_location=2)
b7 = models.Bike(current_location=2)
b8 = models.Bike(current_location=3)
b9 = models.Bike(current_location=3)


# adminuser = models.Account(surname="adSur", username="admin", firstname="adFir", password="Password01", account_type=1)
# staffuser = models.Account(surname="staffSur", username="staff", firstname="staffFir", password="Password01", account_type=2)


db.session.add(l1)
db.session.add(b1)
db.session.add(l2)
db.session.add(b2)
db.session.add(l3)
db.session.add(b3)
db.session.add(b4)
db.session.add(b5)
db.session.add(b6)
db.session.add(b7)
db.session.add(b8)
db.session.add(b9)
# db.session.add(adminuser)
# db.session.add(staffuser)

db.session.commit()
