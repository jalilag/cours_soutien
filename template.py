import py_lib.user_qt as u
from PyQt5.QtWidgets import QWidget,QSizePolicy,QCheckBox,QScrollArea,QLabel,QPushButton,QFrame,QLabel,QDesktopWidget,QGraphicsColorizeEffect
from PyQt5.QtCore import Qt,pyqtSignal,QPropertyAnimation,QRect
from PyQt5.QtGui import QPixmap,QPainter,QPen,QColor


class Template:
	def template_create_menu_grid(self,app_target):
		menu_grid = self.u.UQvboxlayout()
		menuGridWidget = self.u.UQframebox(style="stdBox menuBox",parent=app_target)
		menuGridWidget.setLayout(menu_grid)
		print(type(menuGridWidget))
		return menu_grid

	def template_create_content_grid(self,app_target):
		content_grid = self.u.UQgridlayout()
		# content_grid = self.u.UQvboxlayout()
		mainGridWidget = self.u.UQframebox(style="stdBox mainBox",parent=app_target)
		mainGridWidget.setLayout(content_grid)
		return content_grid

	def template_create_parent_scroll_area(self,app_target,main_grid,resizable=True,min_width=1300,min_height=500):
		l = QWidget()
		l.setLayout(main_grid)
		parent_area = QScrollArea()
		parent_area.setWidget(l)
		parent_area.setWidgetResizable(True)
		parent_area.setMinimumSize(min_width,min_height)
		app_target.setCentralWidget(parent_area)
		return parent_area