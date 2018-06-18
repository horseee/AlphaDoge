#def toGo(r, c):
#    return r*9+c

#def toCoord(p):
#    return p//9, p%9
import numpy as np
def coord_flat2tuple(coord):
    if coord==81: return None
    return coord//9, coord%9

def coord_tuple2flat(coord):
    if coord==None: return 81
    return coord[0]*9+coord[1]

def coord_sgf2tuple(coord):
    if coord=='': return None
    #print(coord)
    r = ord(coord[1])-ord('a')
    c = ord(coord[0])-ord('a')
    return (r, c)

def to_one_hot(p):
    if isinstance(p, int):
        one_hot = np.zeros((9*9+1))
        one_hot[p] = 1
        return one_hot
    else: 
        one_hot = np.zeros((len(p),9*9+1))
        for i in range(len(p)):
            one_hot[i,p[i]] = 1
        return one_hot

def logits2prob(logits):
    probs = np.exp(logits)
    probs = probs/np.sum(probs)
    return probs

colormap = {
        'white': 1,
        'black': -1,
        'empty': 0
}
