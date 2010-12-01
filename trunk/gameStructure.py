from player import *
from piece import *

SIZEX = 8
SIZEY = 8

class GameStructure:	

	''' Initialization Functions '''
	
	def newGame(self,playerTypes=0):
		colors = ["white","black"]
		
		if playerTypes!=0:
			for i in range(2):
				self.player[colors[i]] = newPlayer(playerTypes[i],colors[i])
		else:
			for i in range(2):
				self.player[colors[i]] = newPlayer(self.player[colors[i]].type,colors[i])
			
		self.currentPlayer = self.player["white"]
		self.initializePositions()
		self.obrigatoryPieces = []
		self.winner = "nobody"
		self.state = "idle"
		
		self.newTurn()
		
	def __init__(self,playerTypes):
		self.player = {}
		self.pieces = {}
		self.newGame(playerTypes)
					
		
	''' Utility Functions '''
	''' (they are all Pure Functions) '''
	
	def hasPiece(self,x,y):
		return self.pieces.has_key((x,y))
	
	def hasPieceWithColor(self,x,y,color):
		return self.hasPiece(x,y) and self.getPieceColor(x,y)==color
	
	def getPieceColor(self,x,y):
		return self.pieces[(x,y)].color
		
	def isInBounds(self,x,y):
		return x>=0 and y>=0 and x<SIZEX and y<SIZEY
