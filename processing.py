import pandas as pd
class Processing:
	def process_file_info(self,fpath,sep=";"):
		self.current_file = fpath
		data = pd.read_csv(fpath,sep,encoding="ISO-8859-1")
		# print(data.head())


if __name__ == '__main__':
	data = pd.read_csv(fpath,';',encoding="ISO-8859-1")
