from PyQt4 import QtCore, QtGui, uic

def main():
    pass

if __name__ == '__main__':
    main()

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
