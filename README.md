# TRacker
Tracks the date,time and the time elapsed.
converts the time elapsed to units (time elapsed/60)
creates and saves the data to sqlite database
another feature is to pull out (export) the data to a csv file.


#For PyInstaller .exe file logo you need to create .qrc file using pyrcc5 i/o then convert it to python file (.py)
then rewrite the code for self.setWindowIcon(QtGui.QIcon(':/img/image1.png')) using the :/path/to/your/image file
pre-req: pywin32 pyinstaller and .ico file for the logo/icon of the file

