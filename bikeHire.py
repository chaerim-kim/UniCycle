import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets,QtGui,QtCore

# from PyQt5 import QtSql, QtGui


# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

#
#
# class Database():
#     # def __init__(self):
#
#     def createDB():
#         db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
#         db.setDatabaseName('sports.db')
#
#         query= QtSql.QSqlQuery()
#         query.exec_("create table sportsmen(id int primary key,""firstname varchar(30), lastname varchar(30))")
#
#         query.exec_("insert into sportsmen values(101, 'Roger', 'Federer')")
#         query.exec_("insert into sportsmen values(102, 'Christiano', 'Ronaldo')")
#         query.exec_("insert into sportsmen values(103, 'Ussain', 'Bolt')")
#

class App(QTabWidget):

    def __init__(self):
        super().__init__()
        # self.setGeometrgit commandsy(50, 50, 500, 300)
        self.setWindowTitle("Bike Availability")
        # self.table_widget = CreateWidgets(self)

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.addTab(self.tab1,"Availability")
        self.addTab(self.tab2,"Hire Bike")
        self.addTab(self.tab3,"Payment")

        self.tab1UI()
        self.tab2UI()
        self.tab3UI()



    def tab1UI(self):
        # title widget
        titleLayout = QVBoxLayout()

        title = QLabel("Bike Availability by time")
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(16)
        title.setFont(font)

        moreInfo = QLabel("You can view bike availability in a specified range of time.\n")
        font2 = QtGui.QFont()
        font2.setPointSize(12)
        moreInfo.setFont(font2)

        titleLayout.addWidget(title)
        titleLayout.addWidget(moreInfo)


        # From widgets
        fromHLayout = QHBoxLayout()
        fromLabel = QLabel("From :")
        fromHour = QDoubleSpinBox()
        fromHour.setMinimum(1)
        fromHour.setMaximum(12)
        fromHour.setSingleStep(1)

        fromMin = QDoubleSpinBox()
        fromMin.setMinimum(0.00)
        fromMin.setMaximum(55.00)
        fromMin.setSingleStep(5.00)

        FromAmPm = QComboBox()
        FromAmPm.addItem("AM")
        FromAmPm.addItem("PM")

        fromHLayout.addWidget(fromLabel)
        fromHLayout.addWidget(fromHour)
        fromHLayout.addWidget(fromMin)
        fromHLayout.addWidget(FromAmPm)


        # To widgets
        toHLayout = QHBoxLayout()

        toLabel = QLabel("To :")
        toHour = QDoubleSpinBox()
        toHour.setMinimum(1)
        toHour.setMaximum(12)
        toHour.setSingleStep(1)

        toMin = QDoubleSpinBox()
        toMin.setMinimum(0.00)
        toMin.setMaximum(55.00)
        toMin.setSingleStep(5.00)

        toAmPm = QComboBox()
        toAmPm.addItem("AM")
        toAmPm.addItem("PM")

        toHLayout.addWidget(toLabel)
        toHLayout.addWidget(toHour)
        toHLayout.addWidget(toMin)
        toHLayout.addWidget(toAmPm)


        #buttons
        buttonLayout = QHBoxLayout();

        cancelButton = QPushButton("Cancel")
        cancelButton.clicked.connect(self.close)
        saveButton = QPushButton("View Availability")

        buttonLayout.addWidget(cancelButton)
        buttonLayout.addWidget(saveButton)


        # add layouts to main layout
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(titleLayout)
        mainLayout.addStretch()
                # mainlayout.addStretch()
        mainLayout.addLayout(fromHLayout)
        mainLayout.addLayout(toHLayout)
        mainLayout.addLayout(buttonLayout)

        # set and show
        self.tab1.setLayout(mainLayout)
        self.show()



    def tab2UI(self):

        #widgets
        label = QtWidgets.QLabel('Booking a Bike')
        #change font
        myFont = QtGui.QFont()
        myFont2 = QtGui.QFont()

        myFont.setBold(True)
        myFont.setPointSize(16)
        label.setFont(myFont)
        label2 = QtWidgets.QLabel('Select a Location, date and time to Hire a bike')
        myFont2.setPointSize(12)
        label2.setFont(myFont2)

        #label3 = QtWidgets.QLabel('Please Select Bike')
        #choosebike = QtWidgets.QComboBox()
        loclabel = QtWidgets.QLabel('Pick up Location')
        line = QLineEdit()
        datelabel = QtWidgets.QLabel('Date')
        timelabel = QtWidgets.QLabel('Time')


        cancelButton = QtWidgets.QPushButton('Cancel')
        cancelButton.clicked.connect(self.close)
        saveButton = QtWidgets.QPushButton('Save Booking')

        #self.dateEdit = QtGui.QDateEdit(self)
        #self.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        #self.dateEdit.setMaximumDate(QtCore.QDate(7999, 12, 28))
        #self.dateEdit.setMaximumTime(QtCore.QTime(23, 59, 59))
        #self.dateEdit.setCalendarPopup(True)

        #time and date widgets
        #time = QtWidgets.QTimeEdit()
        #date = QtWidgets.QDateEdit()
        datetime = QtWidgets.QDateEdit()
        datetime.setDateTime(QtCore.QDateTime.currentDateTime())
        datetime.setMinimumDate(QtCore.QDate(2019, 2, 16))
        datetime.setMaximumTime(QtCore.QTime(23, 59, 59))
        datetime.setCalendarPopup(True)
        time = QtWidgets.QTimeEdit()
        time.setTime(QtCore.QTime.currentTime())

        #qformlainitUIyout
        formlayout = QFormLayout()
        #formlayout.addRow(label3, choosebike)
        formlayout.addRow(loclabel, line)
        formlayout.addRow(datelabel, datetime)
        formlayout.addRow(timelabel, time)
        formlayout.addRow(cancelButton, saveButton)

        #tabs.addTab(tab1, "Tab 1")

        #mainlayout
        mainlayout = QVBoxLayout()
        #mainlayout.addWidget(tabs)
        mainlayout.addWidget(label)
        mainlayout.addWidget(label2)
        mainlayout.addStretch()
        # mainlayout.addStretch()
        mainlayout.addLayout(formlayout)

        self.tab2.setLayout(mainlayout)
        self.show()



    def tab3UI(self):


        #Title of tab
        headingLayout = QVBoxLayout()
        title = QLabel("Bike Hire Payment")
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(16)
        title.setFont(font)

        #Description of tab
        moreInfo = QLabel("Cash payment for your hired bike.\n")
        font2 = QtGui.QFont()
        font2.setPointSize(12)
        moreInfo.setFont(font2)
        #Heading layout
        headingLayout.addWidget(title)
        headingLayout.addWidget(moreInfo)


        #Widgets
        dueLayout = QHBoxLayout()
        labelAmount = QLabel("Total amount due:")
        lineEditAmount = QLineEdit("£    ")
        lineEditAmount.setReadOnly(True)
        dueLayout.addWidget(labelAmount)
        dueLayout.addWidget(lineEditAmount)

        receivedLayout = QHBoxLayout()
        label = QLabel("Total amount received:")
        lineEditReceived = QLineEdit("£ ")
        button = QPushButton("Enter")
        receivedLayout.addWidget(label)
        receivedLayout.addWidget(lineEditReceived)
        receivedLayout.addWidget(button)

        changeLayout = QHBoxLayout()
        labelChange = QLabel("Total change due:")
        lineEditChange = QLineEdit("£    ")
        lineEditChange.setReadOnly(True)
        changeLayout.addWidget(labelChange)
        changeLayout.addWidget(lineEditChange)

        #adding all layouts to a main layout
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(headingLayout)
        mainLayout.addStretch()
        mainLayout.addLayout(dueLayout)
        mainLayout.addLayout(receivedLayout)
        mainLayout.addLayout(changeLayout)
        self.tab3.setLayout(mainLayout)
        self.show()







if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
