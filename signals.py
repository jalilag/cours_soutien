from PyQt5.QtWidgets import QWidget,QLabel,QInputDialog,QFileDialog
from PyQt5.QtGui import QPixmap,QTransform
from PyQt5.QtCore import Qt,pyqtSignal
from functools import partial
import time
import os
from pynput.mouse import Listener
import pynput.mouse as pymouse
import pynput.keyboard as pykeyboard

class Signals:
	def sig_change(self,field,func):
		grid = self.content_grid
		w = self.content_grid.get_widget_by_name(field)
		if w is not None: 
			func(w.currentData())

	def sig_create(self,table_name,field_id,func=None):
		grid = self.content_grid
		cols = self.bdd.cols_info(table_name)
		data = dict()
		for i in cols:
			val = grid.get_widget_by_name(i["name"])
			if val is not None:
				if i["name"] == field_id and not val.txt(): continue  
				data[i["name"]] = val.txt()
		if self.error_manage(self.bdd.check_values(table_name,data)): return
		print(data)
		if field_id in data:
			self.bdd.update(table_name,list(data.keys()),list(data.values()),field_id+"="+data[field_id]) 
		else:
			self.bdd.insert(table_name,list(data.keys()),list(data.values())) 
		if func: func()

	def sig_del_field(self,table_name,where,callback = None):
		self.bdd.delete(table_name,where)
		self.tools_callback(callback)

	def sig_price_change(self):
		grid = self.content_grid
		price_30 = grid.get_widget_by_name("price_30").isChecked()
		discount = grid.get_widget_by_name("discount").txt()
		lesson_id = grid.get_widget_by_name("lesson_id").txt()
		price = self.bdd.request("SELECT price_15,price_30 FROM lessons WHERE lesson_id="+str(lesson_id),True)[0][price_30]
		try:
			discount = float(discount)
		except:
			discount = 0
		price -= discount
		grid.get_widget_by_name("total_price").setText(str(price))

	def sig_add_user(self,subgrid):
		grid = self.content_grid
		user_id = grid.get_widget_by_name("user_id").currentData()
		if subgrid.get_widget_by_name(user_id) is not None: return
		user_name = self.bdd.request("SELECT printf('%s %s',firstname,lastname) as name FROM users WHERE user_id="+str(user_id),True)[0][0]
		w = self.u.UQwidget(name_id=str(user_id))
		subgrid.addWidget(w)
		horgrid = self.u.UQhboxlayout()
		w.setLayout(horgrid)
		horgrid.addWidget(self.u.UQtxt(style="field",title=user_name))
		horgrid.addWidget(self.u.UQbut("BUT_DEL",connect2=['clicked',partial(self.tools_remove_item,subgrid,None,None,user_id)]))
