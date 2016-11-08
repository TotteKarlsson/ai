#-------------------------------------------------------------------------------
# Name:        atdb
# Purpose:     The atdb class is a thin api for
#               retrieving and populating data in the atdb database
#-------------------------------------------------------------------------------

import mysql.connector
from PyQt4 import QtCore, QtGui, uic


class atdb:
    def __init__(self, _server_ip='', _database='atdb'):
        ''' Constructor for atdb. '''
        self.IP = _server_ip
        self.database = _database

        #Connect if given an ip
        if len(_server_ip):
            self.cnx = mysql.connector.connect(user='atdb_client', password='atdb123', host=self.IP, database=self.database)

    def connect(self, ip='', _database=''):
        if len(ip):
            self.IP = ip

        self.cnx = mysql.connector.connect(user='atdb_client', password='atdb123', host=self.IP, database=_database)

    def disconnect(self):
        self.cnx.disconnect()

    def getListOfCoverSlips(self):
        cursor = self.cnx.cursor()
        q = "SELECT id, status FROM coverslip ORDER by id DESC"
        cursor.execute(q)
        rows = cursor.fetchall()
        return rows

    def listCoverSlips(self):
        rows = self.getListOfCoverSlips()
        for row in rows:
            print str(row[0]) + ',' + str(row[1])

    def insertCoverSlipAssayData(self, data = []):
        q = (   "INSERT INTO coverslipdustassays"
                    "(coverslip_id, background_image, coverslip_image, result_image, coverslip_status)"
                "VALUES "
                    "(%s, %s, %s, %s, %s)")

        cursor = self.cnx.cursor()
        cursor.execute(q, data)
        newID = cursor.lastrowid
        print 'Inserted assay: ' + `newID`
        self.cnx.commit()
        cursor.close()
        return newID


def showMessageDialog(message):
   msg = QtGui.QMessageBox()
   msg.setIcon(QtGui.QMessageBox.Warning)
   msg.setText(message)
   msg.setWindowTitle("Message to you")
   msg.setStandardButtons(QtGui.QMessageBox.Ok)
   #msg.buttonClicked.connect(self.msgbtn)
   retval = msg.exec_()
   print "value of pressed message box button:", retval

def msgbtn(i):
    print "Button pressed is:",i.text()

