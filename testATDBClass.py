# Import classes from your brand new package
import mysql.connector
from pyat import atdb

try:
    db = atdb()

    db.connect('127.0.0.1', 'atdb_demo')

    db.listCoverSlips()

    db.disconnect()

    #Generate an exception
    db.listCoverSlips()

except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))



