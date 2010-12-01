from gui import *

from ooGame import *
from funGame import *


''' uncomment me to use the O.O. version '''
#game = OOGame(["Human","Human"])

''' or uncomment me to use the Functional version '''
#game = funGame(["Human","Human"])


def main():

	if 'game' in globals():
		gui = GUI()
		gtk.main()
	else:
		print "Please select an implementation version on 'main.py'!"


if __name__ == "__main__":
      main()
