def collisionCheck(dX, dY, shX, shY, bW, bH):
	#Don't run into self or wall
    if ((dX > 0) or ((shX - 1) < 0)):
        print ">> don't move left"
        #outputVector[2] *= 0
        n = 2
    if ((dX < 0) or ((shX + 1) == bW)):
        print ">> don't move right"
        #outputVector[3] *= 0
        n = 3
    if ((dY > 0) or ((shY - 1) < 0)):
        print ">> don't move up"
        #outputVector[0] *= 0
        n = 0
    if ((dY < 0) or ((shY + 1) == bH)):
        print ">> don't move down"
        #outputVector[1] *= 0
        n = 1

    return n