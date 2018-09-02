import sys
from PyQt5.QtWidgets import QApplication
from qt_app import qt_app

application = QApplication(sys.argv)
appBuild = qt_app(application)
application.exec_()