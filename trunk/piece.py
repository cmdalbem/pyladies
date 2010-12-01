class Piece():
	def __init__(self,color,posx,posy,isQueen=False):
		self.color = color
		self.isselected = False
		self.x = posx
		self.y = posy
		self.isqueen = isQueen
		self.eatables = []
		self.movables = {}
		if color == "white":
			self.queenPosY = 7
		elif color == "black":
			self.queenPosY = 0
		
	def select(self):
		self.isselected = True
	
	def deselect(self):
		self.isselected = False
		
	def getDrawColor(self):
		if self.color=="white":
			if self.isselected:
				return (1,0.7,0.7)
			else:
				return (1,1,1)
		elif self.color == "black":
			if self.isselected:
				return (0.5,0,0)
			else:
				return (0,0,0)
		
	def moveTo(self,x,y):
		self.x = x
		self.y = y
