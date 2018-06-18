from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import numpy as np 
import sys
import gym

from utils import *
from go import *
from Opponents import decisionThread

class GoGame(QWidget):
	# init class
	def __init__(self, size=9, opponent=None ,width=800, height=800, condition=None, reset_clock=None):
		super(GoGame, self).__init__()
		# GUI
		self.status = GoStatus()
		self._width = width
		self._height = height
		self._size = int(size)
		self._qp = QPainter()
		self.gridSize =  min(self._width,self._height)/(self._size+1)
		self.latest = None
		self.condition = condition
		self.reset_clock = reset_clock
		self.oppo_thread = decisionThread(self.status)
		self.oppo_thread.tuple_signal.connect(self._opponent_done)
		self.user = colormap['black']
		# status
		
		self.opponent = opponent
		self.reset()

	def _opponent_done(self, coord):
		if coord==(-1,-1): coord=None
		self.status.play_move(coord)
		self.latest = coord
		self.update_cond()
		self.update()

	def __getitem__(self,key):
		return self.status.board[key]

	def update_cond(self, winner=None):
		self.reset_clock()
		if winner!=None:
			self.condition.setText('Game Over, winner is %s'%winner)
		elif self.status.to_play==colormap['black']:
			self.condition.setText('TO PLAY: BLACK')
		elif self.status.to_play==colormap['white']:
			self.condition.setText('TO PLAY: WHITE')

	def act(self, coord):
		""" take action at (r,c) """
		#observation, reward, done, info = self.env.step(coord_doge2gym(r,c))
		success = self.status.play_move(coord)
		print(success)
		if success==True and self.opponent!=None:
			self.latest = coord
			self.update_cond()
			self.oppo_thread.set_status(self.status)
			self.oppo_thread.start()
			#move = self.opponent.make_policy(self.status)
			#self.status.play_move(move)
		self.update_cond()
		self.update()
		return True

	# reset board
	def restart(self):
		if self.user==self.status.to_play:
			self.reset()

	def reset(self):
		self.status.reset()
		self.update_cond()
		self.reset_clock()
		self.update()

	########## Interaction #############
	def mouseReleaseEvent(self, QMouseEvent):
		if QMouseEvent.button() == Qt.LeftButton:
			row = (int)(QMouseEvent.y()//self.gridSize)-1
			col = (int)(QMouseEvent.x()//self.gridSize)-1
			if self.user==self.status.to_play and self.is_inboard((row,col)) and self.is_empty((row, col)):
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
		if self.status.to_play==self.user:
			self.act(None)
			if self.status.is_game_over():
				score = self.status.get_score()
				winner = 'BLACK'
				if score<0: winner='WHITE'
				self.update_cond(winner)
				print("Game Over! The winner is %s"%(winner))
				#self.reset()
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
		markColor = QColor(140,140,140)
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
					if self.latest == (i,j):
						self._qp.setBrush(markColor)
						self._qp.drawRoundedRect( QRectF((j+1+0.5)*self.gridSize-d/2+d/3,(i+1+0.5)*self.gridSize-d/2+d/3,d/3,d/3),1,1 )


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
		self.update()