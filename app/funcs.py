def collisionCheck(vec, dX, dY, sHX, sHY, bW, bH):
    #vec represents the vector of direction weights
    #dX and dY represent whether the second body part is above, below, left or right of the head (-1, 0 or 1)
    #sHX and sHY are coords of snake head
    #bW and bH are dimensions of board

    if ((dX > 0) or ((sHX - 1) < 0)):
        #print ">> don't move left"
        vec[2] = 0
    if ((dX < 0) or ((sHX + 1) == bW)):
        #print ">> don't move right"
        vec[3] = 0
    if ((dY > 0) or ((sHY - 1) < 0)):
        #print ">> don't move up"
        vec[0] = 0
    if ((dY < 0) or ((sHY + 1) == bH)):
        #print ">> don't move down"
        vec[1] = 0
    #print "vec: ", vec
    return vec

def getBoardArray(boardData):
    arr = 0
    #foodData = boardData
    return arr