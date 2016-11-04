import os
import sys
import pyqtgraph as pg
import numpy as np
import MMCorePy
from PyQt4 import QtCore, QtGui, uic
from pyat import atdb

import glob
from datetime import datetime

#Some parameters
gDustAssayImagesRoot = 'x:\ATDB\images\dustassay'
gATDBIP = '127.0.0.1'
gMMConfigFile = 'P:\\ais\\micromanager\\ThorLabCameraOnly.cfg'

class MyWidget(QtGui.QWidget):
    def __init__(self,configfile=''):
        QtGui.QWidget.__init__(self)
        self.initUI()
        self.pushButton1.clicked.connect(self.dopush1)
        self.pushButton2.clicked.connect(self.dopush2)
        self.PopulateBtn.clicked.connect(self.saveBtnClick)

        self.mmc = MMCorePy.CMMCore()
        print self.mmc.getVersionInfo()
        self.mmc.loadSystemConfiguration(configfile)
        #self.mmc.setProperty('Camera', 'PixelType', '32bitRGB')  # Change pixel type
        self.dustAssayImagesRoot = gDustAssayImagesRoot

        #Connect to the database
        self.db = atdb(gATDBIP)
        self.csIDList.itemClicked.connect(self.Clicked)
        self.populateUI()

    def initUI(self):
        currpath=os.path.split(os.path.realpath(__file__))[0]
        filename = os.path.join(currpath,'csDustAssayUI.ui')
        uic.loadUi(filename,self)

        self.img1 = self.setupImageWidget(self.image1)
        self.img2 = self.setupImageWidget(self.image2)
        self.img3 = self.setupImageWidget(self.image3)

    def setupImageWidget(self, imageWidget = []):
        imageItem  = pg.ImageItem()
        p = imageWidget.addPlot()
        p.hideAxis('left')
        p.hideAxis('bottom')
        p.addItem(imageItem)
        return imageItem

    def populateUI(self):
        #Load coverslips into listbox
        coverslips = self.db.getListOfCoverSlips()
        for coverslip in coverslips:
            self.csIDList.addItem(str(coverslip[0]) + ',' + str(coverslip[1]))

        #Select last coverslip
        if self.csIDList.count() > 0:
            self.csIDList.item(0).setSelected(True);

    def populateDB(self, fName1, fName2, fName3):
        dbData = []
        csID = self.csIDList.currentItem().text()

        #CoverSlip ID
        dbData.append(str(csID[0]))

        #Assay data
        dbData.append(fName1)
        dbData.append(fName2)
        dbData.append(fName3)

        #CoverSlip status
        dbData.append(str(csID[2]))

        try:
            self.db.insertCoverSlipAssayData(dbData)
        except mysql.connector.Error as err:
            print("Something went wrong with the DB: {}".format(err))

    def Clicked(self,item):
            print "Current coverslip ID: " + item.text()

    #Pressing buttons..
    def dopush1(self):
        self.mmc.snapImage()
        data = np.rot90(self.mmc.getImage(), 3)
        self.img1.setImage(data, autoLevels=False)

    def dopush2(self):
        self.mmc.snapImage()
        data = np.rot90(self.mmc.getImage(), 3)
        self.img2.setImage(data, autoLevels=False)

        #Do the subtraction
        result = self.img2.image.astype(float) - self.img1.image.astype(float)
        #np.clip(result, 0, [0,25], out=result)
        self.img3.setImage(result, autoLevels=False)

    def saveBtnClick(self):
        print "Populate DB and save files"
        f1 = self.saveImage(self.img1)
        f2 = self.saveImage(self.img2)
        f3 = self.saveImage(self.img3)
        self.populateDB(f1, f2, f3)

    def saveImage(self, image=[]):
        #Setup filenames
        todaysDate = datetime.now().strftime('%Y-%m-%d')
        file_count  = len(glob.glob1(self.dustAssayImagesRoot, todaysDate + "*"))

        fName = todaysDate + '_' + `file_count + 1` + '.jpg'
        fNameWPath = os.path.join(self.dustAssayImagesRoot, fName)

        #Rotate image to "normal" before saving
        image.setImage(np.rot90(image.image, 2), autoLevels=False)

        print "Saving:" + `fNameWPath`
        image.save(fNameWPath)

        #Rotate back for UI
        image.setImage(np.rot90(image.image, 2), autoLevels=False)
        return fName

    def run(self):
        self.show()
        qtapp.exec_()

if __name__ == '__main__':
    qtapp = QtGui.QApplication(sys.argv)
    configfile= gMMConfigFile
    app = MyWidget(configfile)
    qtapp.setWindowIcon(QtGui.QIcon('icons/csDustAssayApp.ico'))

    app.run()
