import os
import pandas as pd
from functools import partial

class Views:
	def view_menu(self):
		self.menu_grid.addWidget(self.u.UQtxt("MENU_STD_TITLE",title="Choisissez une action"))
		self.menu_grid.addWidget(self.u.UQbut("MENU_STD_BUT",title="Ajout/mise à jour client",connect2=["clicked",self.view_box_users_create]))
		self.menu_grid.addWidget(self.u.UQbut("MENU_STD_BUT",title="Liste des clients",connect2=["clicked",self.view_box_users_list]))
		self.menu_grid.addWidget(self.u.UQbut("MENU_STD_BUT",title="Ajout/mise à jour matière",connect2=["clicked",self.view_box_lessons_create]))
		self.menu_grid.addWidget(self.u.UQbut("MENU_STD_BUT",title="Liste des matières",connect2=["clicked",self.view_box_lessons_list]))
		self.menu_grid.addWidget(self.u.UQbut("MENU_STD_BUT",title="Ajout/mise à jour niveau",connect2=["clicked",self.view_box_levels_create]))
		self.menu_grid.addWidget(self.u.UQbut("MENU_STD_BUT",title="Liste des niveau",connect2=["clicked",self.view_box_levels_list]))
		self.menu_grid.addWidget(self.u.UQbut("MENU_STD_BUT",title="Ajouter un paiement",connect2=["clicked",self.view_box_payments_create]))
	
	def view_box_users_create(self,user_id):
		self.tools_remove_items(self.content_grid)
		grid = self.content_grid
		grid.addWidget(self.u.UQtxt("BOX_STD_TITLE",title="Info client"),0,0,1,-1)
		if user_id: users = self.bdd.request("SELECT * FROM users where user_id="+str(user_id))[0]
		else:  users = dict(zip(self.bdd.cols("users"),[None]*100))
		items = self.bdd.request("SELECT printf('%s %s',firstname,lastname), cast(user_id as text) FROM users",True)
		items.insert(0,["Nouveau client",0])
		w = self.u.UQcombo(name_id="user_id",style="field",items=items,connect2=["changed",partial(self.sig_change,"users","user_id",self.view_box_users_create)])
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
		w = self.u.UQcombo(name_id="lesson_id",style="field",items=items,connect2=["changed",partial(self.sig_change,"lessons","lesson_id",self.view_box_lessons_create)])
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
		w = self.u.UQcombo(name_id="level_id",style="field",items=items,connect2=["changed",partial(self.sig_change,"levels","level_id",self.view_box_levels_create)])
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

	def view_box_payments_create(self):
		self.tools_remove_items(self.content_grid)
		grid = self.content_grid
		grid.addWidget(self.u.UQtxt("BOX_STD_TITLE",title="Ajouter un paiement"),0,0,1,-1)
		grid.addWidget(self.u.UQtxt(style="label",title="Client"),1,0)
		items = self.bdd.request("SELECT printf('%s %s',firstname,lastname), cast(user_id as text) FROM users",True)
		grid.addWidget(self.u.UQcombo(name_id="user_id",style="field",items=items),1,1)
		grid.addWidget(self.u.UQtxt(style="label",title="Matière"),2,0)
		items = self.bdd.request("SELECT title, cast(lesson_id as text) as lesson_id FROM lessons",True)
		grid.addWidget(self.u.UQcombo(name_id="lesson_id",style="field",items=items),2,1)
		items = self.bdd.request("SELECT price_15,price_30 FROM lessons WHERE lesson_id="+items[0][1])
		grid.addWidget(self.u.UQtxt(style="label",title="price_15"),3,0)
		grid.addWidget(self.u.UQcheckbox(exclusive=True,name_id="price_15",style="label",title=str(items[0]["price_15"]) + " MAD"),3,1)
		grid.addWidget(self.u.UQtxt(style="label",title="price_30"),4,0)
		grid.addWidget(self.u.UQcheckbox(checked=True,exclusive=True,name_id="price_30",style="label",title=str(items[0]["price_30"]) + " MAD"),4,1)
		grid.addWidget(self.u.UQtxt(style="label",title="Mois concerné"),5,0)
		grid.addWidget(self.u.UQdateedit(name_id="selected_period",popup=True,date_format="MMMM yyyy"),5,1)
		grid.addWidget(self.u.UQbut("STD_BUTTON",title="Sauvegarder",connect2=["clicked",partial(self.sig_create,"payments","payment_id",None)]),6,0)
