import os
from dataLoader import SGFLoader
import numpy as np
import glob

class BatchLoader(object):

	def __init__(self, dir='train', batch_size=16):
		self.batch_size = batch_size
		self.dir = dir
		self.filenames = glob.glob(self.dir+'/**/*.sgf',recursive=True)
		print("[!] %d data loaded from %s"%(len(self.filenames), self.dir))
		self.file_idx = 0
		self.sgf_list = []

	def update(self):
		i=0
		for i in range(len(self.sgf_list)):
			if self.sgf_list[i].is_end():
				self.sgf_list[i] = self._get_new_sgf()
	
		while i<self.batch_size-1: # fill the rest
			self.sgf_list.append(self._get_new_sgf())
			i+=1

	def _get_new_sgf(self):
		new_sgf = SGFLoader( self.filenames[self.file_idx] )
		self.file_idx+=1

		if self.file_idx==len(self.filenames):
			self.file_idx=0 # reset
		return new_sgf

	def get_batch(self):
		self.update()
		X = []
		y = []
		player = []
		for i in range(len(self.sgf_list)):
			X.append(self.sgf_list[i].status.board * self.sgf_list[i].status.to_play)				# current board
			y.append(self.sgf_list[i].peek_next_action()) # the next action
			player.append(-1 * self.sgf_list[i].status.to_play)
			self.sgf_list[i].next()
		return np.array(X), y, player

	def reset_batch(self):
		self.sgf_list = []
		self.file_idx = 0

	def end_batch(self):
		if self.file_idx + self.batch_size >= len(self.filenames):
			return True
		else:
			return False

#if __name__=='__main__':
#	batch = BatchLoader(dir='train')
#	for i in range(10):
#		bX, by, player = batch.get_batch()
#		print(by)
	