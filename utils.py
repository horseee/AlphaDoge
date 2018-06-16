#def toGo(r, c):
#    return r*9+c

#def toCoord(p):
#    return p//9, p%9

def coord_flat2tuple(coord):
    return coord//9, coord%9

def coord_tuple2flat(coord):
    return coord[0]*9+coord[1]

def coord_sgf2tuple(coord):
    if coord=='': return None, None
    #print(coord)
    r = ord(coord[1])-ord('a')
    c = ord(coord[0])-ord('a')
    return (r, c)


colormap = {
        'white': 2,
        'black': 1,
        'empty': 0
}