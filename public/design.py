from PyQt5.QtWidgets import QGridLayout
class Design:
	def design_sub_box(self,parent_grid,row,col=None,Lrow=1,Lcol=1,name_id=None,style=""):
		layGrid = self.u.UQgridlayout()
		style += " stdSubBox"
		Grid = self.u.UQframebox(name_id=name_id,style=style)
		Grid.setLayout(layGrid)
		if isinstance(parent_grid,QGridLayout):
			parent_grid.addWidget(Grid,row,col,Lrow,Lcol)
		else : 
			parent_grid.addWidget(Grid,row)
		return layGrid

	# def form(self,lay,d):

