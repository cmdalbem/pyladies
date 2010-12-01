
def newPlayer(type,color):
	if type == "Human":
		return HumanPlayer(color)
	elif type == "Computer":
		return ComputerPlayer(color)

class Player:
	def __init__(self,color):
		self.npieces = 12
		self.color = color
	
	def losePiece(self):
		self.npieces -= 1

class HumanPlayer(Player):
	def __init__(self,color):
		Player.__init__(self,color)
		self.state = "stopped"
		self.type = "Human"
	
class ComputerPlayer(Player):
	def __init__(self,color):
		Player.__init__(self,color)
		self.type = "Computer"
