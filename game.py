from PyQt5.QtWidgets import QApplication, QWidget, QLCDNumber,QGridLayout
from PyQt5.QtGui import QColor, QPainter, QBrush,QMouseEvent,QCursor,QFont, QPixmap
from PyQt5.QtCore import QTimer, QTime, Qt, QObject, QRectF

import numpy as np 
import sys
import gym

from utils import *
from go import *

class GoGame(QWidget):
	# init class
	def __init__(self, size=9, opponent=None ,width=800, height=800):
		super(GoGame, self).__init__()
		# GUI
		self._width = width
		self._height = height
		self._size = int(size)
		self._qp = QPainter()
		self.gridSize =  min(self._width,self._height)/(self._size+1)


		# status
		self.status = GoStatus()
		self.opponent = opponent
		self.reset()

	def __getitem__(self,key):
		return self.status.board[key]
	
	def act(self, coord):
		""" take action at (r,c) """
		#observation, reward, done, info = self.env.step(coord_doge2gym(r,c))
		self.status.play_move(coord)
		if self.opponent!=None:
			self.status.play_move(self.opponent.make_policy(self.status))
		self.update()
		return True

	# reset board
	def reset(self):
		self.status.reset()
		self.update()

	########## Interaction #############
	def mouseReleaseEvent(self, QMouseEvent):
		if QMouseEvent.button() == Qt.LeftButton:
			row = (int)(QMouseEvent.y()//self.gridSize)-1
			col = (int)(QMouseEvent.x()//self.gridSize)-1
			if self.is_inboard((row,col)) and self.is_empty((row, col)):
				print('ACTION: (%d, %d)'%(row, col)) 
				self.act((row,col))
				self.update()	

	def is_empty(self,coord):
		return self.status.board[coord]==colormap['empty']

	def is_inboard(self, coord):
		r, c = coord
		if r>=0 and r<9 and c>=0 and c<9:
			return True
		else:
			return False

	def pass_move(self):
		self.act(None)
		#print('PASS')

	########   GUI   #######
	def paintEvent(self,event):
		#print('[!] Repaint Board...')
		self._qp.begin(self)
		self._paintBoardAndPieces()
		self._qp.end()


	def _paintBoardAndPieces(self):
		cBlack = QColor(50,50,50)
		cWhite = QColor(255,255,255)
		bgColor = QColor(199,163,104) #self._qp.setPen()
		#
		self._qp.setBrush(bgColor)
		b = QBrush()
		b.setTexture(QPixmap('texture.jpg'))
		self._qp.setBrush(b)
		self._qp.drawRect(self.gridSize,self.gridSize, (self._size)*self.gridSize,(self._size)*self.gridSize)
	
		for i in range(self._size-1):
			for j in range(self._size-1):
				# draw line
				self._qp.drawRect((j+1+0.5)*self.gridSize,(i+1+0.5)*self.gridSize, self.gridSize,self.gridSize)
		
		self._qp.setBrush(cBlack)
		d = self.gridSize/10
		for i in [2,4,6]:
			for j in [2,4,6]:
				self._qp.drawEllipse( (i+1+0.5)*self.gridSize-d/2,(j+1+0.5)*self.gridSize-d/2,d,d)

		# draw stone
		d = self.gridSize*4/5
		for i in range(self._size):
			for j in range(self._size):
				if self[i,j]!=colormap['empty']:
					self._qp.setBrush(cWhite if self[i, j]==colormap['white'] else cBlack)
					self._qp.drawEllipse((j+1+0.5)*self.gridSize-d/2,(i+1+0.5)*self.gridSize-d/2,d,d)

		self._qp.setBrush(cBlack)
		font = self._qp.font()
		font.setPixelSize(20)
		self._qp.setFont(font)
		for i in range(self._size):
			self._qp.drawText(QRectF((i+1+0.4)*self.gridSize,0.5*self.gridSize,self.gridSize,self.gridSize), "%c"%(ord('A')+i))
			self._qp.drawText(QRectF(0.5*self.gridSize,(i+1+0.3)*self.gridSize,self.gridSize,self.gridSize), "%d"%(self._size-i) )
	

# give a handler. It will be called when the time is over
class DigitClock(QLCDNumber):
	def __init__(self,size, digits=8,parent=None,handler=None,timeLimit=300):
		super(DigitClock, self).__init__(digits,parent)
		self.handler = handler
		self.timeLimit = timeLimit
		self.timeLeft = timeLimit
		self.display(self.timeLeft)
		self.setDigitCount(digits)
		self.setStyle
		self.setMinimumSize(size[0],size[1])
		#self.resize(size[0],size[1])
		self.timer = QTimer()
		self.timer.timeout.connect(self._update)
		self.timer.start(1000)
		#self.timer.start(1000)
		self.setSegmentStyle(QLCDNumber.Flat)

	def _update(self):
		self.timeLeft -= 1
		if self.handler!=None and self.timeLeft==0:
			self.handler()
			self.resetTime()
		self.display(self.timeLeft)


	def resetTime(self):
		self.timeLeft = self.timeLimit
		self.timer.start(1000)