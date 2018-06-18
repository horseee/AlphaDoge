#def toGo(r, c):
#    return r*9+c

#def toCoord(p):
#    return p//9, p%9

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

colormap = {
        'white': 1,
        'black': -1,
        'empty': 0
}