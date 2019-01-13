def basicAI(vec, dX, dY, sHX, sHY, bW, bH):
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

def getGenome(fileName):
    #Returns a 1D array (type double) of the genome values stored in a text file
    with open(fileName, 'r') as genomeFile:
        #g is a placeholder array for the genome matrix
        g = genomeFile.read().replace('\n', ' ') #remove new line characters
        g = g.split(' ') #seperate values into 1D array

    return g

def endGame():
    # Stuff to do when snake dies:

    return 0
    # Check genome level
    # Reproduce if level is high enough
    # Change weights of child genomes to reflect cause of death

def causeOfDeath(data):
    print "Data in function: ", data

    if (data["you"]["health"] == 0):
        #Snake died of starvation
        print "Starvation"

    snakeCoords = data["you"]["body"]
    for snakeBodyPart in snakeCoords:
        for snake
    return 0