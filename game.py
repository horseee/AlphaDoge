import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLCDNumber,QGridLayout
from PyQt5.QtGui import QColor, QPainter, QBrush,QMouseEvent,QCursor,QFont, QPixmap
from PyQt5.QtCore import QTimer, QTime, Qt, QObject, QRectF
import numpy as np 

import gym

BLACK = 0
WHITE = 1
colormap = {'BLACK': 0, 'WHITE': 1, 'NONE':-1}
b_offset = 1
class GoEnv(QWidget):
	# init class
	def __init__(self, size=9, width=800, height=800):
		super(GoEnv, self).__init__()
		# GUI
		self._width = width
		self._height = height
		self._size = int(size)
		self._qp = QPainter()
		self.gridSize =  min(self._width,self._height)/(self._size+1)

		#self.env = gym.make('Go9x9-v0')
		#self.env.reset()

		# status
		self.player = colormap['BLACK'] # add new player
		self.board = -1*np.ones(shape=(self._size,self._size))
		self.reset()


	def __getitem__(self,key):
		return self.board[key]
	
	def act(self, r, c):
		""" take action at (r,c) """
		if self.isvalid(r,c) and self[r][c]==-1:
			print(r, c)
			prev_state = self.board.copy()
			self[r][c] = self.player
			capture, capture_list = self.check_capture(r,c)
			dead, chain = self.check_deads(r,c)

			if capture==False and dead==True:
				self[r][c] = -1
				return False
			if capture:
				for coord in capture_list:
					self[coord[0]][coord[1]]=-1
				
			self.player = 1 - self.player

			return True
		return False

	def isvalid(self, r, c):
		if r>=self._size or r<0 or c>=self._size or c<0:
			return False
		return True

	# reset board
	def reset(self):
		self.board = -1*np.ones(shape=(self._size,self._size))
		self.update()

	def check_capture(self, r, c):
		iscaptured=False
		opposite = 1-self[r][c]
		capture_list = []

		if self.isvalid(r-1,c) and self[r-1][c]==opposite:
			iscaptured,chain = self.check_deads(r-1,c)
			if iscaptured:
				for coord in chain:
					if coord not in capture_list:
						capture_list.append(coord)
					

		if self.isvalid(r+1,c) and self[r+1][c]==opposite:
			iscaptured,chain = self.check_deads(r+1,c)
			if iscaptured:
				for coord in chain:
					if coord not in capture_list:
						capture_list.append(coord)
		
		if self.isvalid(r,c-1) and self[r][c-1]==opposite:
			iscaptured,chain = self.check_deads(r,c-1)
			if iscaptured:
				for coord in chain:
					if coord not in capture_list:
						capture_list.append(coord)

		if self.isvalid(r,c+1) and self[r][c+1]==opposite:
			iscaptured,chain = self.check_deads(r,c+1)
			if iscaptured:
				for coord in chain:
					if coord not in capture_list:
						capture_list.append(coord)

		return iscaptured, capture_list

	def do_capture(self, capture_list):
		if len(capture_list)==0: return
		for coord in capture_list:
			self[coord[0]][corrd[1]] = -1	

	def check_deads(self, r, c):
		check_stack = [(r,c)]
		stone_chain = [(r,c)]
		player=self[r][c]
		isdead = True
		while(len(check_stack)>0):
			r, c = check_stack.pop()
			if self.isvalid(r-1,c):
				if self[r-1][c]==-1: isdead=False
				if self[r-1][c]==player and ( (r-1,c) not in stone_chain ):
					stone_chain.append((r-1,c))
					check_stack.append((r-1,c))

			if self.isvalid(r+1,c):
				if self[r+1][c]==-1: isdead=False
				if self[r+1][c]==player and ( (r+1,c) not in stone_chain ):
					stone_chain.append((r+1,c))
					check_stack.append((r+1,c))

			if self.isvalid(r,c-1):
				if self[r][c-1]==-1: isdead=False
				if self[r][c-1]==player and ( (r,c-1) not in stone_chain ):
					stone_chain.append((r,c-1))
					check_stack.append((r,c-1))

			if self.isvalid(r,c+1):
				if self[r][c+1]==-1: isdead=False
				if self[r][c+1]==player and ( (r,c+1) not in stone_chain ):
					stone_chain.append((r,c+1))
					check_stack.append((r,c+1))

		print("chain: ",stone_chain,isdead)
		return isdead, stone_chain
		
	
	




		
		
		

	


	########## Interaction #############
	def mouseReleaseEvent(self, QMouseEvent):
		if QMouseEvent.button() == Qt.LeftButton:
			row = (int)(QMouseEvent.y()//self.gridSize)-1
			col = (int)(QMouseEvent.x()//self.gridSize)-1
			if self.act(row,col):
				self.update()

	########   GUI   #######
	def paintEvent(self,event):
		print('[!] Repaint Board...')
		self._qp.begin(self)
		self._paintBoardAndPieces()
		self._qp.end()

	def _paintBoardAndPieces(self):
		cBlack = QColor(50,50,50)
		cWhite = QColor(255,255,255)
		bgColor = QColor(199,163,104) #self._qp.setPen()

		self._qp.setBrush(bgColor)
		b = QBrush()
		b.setTexture(QPixmap('images.jpg'))
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
				if self[i][j]!=-1:
					self._qp.setBrush(cWhite if self[i][j]==colormap['WHITE'] else cBlack)
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
	def __init__(self,size, digits=8,parent=None,handler=None):
		super(DigitClock, self).__init__(digits,parent)
		self.handler = handler
		self.timeLeft = 60
		self.display(self.timeLeft)
		self.setDigitCount(digits)
		self.setStyle
		self.setMinimumSize(size[0],size[1])
		#self.resize(size[0],size[1])
		self.timer = QTimer()
		self.timer.timeout.connect(self._update)
		self.timer.start(1000)
		self.timer.start(1000)
		self.setSegmentStyle(QLCDNumber.Flat)

	def _update(self):
		self.timeLeft -= 1
		if self.handler!=None and self.timeLeft==0:
			self.handler()
			self.resetTime()
		self.display(self.timeLeft)


	def resetTime(self,t=60):
		self.timeLeft = t 
		self.timer.start(1000)