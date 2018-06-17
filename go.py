from utils import *
import numpy as np
from copy import deepcopy

def get_neighbor(b, coord):
    r, c = coord
    neighbor = []
    for nei in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]:
        if is_inboard(nei[0],nei[1]): 
            neighbor.append(nei)
    return neighbor

def get_opposite(color):
    return colormap['white'] if color==colormap['black'] else colormap['black']

def is_ko(b, coord):
    r, c = coord
    if b[r,c]!=colormap['empty']:
        return None
    neighbors = get_neighbor(b, coord)
    neighbor_color = {b[ncoord] for ncoord in neighbors}
    if len(neighbor_color)==1 and not (colormap['empty'] in neighbor_color):
        return list(neighbor_color)[0]
    else:  
        return None

def place_stones(board, color, stones):
    for s in stones:
        board[s] = color

def is_inboard(r, c):
    if r>=0 and r<9 and c>=0 and c<9:
        return True
    else:
        return False

def find_reached(board, c):
    color = board[c]
    chain = set([c])
    reached = set()
    frontier = [c]
    while frontier:
        current = frontier.pop()
        chain.add(current)
        neighbors = get_neighbor(board,current)
        for n in neighbors:
            if board[n] == color and not n in chain:
                frontier.append(n)
            elif board[n] != color:
                reached.add(n)
    return chain, reached


class GoStatus(object):
    def __init__(self, komi=7.0):
        self.board = np.zeros(shape=(9,9))
        self.to_play = colormap['black']
        self.ko=None
        self.n=0
        self.recent = []
        self.komi = komi
    
    def __repr__(self):
        return '%s'%self.board

    def __getitem__(self,key):
        return self.board[key]

    def get_status(self):
        return self.board

    def copy(self):
        return deepcopy(self)

    def is_game_over(self):
        return (len(self.recent) >= 2
                and self.recent[-1] is None
                and self.recent[-2] is None)

    def get_legal_moves(self):
        legal_map = np.zeros((9*9+1))
        legal_map[-1] = 1
        for i in range(9):
            for j in range(9):
                if self.is_move_legal((i,j)):
                    legal_map[i*9+j] = 1
        return legal_map

    def play_move(self, coord, color=None):
        if self.is_game_over(): 
            print('Game Over!')
            print(self.get_score())
            return False

        b = self.board
        if color==None: color=self.to_play
        opposite = get_opposite(color)
        if coord==None:
            self.n+=1
            self.recent.append(coord)
            self.change_player()
            return True
        if not self.is_move_legal(coord):
            return False
        poential_ko = is_ko(self.board, coord)
        b[coord]=color

        is_captured, capture_list = self.check_capture(coord, do_capture=True)
        if len(capture_list)==1 and poential_ko==opposite:
            new_ko = capture_list[0]
        else: new_ko = None
        self.ko = new_ko
        self.change_player()
        self.recent.append(coord)
        self.n+=1

        return True

    def reset(self):
        self.to_play = colormap['black']
        self.board = np.zeros(shape=(9,9))
        self.ko=None
        self.recent = []
        self.n=0

    def get_score(self):
        UNKNOWN=5
        working_board = np.copy(self.board)
        while colormap['empty'] in working_board:
            unassigned_spaces = np.where(working_board == colormap['empty'])
            c = unassigned_spaces[0][0], unassigned_spaces[1][0]
            territory, borders = find_reached(working_board, c)
            border_colors = set(working_board[b] for b in borders)
            X_border = colormap['black'] in border_colors
            O_border = colormap['white'] in border_colors
            if X_border and not O_border:
                territory_color = colormap['black']
            elif O_border and not X_border:
                territory_color = colormap['white']
            else:
                territory_color = UNKNOWN  # dame, or seki
            place_stones(working_board, territory_color, territory)
        return np.count_nonzero(working_board == colormap['black']) - np.count_nonzero(working_board == colormap['white']) - self.komi

    def is_move_suicidal(self, coord):
        b = self.board
        b[coord]=self.to_play
        iscaptured, capture_list = self.check_capture(coord,do_capture=False)
        isdead, stone_chain = self.check_deads(coord)
        b[coord]=colormap['empty']
        if iscaptured==False and isdead==True:
            return True
        else: return False

    def is_move_legal(self, coord):
        b = self.board
        if coord==None:
            return True
        r, c = coord
        if b[r,c]!=colormap['empty']: 
            #print('nonempty')
            return False
        if coord == self.ko:
            #print('ko')
            return False
        if self.is_move_suicidal(coord):
            #print('suic')
            return False
        return True

    def change_player(self):
        if self.to_play==colormap['black']:
            self.to_play=colormap['white']
        else: self.to_play = colormap['black']

    def capture(self, capture_list):
        for stone in capture_list:
            self.board[stone] = colormap['empty']

    def check_capture(self, coord, do_capture=False):
        r, c = coord
        iscaptured=False
        b = self.board
        opposite = get_opposite(b[coord])
        capture_list = []    
        neighbors = get_neighbor(self.board, coord)
        #print(neighbors)
        for nei in neighbors:
            if b[nei]==opposite:
                cap, chain = self.check_deads(nei)
                #print(iscaptured, chain)
                if cap:
                    capture_list.extend(chain)
                    iscaptured=True
        if do_capture and len(capture_list)>0:
            self.capture(capture_list)
        
        return iscaptured, capture_list

    def check_deads(self, coord):  
        r,c = coord
        check_stack = [coord]        
        stone_chain = [coord]    
        b = self.board
        player= b[coord]        
        isdead = True     
        while(len(check_stack)>0):        
            coord = check_stack.pop()    
            neighbors = get_neighbor(self.board,coord)
            for nei in neighbors:
                if b[nei]==colormap['empty']: isdead=False 
                if b[nei]==player and ( nei not in stone_chain ):        
                    stone_chain.append(nei)        
                    check_stack.append(nei)        
        return isdead, stone_chain
