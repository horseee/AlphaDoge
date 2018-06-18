import sys
from PyQt5.QtWidgets import QApplication, QWidget ,QGridLayout, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QSize
from game import GoGame, colormap, DigitClock
import math


boardFrac = 0.85

seconds_per_move=5
timed_match=False
search_n=800
ckpt = 'checkpoints/model'


from Opponents import randomOppo, AlphaDoge
class App(QWidget):
	def __init__(self):
		super().__init__()
		self.title = 'Go'
		self.left = 50
		self.top = 50
		self.width = 850
		self.height = 800
		self.initUI()

	def restart(self):
		self.env.restart()
		self.digit_clock.resetTime()
		self.update()

	def initUI(self):
		assert(boardFrac>=0.5)
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top,self.width, self.height)
		cond = QLabel("TO PLAY: BLACK")
		self.digit_clock = DigitClock(  size=(0.9*self.width*(1-boardFrac),
															0.9*self.width*(1-boardFrac)/2), digits=8 )
		doge = AlphaDoge(ckpt,seconds_per_move=seconds_per_move,timed_match=timed_match,search_n=search_n)
		self.env = GoGame(size=9, oppo_thread=doge,width=self.width*boardFrac*0.95, height=self.height*boardFrac*0.95, condition=cond, reset_clock=self.digit_clock.resetTime)
		self.layout = QGridLayout()
		self.layout.setColumnStretch(0, math.ceil(boardFrac/(1-boardFrac)))
		self.layout.addWidget(self.env,0,0)
		self.layout.setColumnStretch(1, 1)
		
		sublayout = QVBoxLayout()
		sublayout.addWidget(self.digit_clock)
		pass_buttom = QPushButton('PASS',self)
		pass_buttom.isFlat=True
		pass_buttom.clicked.connect(self.env.pass_move)
		pass_buttom.setMinimumSize(QSize(0.9*self.width*(1-boardFrac),
															0.9*self.width*(1-boardFrac)/2))

		restart_buttom = QPushButton('RESTART',self)
		restart_buttom.isFlat=True
		restart_buttom.clicked.connect(self.restart)
		restart_buttom.setMinimumSize(QSize(0.9*self.width*(1-boardFrac),
															0.9*self.width*(1-boardFrac)/2))
															
															
		sublayout.addWidget(restart_buttom)

		sublayout.addWidget(pass_buttom)
		
		sublayout.addWidget(cond)
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