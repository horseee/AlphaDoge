# -*- coding: utf-8 -*-  

import argparse
import tensorflow as tf
from model import policy_value_net
from batchLoader import BatchLoader
import os
import numpy as np

def Get_One_Hot(by, player):
	label_by = np.zeros( [len(by) , 9*9+1])
	for i in range(len(by)):
		if by[i] == None:
			label_by[i][81] = player[i]
		else:
			label_by[i][by[i][0]*9 + by[i][1]] = player[i]
	return label_by


if __name__ == '__main__':

	os.environ["CUDA_VISIBLE_DEVICES"] = "2"

	parser = argparse.ArgumentParser()
	parser.add_argument('--learning_rate',type=float,default=0.00003,help='learning rate')
	parser.add_argument('--epoch',type=int,default=300,help='epoch number')
	parser.add_argument('--ckpt',type=str,default='checkpoints/model',help='epoch number')
	parser.add_argument('--batch_size',type=int,default=16,help='batch size')
	args = parser.parse_args()

	data_input = tf.placeholder(dtype='float32',shape=(None, 9, 9, 1))
	label_input = tf.placeholder(dtype='float', shape=(None, 9*9+1)) #考虑PASS
	
	# load model
	net_out = policy_value_net(data_input)

	policy_logits = net_out['policy']
	value = net_out['value']

	policy_loss = tf.losses.softmax_cross_entropy(label_input, policy_logits)
	opt = tf.train.AdamOptimizer(args.learning_rate).minimize(policy_loss)

	# deployment and save checkpoint
	tf_config = tf.ConfigProto()
	tf_config.gpu_options.allow_growth = True
	sess = tf.Session(config=tf_config)
	try: 
		os.mkdir('checkpoints')
	except: 
		pass 
	sess.run(tf.global_variables_initializer())
	saver =  tf.train.Saver(tf.global_variables())

	try:
		if os.path.exists('checkpoints'):
			saver.restore(sess, args.ckpt)
			print('[!] Model restored from %s'%(args.ckpt))
		else: 
			print('[!] No checkpoints!')
	except:
		print('[!] No checkpoints!')

	batch_train = BatchLoader(dir='train')
	batch_validation = BatchLoader(dir='validation', batch_size = 1)
	for ep in range(args.epoch):
		total_loss = []
	
		while not batch_train.end_batch():
			bX, by, player = batch_train.get_batch()
			label_by = Get_One_Hot(by, player)
			bX = np.reshape(bX, [-1, 9, 9, 1])
			_, cur_loss = sess.run([opt, policy_loss], {data_input: bX, label_input: label_by})
			total_loss.append(cur_loss)
		
		print('[*] epoch %d, average loss = %f'%(ep, np.mean(total_loss)))
		saver.save(sess, args.ckpt)

		batch_train.reset_batch()

		correct = 0
		total_game = 0

		while not batch_validation.end_batch():
			bX, by, player = batch_validation.get_batch()
			bX = np.reshape(bX, [-1, 9, 9, 1])
			res = sess.run([logits], {data_input: bX})
			predicts  = np.argmax(res,axis=1)
			if by == None and predicts == 81:
				correct = correct + 1
			elif by[0] * 9 + by[1] == predicts:
				correct = correct + 1
			total_game += 1
			
		print("[!] %d validation data, accuracy = %f"%(total_game, correct / total_game))

