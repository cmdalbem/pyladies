import pygtk
pygtk.require('2.0')
import gtk.glade
import cairo
import math

from piece import *
from main import *

global SIZEX
global SIZEY
FRAME = 0
DSTONES = 70
STONE_R = 25

SCREENX = SIZEX*DSTONES + 2*FRAME
SCREENY = SIZEY*DSTONES + 2*FRAME

global game


class Screen():
	def __init__(self,drawable):
		self.drawable = drawable
		self.drawable.connect("expose-event", self.expose)
		self.drawable.set_size_request(SCREENX,SCREENY)
		self.squares = {}
		for x in range(8):
			for y in range(8):
				self.squares[x,y] = 0
						
		self.selected = 0
	
	def drawPiece(self,cr,x,y,piece):
		cr.set_line_width(3)
		cr.set_source_rgb(*piece.getDrawColor())
		
		if piece.color=="white":
			cr.arc( x, y, STONE_R, 0, math.pi*2)
			cr.fill()
			cr.set_source_rgb(0,0,0)
			cr.arc( x, y , STONE_R, 0, math.pi*2)
			cr.stroke();
		elif piece.color=="black":
			cr.arc( x, y, STONE_R, 0, math.pi*2)
			cr.fill()
		
		# queen mark
		if piece.isqueen:
			cr.set_source_rgb(0.8,0.25,0)
			cr.select_font_face("Georgia",cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
			cr.set_font_size(50)
			x_bearing, y_bearing, width, height = cr.text_extents("*")[:4]
			cr.move_to(x - width/2 - x_bearing, y - height/2 - y_bearing)
			cr.show_text("*")
			cr.stroke();
		
		# other marks
		if piece.isselected:
			cr.set_line_width(4)
			if piece.eatables > 0:
				for i in piece.movables:
					if piece.movables[i]!="noeat":
						self.markSquare(*i)
						self.markEatable(cr,piece.movables[i])
			else:
				for i in piece.movables:
					if piece.movables[i]=="noeat":
						self.markSquare(*i)
	
	def markEatable(self,cr,piece):
		cr.set_source_rgb(0,1,0)
		x,y = self.getPiecePos(*piece)
		cr.arc(x,y, STONE_R, 0, math.pi*2)
		cr.stroke()
	
	def drawRectangle(self, cr, x, y, rgb):
		cr.set_source_rgb(*rgb)
		cr.rectangle(FRAME+x*DSTONES, FRAME+y*DSTONES, DSTONES, DSTONES)
		cr.fill()
		
	def getPiecePos(self,x,y):
		return (FRAME+x*DSTONES + DSTONES/2,FRAME+y*DSTONES + DSTONES/2)
	
	def expose(self, widget, event):
		cr = widget.window.cairo_create()
		
		# background color
		cr.set_source_rgb(1,1,1)
		cr.rectangle(0, 0, widget.allocation.width, widget.allocation.height)
		cr.fill()
		
		# squares
		iswhite = True;
		for y in range(8):
			for x in range(8):
				if iswhite:
					rgb = [0.9,0.9,0.9]
				else:
					rgb = [0.6,0.6,0.6]
				if self.squares[x,y] == 1:
					#rgb = [x*1.3 for x in rgb] # why the hell it doesnt work?!?
					rgb[0] += 0.2
					rgb[1] += 0.2
					rgb[2] += 0.2
				self.drawRectangle(cr,x,y,rgb)
				iswhite = not iswhite
			iswhite = not iswhite
		
		# pieces
		for i in game.pieces:
			pos = self.getPiecePos(*i)
			self.drawPiece(cr,pos[0],pos[1],game.pieces[i])
		
		if game.obrigatoryPieces.__len__()>0:
			for i in game.obrigatoryPieces:
				pos = self.getPiecePos(*i)
				cr.set_source_rgb(1,0,0)
				cr.arc( pos[0],pos[1], STONE_R, 0, math.pi*2)
				cr.stroke()
		else:
			for i in game.pieces:
				if game.pieces[i].color == game.currentPlayer.color and\
						game.pieces[i].movables.__len__():
					pos = self.getPiecePos(*i)
					cr.set_source_rgb(1,0,0)
					cr.arc( pos[0],pos[1], STONE_R, 0, math.pi*2)
					cr.stroke()
		
	def selectSquare(self,x,y):
		#you can only select obrigatory pieces
		if game.obrigatoryPieces.__len__()>0:
			if game.obrigatoryPieces.__contains__((x,y)):
				self.selectPiece(x,y)
				self.markSquare(x,y)
				return "selected"
			else:
				return "idle"
		
		#there isnt obrigatory pieces
		elif game.hasPieceWithColor(x,y,game.currentPlayer.color) and\
				game.pieces[(x,y)].movables.__len__():
			self.selectPiece(x,y)
			self.markSquare(x,y)
			return "selected"
		else:
			return "idle"
		
	def markSquare(self,x,y):
		self.squares[x,y] = 1
		self.drawable.queue_draw_area(FRAME+x*DSTONES, FRAME+y*DSTONES, DSTONES, DSTONES)

	def deselect(self):
		if self.selected != 0:
			for i in self.squares:
				self.squares[i] = 0
			self.selected.deselect()
			self.selected = 0
			self.update()
		return "idle"
	
	def selectPiece(self,x,y):
		game.pieces[x,y].select()
		self.selected = game.pieces[x,y]
		self.update()
		
	def update(self):
		self.drawable.queue_draw_area(0,0, SCREENX, SCREENY)
			
	def action(self,x,y):
		if not game.hasPiece(x,y):
			if self.selected.x==x and self.selected.y==y:
				return "selected"
		
			if self.selected.movables.has_key((x,y)):
				ate = self.selected.movables[(x,y)]
				if ate=="noeat":
					if self.selected.eatables==0:
						self.selectedMoveAction(x,y)
						self.deselect()
						return "done"
					else:
						return "selected"
				else:
					return self.selectedEatAction(x,y,ate[0],ate[1])
			else:
				return "selected"
				
		else:
			return "selected"
			
	def selectedMoveAction(self,x,y):
		game.pieces.pop((self.selected.x,self.selected.y))
		self.selected.moveTo(x,y)
		game.pieces[x,y] = self.selected
		
	def selectedEatAction(self,x,y,atex,atey):
		game.player[game.pieces[atex,atey].color].losePiece()
		self.selectedMoveAction(x,y)
		game.pieces.pop((atex,atey))
		game.calculatePlays()
		if self.selected.eatables == 0: #can't eat anymore
			self.deselect()
			return "done"
		else:
			game.pieces[x,y] = self.selected
			self.deselect()
			self.selectPiece(x,y)
			return "ate"		


class GUI:
	def __init__(self):
		builder = gtk.Builder()
		builder.add_from_file("gui.glade")
		
		self.window = builder.get_object("window")
		self.screen = Screen(builder.get_object("screen"))
		self.blackPlayerPanel = builder.get_object("player1Panel")
		self.whitePlayerPanel = builder.get_object("player2Panel")
		self.blackPiecesPanel = builder.get_object("blackPiecesPanel")
		self.whitePiecesPanel = builder.get_object("whitePiecesPanel")
		builder.connect_signals(self)
		
		self.updatePanel()
		self.window.show_all()

	def updatePanel(self,foo1=0,foo2=0):
		if game.winner == "white":
			self.whitePlayerPanel.set_label( "<b><span color=\"darkgreen\">Winner!</span></b>" )
			self.blackPlayerPanel.set_label( "<b><span color=\"darkred\">Loser!</span></b>" )
		elif game.winner == "black":
			self.whitePlayerPanel.set_label( "<b><span color=\"darkred\">Loser!</span></b>" )
			self.blackPlayerPanel.set_label( "<b><span color=\"darkgreen\">Winner!</span></b>" )
		else:
			if game.currentPlayer.color == "white":
				self.whitePlayerPanel.set_label( "<b>[" + game.player["white"].type + "]</b>" )
			else:
				self.whitePlayerPanel.set_label( game.player["white"].type )
			
			if game.currentPlayer.color == "black":
				self.blackPlayerPanel.set_label( "<b>[" + game.player["black"].type + "]</b>" )
			else:
				self.blackPlayerPanel.set_label( game.player["black"].type)
			
		self.blackPiecesPanel.set_text( str(game.player["black"].npieces) )
		self.whitePiecesPanel.set_text( str(game.player["white"].npieces) )

	def window_destroy_event_cb(self, widget, data=None):
		gtk.main_quit()
		
	def openAboutDialog(self, widget, data=None):
		about = gtk.AboutDialog()
		about.set_version("0.1")
		about.set_program_name("pyLadies (an Draughts game)")
		about.set_comments("\nAn case study about programming with Python in Object Oriented and Functional paradigms.")
		about.set_website("http://pyladies.googlecode.com")
		about.set_copyright("by Cristiano Medeiros Dalbem")
		about.set_logo(gtk.gdk.pixbuf_new_from_file("logo.png"))
		about.run()
		about.destroy()
	
	def newGameButton_clicked_cb(self, widget, data=None):
		game.newGame()
		self.screen.update()
		self.updatePanel()
	
	def passButton_clicked_cb(self, widget, data=None):
		game.passTurn()
		self.updatePanel()
		self.screen.update()

	def screen_button_press_event_cb(self, widget, event, data=None):
		if event.button == 1:
			x = int((event.x-FRAME)/DSTONES)
			y = int((event.y-FRAME)/DSTONES)
			
			clickOpt = dict( stopped	= self.updatePanel,
							 idle		= self.screen.selectSquare,
							 selected	= self.screen.action,
							 ate		= self.screen.action )
			
			game.state = clickOpt[game.state](x,y)
			if game.state == "done":
				game.passTurn()
				if game.winner!="nobody":
					game.state = "stopped"
				else:					
					game.state = "idle"
		
			self.screen.update()
			self.updatePanel()
