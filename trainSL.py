import argparse
import tensorflow as tf
from model import policy_value_net


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--learning_rate',type=float,default=0.00003,help='learning rate')
	parser.add_argument('--epochs',type=int,default=100,help='epoch number')
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

	if os.path.exists('checkpoints'):
		saver.restore(sess, args.ckpt)
		print('[!] Model restored from %s'%(args.ckpt))
	else: 
		print('[!] No checkpoints!')



	#for ep in range(epoch):

		# total_loss = []
		# batch_input = SGF_file.SGF_file_reader(batch_size)
		# _, cur_loss = sess.run([opt, loss], {data_input: batch_input, label_input: batch_labels})
        # total_loss.append(cur_loss)

    #print('[*] epoch %d, average loss = %f'%(ep, np.mean(total_loss))
    #saver.save(sess, args.ckpt)