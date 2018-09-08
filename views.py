import os
import pandas as pd
from functools import partial
from PyQt5.QtCore import QDate
import barcode
from barcode.writer import ImageWriter
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class Views:
	def view_menu(self):
		self.menu_grid.addWidget(self.u.UQtxt("MENU_STD_TITLE",title="Choisissez une action"),0,0,1,-1)
		self.menu_grid.addWidget(self.u.UQbut("MENU_STD_BUT",title="Ajout/mise à jour client",connect2=["clicked",self.view_box_users_create]),1,0)
		self.menu_grid.addWidget(self.u.UQbut("MENU_STD_BUT",title="Liste des clients",connect2=["clicked",self.view_box_users_list]),1,1)
		self.menu_grid.addWidget(self.u.UQbut("MENU_STD_BUT",title="Ajout/mise à jour matière",connect2=["clicked",self.view_box_lessons_create]),2,0)
		self.menu_grid.addWidget(self.u.UQbut("MENU_STD_BUT",title="Liste des matières",connect2=["clicked",self.view_box_lessons_list]),2,1)
		self.menu_grid.addWidget(self.u.UQbut("MENU_STD_BUT",title="Ajout/mise à jour niveau",connect2=["clicked",self.view_box_levels_create]),3,0)
		self.menu_grid.addWidget(self.u.UQbut("MENU_STD_BUT",title="Liste des niveaux",connect2=["clicked",self.view_box_levels_list]),3,1)
		self.menu_grid.addWidget(self.u.UQbut("MENU_STD_BUT",title="Ajouter un paiement",connect2=["clicked",self.view_box_payments_create]),4,0)
		self.menu_grid.addWidget(self.u.UQbut('MENU_STD_BUT',title="Liste des paiements",connect2=["clicked",self.view_box_payments_list]),4,1)
		self.menu_grid.addWidget(self.u.UQbut('MENU_STD_BUT',title="Liste des paiements",connect2=["clicked",self.view_box_barcode_create]),5,0)

	def view_box_users_create(self,user_id):
		self.tools_remove_items(self.content_grid)
		grid = self.content_grid
		grid.addWidget(self.u.UQtxt("BOX_STD_TITLE",title="Info client"),0,0,1,-1)
		if user_id: users = self.bdd.request("SELECT * FROM users where user_id="+str(user_id))[0]
		else:  users = dict(zip(self.bdd.cols("users"),[None]*100))
		items = self.bdd.request("SELECT printf('%s %s',firstname,lastname), cast(user_id as text) FROM users",True)
		items.insert(0,["Nouveau client",0])
		w = self.u.UQcombo(name_id="user_id",style="field",items=items,connect2=["changed",partial(self.sig_change,"user_id",self.view_box_users_create)])
		w.setCurrentData(user_id)
		grid.addWidget(w,1,0,1,-1)
		grid.addWidget(self.u.UQtxt(title="Niveau de l'élève",style="label"),2,0)
		items = self.bdd.request("SELECT title,level_id FROM levels",True)
		grid.addWidget(self.u.UQcombo(name_id="level_id",items=items),2,1)
		ii = 2
		for i,j in users.items():
			if i in ["user_id","level_id"]: continue
			ii += 1
			grid.addWidget(self.u.UQtxt(style="label",title=self.u.get_text(i)),ii,0)
			if i == "address":
				grid.addWidget(self.u.UQplaintxtedit(name_id=i,style="field",title=j),ii,1,1,2)
			else:
				grid.addWidget(self.u.UQtxtedit(name_id=i,style="field",title=j),ii,1)
		grid.addWidget(self.u.UQbut("STD_BUTTON",title="Sauvegarder",connect2=["clicked",partial(self.sig_create,"users","user_id",self.view_box_users_list)]),ii+1,0)

	def view_box_users_list(self):
		self.tools_remove_items(self.content_grid)
		grid = self.content_grid
		grid.addWidget(self.u.UQtxt("BOX_STD_TITLE",title="Liste des clients"),0,0,1,-1)
		users = self.bdd.request("SELECT user_id,email,firstname,lastname,phone1,phone2,address,l.title as level FROM users LEFT JOIN levels l USING(level_id)")
		if len(users) == 0:
			grid.addWidget(self.u.UQtxt(style="label",title="Aucun clients"),1,0)
			return
		users_cols = list(users[0].keys())
		users_cols.append("dels")
		for i,j in enumerate(users_cols):
			if j not in ["dels","user_id"]:
				grid.addWidget(self.u.UQtxt(style="label",title=j),1,i)
			ii = 1
			for k in users:
				ii += 1
				if j == "dels":
					grid.addWidget(self.u.UQbut("BUT_DEL",connect2=["clicked",partial(self.sig_del_field,"users","user_id="+str(k["user_id"]),self.view_box_users_list)]),ii,i)
				else:
					grid.addWidget(self.u.UQtxt(style="field",title=k[j]),ii,i)

	def view_box_lessons_create(self,lesson_id):
		self.tools_remove_items(self.content_grid)
		grid = self.content_grid
		grid.addWidget(self.u.UQtxt("BOX_STD_TITLE",title="Ajouter ou mettre à jour une matière"),0,0,1,-1)
		if lesson_id: lessons = self.bdd.request("SELECT * FROM lessons where lesson_id="+str(lesson_id))[0]
		else:  lessons = dict(zip(self.bdd.cols("lessons"),[None]*100))
		items = self.bdd.request("SELECT title, cast(lesson_id as text) FROM lessons",True)
		items.insert(0,["Nouvelle matière",0])
		w = self.u.UQcombo(name_id="lesson_id",style="field",items=items,connect2=["changed",partial(self.sig_change,"lesson_id",self.view_box_lessons_create)])
		w.setCurrentData(lesson_id)
		grid.addWidget(w,1,0,1,-1)
		ii = 1
		for i,j in lessons.items():
			if i == "lesson_id": continue
			ii += 1
			grid.addWidget(self.u.UQtxt(style="label",title=self.u.get_text(i)),ii,0)
			grid.addWidget(self.u.UQtxtedit(name_id=i,style="field",title=j),ii,1)
		grid.addWidget(self.u.UQbut("STD_BUTTON",title="Sauvegarder",connect2=["clicked",partial(self.sig_create,"lessons","lesson_id",self.view_box_lessons_list)]),ii+1,0)

	def view_box_lessons_list(self):
		self.tools_remove_items(self.content_grid)
		grid = self.content_grid
		grid.addWidget(self.u.UQtxt("BOX_STD_TITLE",title="Liste des matières"),0,0,1,-1)
		lessons = self.bdd.request("SELECT * FROM lessons")
		if len(lessons) == 0:
			grid.addWidget(self.u.UQtxt(style="label",title="Aucunes matières"),1,0)
			return
		lessons_cols = list(lessons[0].keys())
		lessons_cols.append("dels")
		for i,j in enumerate(lessons_cols):
			if j not in ["dels","lesson_id"]:
				grid.addWidget(self.u.UQtxt(style="label",title=j),1,i)
			ii = 1
			for k in lessons:
				ii += 1
				if j == "dels":
					grid.addWidget(self.u.UQbut("BUT_DEL",connect2=["clicked",partial(self.sig_del_field,"lessons","lesson_id="+str(k["lesson_id"]),self.view_box_lessons_list)]),ii,i)
				else:
					grid.addWidget(self.u.UQtxt(style="field",title=k[j]),ii,i)

	def view_box_levels_create(self,level_id):
		self.tools_remove_items(self.content_grid)
		grid = self.content_grid
		grid.addWidget(self.u.UQtxt("BOX_STD_TITLE",title="Ajouter ou mettre à jour un niveau"),0,0,1,-1)
		if level_id: levels = self.bdd.request("SELECT * FROM levels where level_id="+str(level_id))[0]
		else:  levels = dict(zip(self.bdd.cols("levels"),[None]*100))
		items = self.bdd.request("SELECT title, cast(level_id as text) FROM levels",True)
		items.insert(0,["Nouveau niveau",0])
		w = self.u.UQcombo(name_id="level_id",style="field",items=items,connect2=["changed",partial(self.sig_change,"level_id",self.view_box_levels_create)])
		w.setCurrentData(level_id)
		grid.addWidget(w,1,0,1,-1)
		ii = 1
		for i,j in levels.items():
			if i == "level_id": continue
			ii += 1
			grid.addWidget(self.u.UQtxt(style="label",title=self.u.get_text(i)),ii,0)
			grid.addWidget(self.u.UQtxtedit(name_id=i,style="field",title=j),ii,1)
		grid.addWidget(self.u.UQbut("STD_BUTTON",title="Sauvegarder",connect2=["clicked",partial(self.sig_create,"levels","level_id",self.view_box_levels_list)]),ii+1,0)

	def view_box_levels_list(self):
		self.tools_remove_items(self.content_grid)
		grid = self.content_grid
		grid.addWidget(self.u.UQtxt("BOX_STD_TITLE",title="Liste des niveaux"),0,0,1,-1)
		levels = self.bdd.request("SELECT * FROM levels")
		if len(levels) == 0:
			grid.addWidget(self.u.UQtxt(style="label",title="Aucun  niveau"),1,0)
			return
		levels_cols = list(levels[0].keys())
		levels_cols.append("dels")
		for i,j in enumerate(levels_cols):
			if j not in ["dels","level_id"]:
				grid.addWidget(self.u.UQtxt(style="label",title=j),1,i)
			ii = 1
			for k in levels:
				ii += 1
				if j == "dels":
					grid.addWidget(self.u.UQbut("BUT_DEL",connect2=["clicked",partial(self.sig_del_field,"levels","level_id="+str(k["level_id"]),self.view_box_levels_list)]),ii,i)
				else:
					grid.addWidget(self.u.UQtxt(style="field",title=k[j]),ii,i)

	def view_box_payments_create(self,lesson_id):
		self.tools_remove_items(self.content_grid)
		grid = self.content_grid
		grid.addWidget(self.u.UQtxt("BOX_STD_TITLE",title="Ajouter un paiement"),0,0,1,-1)
		grid.addWidget(self.u.UQtxt(style="label",title="Client"),1,0)
		items = self.bdd.request("SELECT printf('%s %s',firstname,lastname), cast(user_id as text) FROM users",True)
		grid.addWidget(self.u.UQcombo(name_id="user_id",style="field",items=items),1,1)
		grid.addWidget(self.u.UQtxt(style="label",title="Matière"),2,0)
		items = self.bdd.request("SELECT title, cast(lesson_id as text) as lesson_id FROM lessons",True)
		if not lesson_id:
			lesson_id = items[0][1]
		w = self.u.UQcombo(current_data=lesson_id, name_id="lesson_id",style="field",items=items,connect2=["changed",partial(self.sig_change,"lesson_id",self.view_box_payments_create)])
		grid.addWidget(w,2,1)
		items = self.bdd.request("SELECT price_15,price_30 FROM lessons WHERE lesson_id="+str(lesson_id))
		grid.addWidget(self.u.UQtxt(style="label",title="price_15"),3,0)
		grid.addWidget(self.u.UQcheckbox(exclusive=True,name_id="price_15",style="label",title=str(items[0]["price_15"]) + " MAD",connect2=["toggled",self.sig_price_change]),3,1)
		grid.addWidget(self.u.UQtxt(style="label",title="price_30"),4,0)
		grid.addWidget(self.u.UQcheckbox(checked=True,exclusive=True,name_id="price_30",style="label",title=str(items[0]["price_30"]) + " MAD",connect2=["toggled",self.sig_price_change]),4,1)
		grid.addWidget(self.u.UQtxt(style="label",title="Mois concerné"),5,0)
		grid.addWidget(self.u.UQdateedit(name_id="selected_period",popup=True,date_format="MMMM yyyy"),5,1)
		grid.addWidget(self.u.UQtxt(style="label",title="Remise (MAD)"),6,0)
		grid.addWidget(self.u.UQtxtedit(name_id="discount",title="0",style="field",connect2=["changed",self.sig_price_change]),6,1)
		grid.addWidget(self.u.UQtxt(style="label",title="Prix total (MAD)"),7,0)
		grid.addWidget(self.u.UQtxt(name_id="total_price",style="label"),7,1)
		grid.addWidget(self.u.UQbut("STD_BUTTON",title="Sauvegarder",connect2=["clicked",partial(self.sig_create,"payments","payment_id",self.view_box_payments_list)]),8,0)
		self.sig_price_change()

	def view_box_payments_list(self):		
		self.tools_remove_items(self.content_grid)
		grid = self.content_grid
		grid.addWidget(self.u.UQtxt("BOX_STD_TITLE",title="Liste des paiements"),0,0,1,-1)
		payments = self.bdd.request("""
			SELECT p.payment_id as payment_id,printf('%s %s',u.firstname,u.lastname) as user
			, payment_date, selected_period
			, CASE WHEN p.price_30 THEN 'price_30' ELSE 'price_15' END price_duration
			, CASE WHEN p.price_30 THEN l.price_30 ELSE l.price_15 END price
			, p.discount, p.total_price
			FROM payments p
			JOIN lessons l USING(lesson_id)
			JOIN users u USING(user_id)
			""")
		if len(payments) == 0:
			grid.addWidget(self.u.UQtxt(style="label",title="Aucun payment"),1,0)
			return
		payments_cols = list(payments[0].keys())
		payments_cols.append("dels")
		for i,j in enumerate(payments_cols):
			if j not in ["dels","payment_id"]:
				grid.addWidget(self.u.UQtxt(style="label",title=j),1,i)
			ii = 1
			for k in payments:
				ii += 1
				if j == "selected_period": k[j] = QDate.fromString(k[j],'yyyy-MM-dd').toString("MMMM yyyy")

				if j == "payment_date": k[j] = QDate.fromString(k[j],'yyyy-MM-dd').toString("dd/MM/yyyy")
				if j == "dels":
					grid.addWidget(self.u.UQbut("BUT_DEL",connect2=["clicked",partial(self.sig_del_field,"payments","payment_id="+str(k["payment_id"]),self.view_box_payments_list)]),ii,i)
				else:
					grid.addWidget(self.u.UQtxt(style="field",title=k[j]),ii,i)

	def view_box_barcode_create(self):
		self.tools_remove_items(self.content_grid)
		grid = self.content_grid
		grid.addWidget(self.u.UQtxt("BOX_STD_TITLE",title="Générer des codes barres"),0,0,1,-1)
		items = self.bdd.request("SELECT printf('%s %s',firstname,lastname),user_id FROM users",True)
		grid.addWidget(self.u.UQcombo(name_id="user_id",style="label",items=items),1,0,)
		subgrid = self.u.UQvboxlayout()
		w = self.u.UQwidget()
		w.setLayout(subgrid)
		grid.addWidget(self.u.UQbut(style="STD_BUTTON",title="Ajouter",connect2=["clicked",partial(self.sig_add_user,subgrid)]),1,1)
		grid.addWidget(w,2,0,1,-1)
		# w = self.view_user_card(str(items[0][1]))
		grid.addWidget(w,2,0,1,-1)
		grid.addWidget(self.u.UQbut(style="STD_BUTTON",title="Générer",connect2=["clicked",partial(self.u.print_widget_as_pdf,w)]),3,0)

	def view_user_card(self,user_id):
		grid = self.u.UQgridlayout()
		w = self.u.UQframebox()
		w.setLayout(grid)
		user = self.bdd.request("SELECT * FROM users WHERE user_id="+user_id)[0]
		grid.addWidget(self.u.UQtxt(style="label", title=user["firstname"] + " " + user["lastname"]),0,0,1,-1)
		ean = barcode.get_barcode_class(u'ean13')
		d = ''.join(user["registered_date"].split('-')) + str(user["user_id"])
		d = (13-len(d))*'1'+d
		code = ean(d,writer=ImageWriter())
		fullname = code.save("img/temp")
		l = self.u.UQtxt(style="center")
		l.setPixmap(QPixmap("img/temp.png").scaled(200,200,Qt.KeepAspectRatio,Qt.SmoothTransformation))
		grid.addWidget(l,1,0,1,-1)
		return w