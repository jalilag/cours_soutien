class Error:
	def error_manage(self,*args,**kwargs):
		# paramètres
		# err_num : Numéro d'érreur faisant ref à public.error.err
		# check : si true déclenche l'érreur, check est renvoyé
		# fields: les champs concernés (facultatif)
		fields = kwargs.get("fields",None)
		check = kwargs.get("check",None)
		console = kwargs.get("console",None)
		if len(args) == 0: return 0
		listargs = args
		if isinstance(listargs[0],list): listargs = listargs[0]
		err_num = listargs[0]
		if len(listargs) >= 2 and check is None: check = listargs[1]
		if len(listargs) >= 3 and fields is None: fields = listargs[2]
		if len(listargs) == 4 and console is None: console = listargs[3]
		fields = self.u.get_text(fields)
		if check:
			self.u.UQapplication.restoreOverrideCursor()
			if self.errors[err_num]["group"] in self.u.utxt:
				group = self.u.utxt[self.errors[err_num]["group"]][self.u.ulang]
			else: group = self.errors[err_num]["group"]
			if self.errors[err_num]["msg"] in self.u.utxt:
				msg = self.u.utxt[self.errors[err_num]["msg"]][self.u.ulang]
			else: msg = self.errors[err_num]["msg"]
			msg = '0x{:04x}'.format(err_num) + " : " +msg
			if console:
				if fields is not None:
					print(group,"Items"+ " : " + fields + "\n" + msg)
				else:
					print(group,msg)
			else:
				if fields is not None:
					self.u.txtBox(group,"Items"+ " : " + fields + "\n" + msg,"critical")
				else:
					self.u.txtBox(group,msg,"critical")
		return check

