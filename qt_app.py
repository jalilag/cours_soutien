import sys
from functools import partial
import py_lib.user_qt as u
from PyQt5.QtWidgets import QWidget,QSizePolicy,QCheckBox,QScrollArea,QLabel,QPushButton,QFrame,QLabel,QDesktopWidget,QGraphicsColorizeEffect
from PyQt5.QtCore import Qt,pyqtSignal,QPropertyAnimation,QRect
from PyQt5.QtGui import QPixmap,QPainter,QPen,QColor
import time
import sqlite3 as sql
from py_lib.user_sqlite import Usql
from public.lang import txt
from public.app_style import sty
from public.design import Design
import public.error as error
from tools import Tools
from template import Template
from views import Views
from signals import Signals
from processing import Processing
from error import Error
from check import Check
u.utxt = txt
u.usty = sty
u.ulang = "fr"

class qt_app(Template,Design,Tools,Views,Signals,Processing,Error,Check):
	u = u
	errors = error.err
	application = None
	app = None
	main_grid = None
	menu_grid = None
	content_grid = None
	parent_area = None
	current_file = None
	x = None
	y = None
	bdd_con = None
	bdd_curs = None
	def __init__(self,application):
		# self.load_lang()
		self.bdd_con = sql.connect('cours_soutien.db')
		self.bdd = Usql(self.bdd_con)
		self.bdd.activate_for_keys()
		self.application = application
		self.subapp = self.u.UQapp(title="Maria mode")
		self.subapp.style = "css"
		self.menu_grid = self.template_create_menu_grid(self.subapp)
		self.view_menu()
		self.content_grid = self.template_create_content_grid(self.subapp)
		# self.view_box_client_info()
		self.main_grid = self.u.UQhboxlayout()
		self.main_grid.addWidget(self.menu_grid.parentWidget(),0,Qt.AlignTop)
		self.main_grid.addStretch(1)
		self.main_grid.addWidget(self.content_grid.parentWidget(),0,Qt.AlignTop)
		self.main_grid.addStretch(1)
		self.parent_area = self.template_create_parent_scroll_area(self.subapp,self.main_grid)		
		self.subapp.center(0)
		self.subapp.showMaximized()
		self.subapp.show()
