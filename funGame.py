from gameStructure import *


class funGame(GameStructure):
	
	def __init__(self,playerTypes):
		GameStructure.__init__(self,playerTypes)

	''' Implementation of game rules with (semi-)PURE Functions'''
	
	def initializePositions(self):
		'''self.pieces = dict( [((x,y),Piece((lambda y: (y<4 and "white") or "black")(y),x,y)) for x in range(0,8) for y in range(0,8) if (not 3<=y<=4 and (
																																		((y%2==0) and [z*2 + 1 for z in range(0,4)].__contains__(x))
																																		or
																																		((y%2==1)and [z*2 for z in range(0,4)].__contains__(x)))
																																		)  ])'''
		# the line above works and is more generic, but the one below is more explicit and works aswell:
		self.pieces = dict([ ((x,y),Piece((lambda y: (y<5 and "white") or "black")(y),x,y))
							for x in range(0,8)
							for y in range(0,8)
							if [(4,7),(3,0),(0,7),(1,6),(2,5),(7,2),(1,2),(6,7),
								(7,6),(5,6),(5,0),(4,1),(2,7),(3,2),(3,6),(4,5),
								(0,5),(2,1),(1,0),(6,5),(0,1),(7,0),(6,1),(5,2)]
								.__contains__((x,y))
		
		])
		
	def passTurn(self):
		self.pieces = dict( [(pos,(lambda pos,piece: (pos[1]==piece.queenPosY and Piece(pieces.color,pos[0],pos[1],True)) or piece ) (pos,pieces))
							for pos,pieces in self.pieces.iteritems()] )
				
		self.currentPlayer = (self.currentPlayer.color=="white" and self.player["black"]) or self.player["white"]
		
		self.newTurn()
		
	def checkWinner(self):
		return (self.player["white"].npieces == 0 and "black") or \
			   (self.player["black"].npieces == 0 and "white") or \
			   "nobody"
			   
	def newTurn(self):
		self.winner = self.checkWinner()
			
		self.calculatePlays()
	
	'''def calculateQueenPlays(self,i):
		if self.currentPlayer.color == "white":
			otherColor = "black"
		else:
			otherColor = "white"		
		directions = [(1,1),(-1,-1),(-1,1),(1,-1)]
		for k in directions:
			x = self.pieces[i].x
			y = self.pieces[i].y
			piece = 0
			isok = False
			possible = True
			noeatMovables = {}
			while possible and self.isInBounds(x,y):
				x = x + k[0]
				y = y + k[1]
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
				self.pieces[i].movables = dict(noeatMovables, **(self.pieces[i].movables))'''
		
	
	
	def calculateQueenMovables(self,piece):
		# Implement me!
		print "calculateQueenMovables() not implemented."
		return {}

	def calculateNormalPieceMovables(self,piece):
		directions = [(1,1),(-1,-1),(-1,1),(1,-1)]
		
		def willEat(dirx,diry):
			if self.isInBounds(piece.x+dirx,piece.y+diry) \
				 and not self.hasPiece(piece.x+dirx,piece.y+diry) \
				 and	((piece.color=="white" and diry==1) or \
						(piece.color=="black" and diry==-1)):
				return 0
			elif (self.isInBounds(piece.x+dirx*2,piece.y+diry*2) and \
					self.hasPieceWithColor(piece.x+dirx,piece.y+diry, (lambda x: (x=="white" and "black") or "white")(self.currentPlayer.color)) and \
					not self.hasPiece(piece.x+dirx*2,piece.y+diry*2)):
				return 1
			else:
				return -1
		
		return dict( [ (lambda dirx,diry: (willEat(dirx,diry) and ((piece.x+dirx*2,piece.y+diry*2),(piece.x+dirx,piece.y+diry)))
											or ((piece.x+dirx,piece.y+diry),"noeat"))(dirx,diry)
						for dirx,diry in directions if willEat(dirx,diry)!=-1 ])
																					 

	
	def calculateEatables(self,it):
		try:
			if next(it)!="noeat":
				return 1
			else:
				return self.calculateEatables(it)
		except StopIteration:
			return 0
	
	def calculatePlays(self,it=0):
		if it==0:
			self.obrigatoryPieces = []
			self.calculatePlays(self.pieces.itervalues())
		else:
			try:
				this = next(it)

				if this.color == self.currentPlayer.color:
					if this.isqueen:
						this.movables = self.calculateQueenMovables(this)
					else:
						this.movables = self.calculateNormalPieceMovables(this)
					
					this.eatables = self.calculateEatables(this.movables.itervalues())
					
					# if this piece has eatables, then it's a obrigatory piece
					if this.eatables != 0:
						self.obrigatoryPieces.append((this.x,this.y))
						
				self.calculatePlays(it)
				
			except StopIteration:
				pass
