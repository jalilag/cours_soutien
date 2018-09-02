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
	
	def sig_change(self,table_name,field,func):
		grid = self.content_grid
		w = self.content_grid.get_widget_by_name(field)
		if w is not None: 
			s = w.currentData()
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
