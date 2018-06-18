from dataLoader import SGFLoader
from scipy.io import savemat
import glob

def merge_dataset(dir='train', to_file='data/data'):
    filenames = glob.glob(dir+'/**/*.sgf',recursive=True)
    print("[!] %d data loaded from %s"%(len(filenames), dir))
    X = []
    p = []
    v = []
    f_id = 0
    for i in range(len(filenames)):
        Xi, pi, vi = make_dataset_from_sgf(filenames[i])
        X.extend(Xi)
        p.extend(pi)
        v.extend(vi)
        #print(X,p,v)
        #if i==3: return 
        if i%100==0:
            print('%d/%d'%(i,len(filenames)))

        if i%10000==0 and i>0:
            savemat(to_file+'_%d'%f_id, {'X':X,'p':p,'v':v})
            print('saved as %s_%d.mat'%(to_file,f_id))
            X = []
            p = []
            v = []
            f_id+=1

    if len(X)>0: # save the rest
         savemat(to_file+'_%d'%f_id, {'X':X,'p':p,'v':v})
         print('saved as %s_%d.mat'%(to_file,f_id))
    

def make_dataset_from_sgf(sgf_name):
    sgf_reader = SGFLoader(sgf_name)
    X = []
    p = []
    v = []
    while not sgf_reader.is_end():
        next_action = sgf_reader.peek_next_action()
        if next_action==None: 
            next_action = 81 # pass
        elif next_action==-1: break
        else: next_action = next_action[0]*9+next_action[1]

        X.append(sgf_reader.status.board * sgf_reader.status.to_play)
        p.append(next_action)
        v.append(sgf_reader.value * sgf_reader.status.to_play)
        sgf_reader.next()
    return X, p, v

if __name__=='__main__':
    merge_dataset()#
    #filenames = glob.glob('train/**/*.sgf',recursive=True)
    #print(filenames[58913])
    #Xi, pi, vi = make_dataset_from_sgf(filenames[58913])