import pynput.mouse as pymouse
import pynput.keyboard as pykeyboard

class Tools:
	def tools_load_view(self,menu_id,content_id):
		self.menu_view = menu_id
		self.content_view = content_id

	def tools_remove_items(self,layout):
		if layout is not None:
		    for cnt in reversed(range(layout.count())):
		        w = layout.takeAt(cnt).widget()
		        if w is not None:
		            w.deleteLater()

	def tools_remove_item(self,layGrid=None,line=None,col=None,widname=None):
		"""
			Suppression d'élément
		"""
		if widname is not None:
			wid = layGrid.get_child_by_name(widname)
			if wid is not None: wid.deleteLater()
			if layGrid.get_child_by_name(widname) is not None:
				wid.setParent(None)
		else:
			if layGrid.get_widget_by_pos(line,col) is not None:
				layGrid.get_widget_by_pos(line,col).deleteLater()
			if layGrid.get_widget_by_pos(line,col) is not None:
				layGrid.get_widget_by_pos(line,col).setParent(None)

	def tools_load_lang(self):
		bdd_lang = self.bdd.select("Configuration","val",u_where="name='LANG_CHOOSE'")[0]
		if int(bdd_lang) == 0: self.u.ulang = "fr"
		else: self.u.ulang = "en"

	def tools_type_str(self,word):
		mouse = pymouse.Controller()
		keyboard = pykeyboard.Controller()
		for i in word:
			print(i)
			if i == '\n':
				keyboard.press(pykeyboard.Key.enter)
				keyboard.release(pykeyboard.Key.enter)
			else:
				keyboard.press(str(i))
				keyboard.release(str(i))

	def tools_get_checked_widget(self,lay):
		res = []
		for i in range(lay.count()):
			if lay.itemAt(i).widget().isChecked(): res.append(lay.itemAt(i).widget())
		return res

	def tools_callback(self,func):
		if func is None: return
		if isinstance(func,list):
			func[0](*func[1])
			return
		else:
			func()
