import os, sys 
import sgf
import numpy as np
from utils import colormap

class SGFLoader(object):
    "Loader for single sgf files"
    def __init__(self, filepath):
        self.open(filepath)

    def open(self, filename):
        self.filepath = filename
        with open(filename, 'rt') as f:
            self.sgf = sgf.parse(f.read())
        self.nodes = self.sgf.children[0].nodes
        self.root = self.sgf.children[0].root
        self.total = len(self.nodes)
        self.step = 0
        self.cur = self.root 
        self.board = np.zeros((9,9))
        self.end=False

    def action_n(self, n):
        assert n>0
        if n>self.total: return None, None
        return coord_str2int(self.nodes[n].properties['B' if n%2==1 else 'W'][0])

    def reset(self):
        self.step = 0
        self.cur = self.root
        self.board = np.zeros((9,9))
        self.end=False

    def is_end(self):
        return self.end

    def state(self):
        return self.board

    def next(self):
        return self._next()
    
    def to(self, n):
        return self._to(n)
    
    def __getitem__(self, key):
        return self.action_n(key)

    def _to(self, n):
        if n<0: n = self.total-n+1 # the last
        assert n>=0
        if self.step>n: self.reset()

        while self.step < n and self.end==False:
            self.next()
        return self.board

    def _next(self):
        if self.cur.next==None:
            #print("End!")
            self.end = True
            return self.board

        self.cur = self.cur.next
        self.step+=1
        player = colormap['black'] if self.step%2==1 else colormap['white']
        r, c = coord_str2int( self.cur.properties['B' if self.step%2==1 else 'W'][0] )
        if r!=None:
            self.board[r,c] = player
            self.check_capture(r,c)
        #print(self.board)
        return self.board

    def check_capture(self, r, c):
        iscaptured=False
        b = self.board
        opposite = colormap['white'] if b[r][c]==colormap['black'] else colormap['black']
        capture_list = []    
        
        if self.isvalid(r-1,c) and b[r-1][c]==opposite:
            iscaptured,chain = self.check_deads(r-1,c)        
            if iscaptured:        
                for coord in chain:        
                    b[coord[0], coord[1]] = colormap['empty']        
                            
        if self.isvalid(r+1,c) and b[r+1][c]==opposite:        
            iscaptured,chain = self.check_deads(r+1,c)        
            if iscaptured:        
                for coord in chain:        
                    b[coord[0], coord[1]] = colormap['empty']        
                
        if self.isvalid(r,c-1) and b[r][c-1]==opposite:        
            iscaptured,chain = self.check_deads(r,c-1)        
            if iscaptured:        
                for coord in chain:        
                    b[coord[0], coord[1]] = colormap['empty']        
        
        if self.isvalid(r,c+1) and b[r][c+1]==opposite:        
            iscaptured,chain = self.check_deads(r,c+1)        
            if iscaptured:        
                for coord in chain:        
                    b[coord[0], coord[1]] = colormap['empty']        
        
        return iscaptured, capture_list


    def isvalid(self, r, c):
        if r>=0 and r<9 and c>=0 and c<9:
            return True
        return False

    def check_deads(self, r, c):        
        check_stack = [(r,c)]        
        stone_chain = [(r,c)]    
        b = self.board
        player= b[r][c]        
        isdead = True        
        while(len(check_stack)>0):        
            r, c = check_stack.pop()        
            if self.isvalid(r-1,c):        
                if b[r-1][c]==colormap['empty']: isdead=False        
                if b[r-1][c]==player and ( (r-1,c) not in stone_chain ):        
                    stone_chain.append((r-1,c))        
                    check_stack.append((r-1,c))        
        
            if self.isvalid(r+1,c):        
                if b[r+1][c]==colormap['empty']: isdead=False        
                if b[r+1][c]==player and ( (r+1,c) not in stone_chain ):        
                    stone_chain.append((r+1,c))        
                    check_stack.append((r+1,c))        
        
            if self.isvalid(r,c-1):        
                if b[r][c-1]==colormap['empty']: isdead=False        
                if b[r][c-1]==player and ( (r,c-1) not in stone_chain ):        
                    stone_chain.append((r,c-1))        
                    check_stack.append((r,c-1))        
        
            if self.isvalid(r,c+1):        
                if b[r][c+1]==colormap['empty']: isdead=False        
                if b[r][c+1]==player and ( (r,c+1) not in stone_chain ):        
                    stone_chain.append((r,c+1))        
                    check_stack.append((r,c+1))        
        
        #print("chain: ",stone_chain,isdead)        
        return isdead, stone_chain
            
def coord_str2int(coord):
    if coord=='': return None, None
    #print(coord)
    r = ord(coord[1])-ord('a')
    c = ord(coord[0])-ord('a')
    return r, c

# 2 white, 1 black, 0 empty
if __name__=='__main__':
    sgf_file = SGFLoader('train/2015/11/10/1.sgf')
    print(sgf_file.to(10))
    print(sgf_file.end)
    print(sgf_file.next())
    print(sgf_file.to(-1))
    print(sgf_file.end)
    print(sgf_file.to(2))
    print(sgf_file.to(-2))


    