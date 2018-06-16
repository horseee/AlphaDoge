import sys
from PyQt5.QtWidgets import QApplication, QWidget ,QGridLayout, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QSize
from game import GoGame, colormap, DigitClock
import math

boardFrac = 0.85
from Opponents import RandomOppo
class App(QWidget):
	def __init__(self):
		super().__init__()
		self.title = 'Go'
		self.left = 50
		self.top = 50
		self.width = 850
		self.height = 800
		self.initUI()

	def initUI(self):
		assert(boardFrac>=0.5)
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top,self.width, self.height)
		self.env = GoGame(size=9, opponent=RandomOppo(),width=self.width*boardFrac*0.95, height=self.height*boardFrac*0.95)
		self.layout = QGridLayout()
		self.layout.setColumnStretch(0, math.ceil(boardFrac/(1-boardFrac)))
		self.layout.addWidget(self.env,0,0)
		self.layout.setColumnStretch(1, 1)
		sublayout = QVBoxLayout()
		sublayout.addWidget(DigitClock(  size=(0.9*self.width*(1-boardFrac),
															0.9*self.width*(1-boardFrac)/2), digits=8 ))
		pass_buttom = QPushButton('PASS',self)
		pass_buttom.isFlat=True
		pass_buttom.clicked.connect(self.env.pass_move)
		pass_buttom.setMinimumSize(QSize(0.9*self.width*(1-boardFrac),
															0.9*self.width*(1-boardFrac)/2))
		sublayout.addWidget(pass_buttom)
		sublayout.addStretch(1)

		self.layout.addLayout(sublayout,0,1)
		self.setLayout(self.layout)
		self.show()

def main():
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()