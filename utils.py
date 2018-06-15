def toGo(r, c):
    return r*9+c

def toCoord(p):
    return p//9, p%9

colormap = {
        'white': 2,
        'black': 1,
        'empty': 0
}