import os
import dataLoader
import numpy as np

class SGF_file_reader(object):

	
	def __init__(self, batch_size):
		self.batch_size = batch_size
		self.loadfileArray = ['./train/2015', './train/2016', './train/2017', './train/2018']
		self.loadfile = []
		self.loadfile_ptr = 0
		self.SgfPath = []
		self.Sgf_file = []
	
	def GetOneBatch(self):
		while len(self.Sgf_file) < self.batch_size:
			if len(self.SgfPath) == 0 and self.loadfile_ptr > 3:
				break
			if len(self.SgfPath) == 0:
				self.appendSgfPath()
			self.Sgf_file.append(dataLoader.SGFLoader(self.SgfPath.pop()))

		batch_input = np.zeros(self.batch_size, 9, 9, 1)
		for itr in self.batch_size:
			if (self.Sgf_file[itr])
			batch_input[itr] = np.shape(self.Sgf_file[itr].next().board, [9, 9, 1])
			if self.Sgf_file[itr].peek_next_action()
				batch_input.remove


		return batch_input

	def appendSgfPath(self):
		self.loadfile.append(self.loadfileArray[loadfile_ptr])
		while self.loadfile:
			path = self.loadfile.pop()
			for filepath in os.listdir(path):
				if os.path.isfile(os.path.join(path, filepath)):
					self.SgfPath.append(os.path.join(path, filepath))
				else:
					self.loadfile.append(os.path.join(path, filepath))
		self.loadfile_ptr = self.loadfile_ptr + 1
