from PyQt4 import QtCore, QtGui, uic
import os
import sys
import pyqtgraph as pg
import numpy as np
import MMCorePy
import mysql.connector
import glob
from datetime import datetime

class MyWidget(QtGui.QWidget):
    def __init__(self,configfile=''):
        QtGui.QWidget.__init__(self)
        self.initUI()
        self.pushButton1.clicked.connect(self.dopush1)
        self.pushButton2.clicked.connect(self.dopush2)
        self.PopulateBtn.clicked.connect(self.saveBtnClick)
        self.mmc = MMCorePy.CMMCore()
        self.mmc.loadSystemConfiguration(configfile)
        self.dustAssayImagesRoot = 'x:\ATDB\images\dustassay'
        self.cnx = mysql.connector.connect(user='atdb_client', password='atdb123', host='127.0.0.1', database='atdb')
        self.csIDList.itemClicked.connect(self.Clicked)
        self.populateUI()

    def initUI(self):
        currpath=os.path.split(os.path.realpath(__file__))[0]
        filename = os.path.join(currpath,'csDustAssayUI.ui')
        uic.loadUi(filename,self)

        self.img1 = pg.ImageItem()

        self.p1 = self.image1.addPlot()
        self.p1.hideAxis('left')
        self.p1.hideAxis('bottom')
        self.p1.addItem(self.img1)

        self.img2 = pg.ImageItem()
        self.p2 = self.image2.addPlot()
        self.p2.hideAxis('left')
        self.p2.hideAxis('bottom')
        self.p2.addItem(self.img2)

        self.img3 = pg.ImageItem()
        self.p3 = self.image3.addPlot()
        self.p3.hideAxis('left')
        self.p3.hideAxis('bottom')
        self.p3.addItem(self.img3)

    def Clicked(self,item):
        print "Current coverslip ID: " + item.text()

    def populateUI(self):
        self.loadCoverSlipIDS()

    def loadCoverSlipIDS(self):
        cursor = self.cnx.cursor()
        q = "SELECT id, status FROM coverslip ORDER by id"
        cursor.execute(q)
        rows = cursor.fetchall()
        for row in rows:
            self.csIDList.addItem(str(row[0]) + ',' + str(row[1]))

    def populateDB(self):
        dustAssay = ("INSERT INTO coverslipdustassays"
                    "(coverslip_id, background_image, coverslip_image, result_image, coverslip_status)"
                    "VALUES (%s, %s, %s, %s, %s)")
        dbData = []
        csID = self.csIDList.currentItem().text()
        dbData.append(str(csID[0]))
        dbData.append(self.img1FileName)
        dbData.append(self.img2FileName)
        dbData.append(self.img3FileName)
        dbData.append(str(csID[2]))

        try:
            cursor = self.cnx.cursor()
            cursor.execute(dustAssay, dbData)
            newID = cursor.lastrowid
            print 'Inserted assay: ' + `newID`
            self.cnx.commit()
            cursor.close()

        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))


    def dopush1(self):
        print "hello"
        self.mmc.snapImage()
        data = np.rot90(self.mmc.getImage(), 3)
        self.img1.setImage(data, autoLevels=False)
        self.img1FileName = datetime.now().strftime('%Y-%m-%d')

    def dopush2(self):
        print "hello 22"
        self.mmc.snapImage()
        data = np.rot90(self.mmc.getImage(), 3)
        self.img2.setImage(data, autoLevels=False)
        self.img2FileName = datetime.now().strftime('%Y-%m-%d')

        #Do the subtraction
        result = self.img2.image.astype(float) - self.img1.image.astype(float)
        #np.clip(result, 0, [0,25], out=result)
        self.img3.setImage( result, autoLevels=False)
        self.img3FileName = datetime.now().strftime('%Y-%m-%d')


    def saveBtnClick(self):

        print "Populate DB and save files"
        print os.path.join(self.dustAssayImagesRoot, self.img1FileName)

        todaysDate = datetime.now().strftime('%Y-%m-%d')
        file_count  = len(glob.glob1(self.dustAssayImagesRoot, todaysDate + "*"))

        self.img1FileName = self.img1FileName + '_' + `file_count + 1` + '.jpg'
        self.img2FileName = self.img2FileName + '_' + `file_count + 2` + '.jpg'
        self.img3FileName = self.img3FileName + '_' + `file_count + 3` + '.jpg'

        img1FName = os.path.join(self.dustAssayImagesRoot, self.img1FileName)
        img2FName = os.path.join(self.dustAssayImagesRoot, self.img2FileName)
        img3FName = os.path.join(self.dustAssayImagesRoot, self.img3FileName)

        self.img1.save(img1FName)
        self.img2.save(img2FName)
        self.img3.save(img3FName)
        self.populateDB()

    def run(self):
        self.show()
        qtapp.exec_()

if __name__ == '__main__':

    qtapp = QtGui.QApplication(sys.argv)
    configfile= 'P:\\QtDemo\\ThorLabCameraOnly.cfg'
    app = MyWidget(configfile)

    qtapp.setWindowIcon(QtGui.QIcon('icons/csDustAssayApp.ico'))
    #mainwindow.setWindowIcon(QtGui.QIcon('chalk.ico'))

    app.run()
