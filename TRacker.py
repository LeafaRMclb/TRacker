import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sqlite3
import time
import datetime
from pandas import read_sql


s = 0
m = 0
h = 0

class Clock(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("TRacker")
        self.setWindowIcon(QIcon("gnome_panel_clock.png"))
        self.resize(280, 170)

        centralwidget = QWidget(self)

        self.lcd = QLCDNumber(self)

        # credits1 = QLabel("Economics Manila", self)
        # credits1.move(210, 135)

        self.timer = QTimer(self)   
        self.timer.timeout.connect(self.timeOut)        

        self.btn_start = QPushButton("Start", self)
        self.btn_start.clicked.connect(self.start)

        self.btn_stop = QPushButton("Stop", self)
        self.btn_stop.clicked.connect(lambda: self.timer.stop())

        self.btn_reset = QPushButton("Reset", self)
        self.btn_reset.clicked.connect(self.reset)

        self.btn_save = QPushButton("Save", self)
        self.btn_save.clicked.connect(self.timeElapsed)

        self.btn_export = QPushButton("Export", self)
        self.btn_export.clicked.connect(self.exportData)

        # self.btn_retrieve = QPushButton("Retrieve", self)
        # self.btn_retrieve.clicked.connect(self.retrieve)



        grid = QGridLayout()

        grid.addWidget(self.btn_start, 1, 0)
        grid.addWidget(self.btn_stop, 1, 1)
        grid.addWidget(self.btn_reset, 1, 3)
        grid.addWidget(self.btn_save, 1, 2)
        grid.addWidget(self.btn_export, 4, 0)
        # grid.addWidget(self.btn_retrieve, 4, 1)
        grid.addWidget(self.lcd, 2, 0, 1, 4)

        centralwidget.setLayout(grid)

        self.setCentralWidget(centralwidget)

        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def reset(self):
        global s, m, h

        self.timer.stop()

        s = 0
        m = 0
        h = 0

        time = "{0}:{1}:{2}".format(h, m, s)

        self.lcd.setDigitCount(len(time))
        self.lcd.display(time)

    def start(self):
        global s, m, h
        global start
        global now
        global hms
        global dateNow
        
        # global taskName
        hms = time.strftime("%H:%M")
        start = time.time()
        self.timer.start(1000)        
        self.getTaskName()
        
        now = datetime.datetime.now()
        dateNow = now.strftime("%Y-%m-%d")
        QMessageBox.information(self, 'Message', "Tracker started: %s" % (now.strftime("%Y-%m-%d %H:%M")))
        
    def timeOut(self):
        global s, m, h
        
        if s < 59:
            s += 1
        else:
            if m < 59:
                s = 0
                m += 1
            elif m == 59 and h < 24:
                h += 1
                m = 0
                s = 0
            else:
                self.timer.stop()

        self.time = "{0}:{1}:{2}".format(h, m, s)

        self.lcd.setDigitCount(len(self.time))
        self.lcd.display(self.time)

    def timeElapsed(self):
        global stop
        global minutes
        global unit
        global stophms

        stophms = time.strftime("%H:%M")
        dateNow = datetime.datetime.now()
        QMessageBox.information(self, 'Message', "Tracker ended: "+ dateNow.strftime("%Y-%m-%d %H:%M"))
        stop = time.time()
        minutes = (start - stop) / 60
        minutes = ("%.2f" % minutes)
        minutes = abs(float(minutes))                 
        unit = minutes / 60
        unit = ("%.2f" % unit)
        unit = abs(float(unit))
        QMessageBox.information(self, 'Message', "Time elapsed: %.2f minutes \n Units earned: %.2f " % (abs(minutes), abs(unit)))        
        # print(self.time, len(self.time))
        return saveTime(self.time)

    def exportData(self):
        con = sqlite3.connect('database.db')
        table = read_sql('SELECT * FROM data', con)
        table.to_csv('output.csv')
        QMessageBox.information(self, 'Message','Output created on directory!')

    
    # def retrieve(self):
    #     conn = sqlite3.connect("database.db")
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT * FROM data")
    #     # t1 = cursor.fetchone()
    #     # print(t1[0])
    #     allRows= cursor.fetchall()
    #     for row in allRows:
    #         print("{}, {}, {}, {}, {}, {}".format(row[0],row[1],row[2],row[3],row[4], row[5]))
            
            
        

    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def getTaskName(self):
        global taskName

        taskName, okPressed = QInputDialog.getText(self, "Message","Task name:", QLineEdit.Normal, "")
        if okPressed and taskName != '':
            QMessageBox.information(self, 'Message', "Task name: %s" % taskName)
        else:
            self.getTaskName()

    # def drop(self):
    #     conn = sqlite3.connect("database.db")
    #     cursor = conn.cursor()
    #     cursor.execute("DROP TABLE data")
    #     conn.commit()
        

def saveTime(*args):
    conn = sqlite3.connect("database.db")
    conn.text_factory = str
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS data (Calendar TEXT, Start TEXT, Stop TEXT, Elapsed INTEGER, Units INTEGER, Task TEXT)")
    # cursor.execute("INSERT INTO data VALUES (?)", args)
    cursor.execute("INSERT INTO data(Calendar,Start,Stop,Elapsed,Units,Task) VALUES (?,?,?,?,?,?)", (dateNow, hms, stophms, minutes, unit, taskName))
    conn.commit()
    conn.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Clock()
    sys.exit(app.exec_())
