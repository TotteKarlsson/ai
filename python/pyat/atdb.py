#-------------------------------------------------------------------------------
# Name:        atdb
# Purpose:     The atdb class is a thin api for
#               retrieving and populating data in the atdb database
#-------------------------------------------------------------------------------

import mysql.connector

class atdb:
    def __init__(self, server_ip=''):
        ''' Constructor for atdb. '''
        self.IP = server_ip

        #Connect if given an ip
        if len(server_ip):
            self.cnx = mysql.connector.connect(user='atdb_client', password='atdb123', host=self.IP, database='atdb')

    def connect(self, ip=''):
        if len(ip):
            self.IP = ip

        self.cnx = mysql.connector.connect(user='atdb_client', password='atdb123', host=self.IP, database='atdb')

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


