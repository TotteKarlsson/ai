# Import classes from your brand new package
import mysql.connector
from pyat import atdb

try:
    db = atdb()

    db.connect('127.0.0.1')

    db.listCoverSlips()

    db.disconnect()

    db.listCoverSlips()

except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))



