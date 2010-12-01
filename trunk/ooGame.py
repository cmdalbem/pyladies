from gameStructure import *


class OOGame(GameStructure):
	
	def __init__(self,playerTypes):
		GameStructure.__init__(self,playerTypes)
		
		
	''' Implementation of game rules with NON-PURE IMPERATIVE Functions '''
	
	def initializePositions(self):
		self.pieces = {}
		
		var = True
		for y in range(0,3):
			for x in range(0,8,2):
				self.pieces[x+var,y] = Piece("white",x+var,y)
			var = not var
		
		var = False
		for y in range(5,8):
			for x in range(0,8,2):
				self.pieces[x+var,y] = Piece("black",x+var,y)
			var = not var	
	
	def passTurn(self):
		for i in self.pieces:
			if i[1] ==  self.pieces[i].queenPosY:
				self.pieces[i].isqueen = True
		if self.currentPlayer.color == "white":
			self.currentPlayer = self.player["black"]
		else:
			self.currentPlayer = self.player["white"]
		self.newTurn()
		
	def newTurn(self):
		self.calculatePlays()
		if self.player["white"].npieces == 0:
			self.winner = "black"
		if self.player["black"].npieces == 0:
			self.winner = "white"
		elif self.currentPlayer.type == "computer":
			passTurn()
		else:
			pass
			
	
	def calculateQueenPlays(self,i):
		if self.currentPlayer.color == "white":
			otherColor = "black"
		else:
			otherColor = "white"		
		directions = [(1,1),(-1,-1),(-1,1),(1,-1)]
		for k in directions:
			x,y = i
			piece = 0
			isok = False
			possible = True
			noeatMovables = {}
			while possible and self.isInBounds(x,y):
				x,y = x + k[0], y + k[1]
				if piece!=0: #has candidate
					if self.isInBounds(x,y):
						if self.hasPiece(x,y): #next square is occupied, cannot eat
							possible = False
						else: #at lest the next square is free, can eat
							isok = True
							self.pieces[i].movables[(x,y)] = piece
				else:
					if self.hasPieceWithColor(x,y,otherColor): #found an candidate
						piece = (x,y)
					elif self.hasPieceWithColor(x,y,self.currentPlayer.color): #path is blocked
						possible = False
					else:
						noeatMovables[(x,y)] = "noeat"
						
			if isok==True:
				self.pieces[i].eatables += 1
			else:
				self.pieces[i].movables = dict(noeatMovables, **(self.pieces[i].movables))
		
	def calculateNormalPiecePlays(self,i):
		if self.currentPlayer.color == "white":
			otherColor = "black"
		else:
			otherColor = "white"		
		directions = [(1,1),(-1,-1),(-1,1),(1,-1)]
		for k in directions:
			if self.hasPieceWithColor(k[0]+i[0],k[1]+i[1],otherColor) and\
					self.isInBounds(k[0]*2+i[0],k[1]*2+i[1]) and\
					not self.hasPiece(k[0]*2+i[0],k[1]*2+i[1]):
				self.pieces[i].eatables += 1
				self.pieces[i].movables[(k[0]*2+i[0],k[1]*2+i[1])] = (k[0]+i[0],k[1]+i[1])
			# no eating
			else:
				if self.isInBounds(k[0]+i[0],k[1]+i[1]) and\
					not self.hasPiece(k[0]+i[0],k[1]+i[1]) and\
					((self.pieces[i].color=="white" and k[1]==1) or\
					(self.pieces[i].color=="black" and k[1]==-1)) :
						self.pieces[i].movables[(k[0]+i[0],k[1]+i[1])] = "noeat"		
		
	
	def calculatePlays(self):
		self.obrigatoryPieces = []
		
		for i in self.pieces:
			self.pieces[i].eatables = 0
			self.pieces[i].movables = {}
			if self.pieces[i].color == self.currentPlayer.color:
				if self.pieces[i].isqueen:
					self.calculateQueenPlays(i)
				else:
					self.calculateNormalPiecePlays(i)
				# if this piece has eatables, then it's a obrigatory piece
				if self.pieces[i].eatables != 0:
					self.obrigatoryPieces.append(i)
