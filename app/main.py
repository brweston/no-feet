import bottle
import os
import random
import numpy as np
import funcs

from api import *

@bottle.route('/')
def static():
    return "The server is running"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    print "Starting game %s" % data["game"]["id"]
    return StartResponse("#00ff00")


@bottle.post('/move')
def move():
    data = bottle.request.json
    #print data

    #Game board data:
    #Snake head and first body part coords (you)
    snakeHeadX = data["you"]["body"][0]["x"]
    snakeHeadY = data["you"]["body"][0]["y"]
    snakeBodyX = data["you"]["body"][1]["x"]
    snakeBodyY = data["you"]["body"][1]["y"]

    turn = data["turn"]

    #dX, dY are integers for whether the first body part is above, below, right or left of the head (either -1, 0 or 1)
    dX = snakeHeadX - snakeBodyX
    dY = snakeHeadY - snakeBodyY

    boardWidth = data["board"]["width"]
    boardHeight = data["board"]["height"]

    #Genome calculations:
    #a represents the Genome with the weights determined by ML process

    #Get genome values from text file:
    path = "snakeGenomes/gen0_child0.txt"
    g = funcs.getGenome(path)

    #Put genome values into Numpy matrix:
    genome = np.matrix([[float(g[0]), float(g[1]), float(g[2]), float(g[3])], [float(g[4]), float(g[5]), float(g[6]), float(g[7])], [float(g[8]), float(g[9]), float(g[10]), float(g[11])],
               [float(g[12]), float(g[13]), float(g[14]), float(g[15])], [float(g[16]), float(g[17]), float(g[18]), float(g[19])], [float(g[20]), float(g[21]), float(g[22]), float(g[23])],
               [float(g[24]), float(g[25]), float(g[26]), float(g[27])], [float(g[28]), float(g[29]), float(g[30]), float(g[31])], [float(g[32]), float(g[33]), float(g[34]), float(g[35])],
               [float(g[36]), float(g[37]), float(g[38]), float(g[39])]])
        

    #Game data vector
    gameDataVec = np.matrix([[random.random()], [random.random()], [random.random()], [random.random()], [random.random()],
                   [random.random()], [random.random()], [random.random()], [random.random()], [random.random()]])

    genomeTranspose = genome.getT() #Get transpose of a
    outputVector = genomeTranspose*gameDataVec #outputVector => direction weights (1x4 vector)

    #Basic AI (Don't run into self or wall)
    outputVector = funcs.basicAI(outputVector, dX, dY, snakeHeadX, snakeHeadY, boardWidth, boardHeight)
    print "outputVector: ", outputVector


    #Final decision:
    directions = ['up', 'down', 'left', 'right'] #string to be returned
    direction = directions[np.argmax(outputVector)] #Return element of outputVector with highest weight

    #Logs:
    #print outputVector
    print np.argmax(outputVector)
    print direction
    print "SnakeHeadX = ", snakeHeadX, "\n"
    print "SnakeHeadY = ", snakeHeadY, "\n"
    print "Moving %s" % direction

    #Respond to server:
    return MoveResponse(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    print "Data out of function: ", data
    #Excecute end of game tasks
    funcs.causeOfDeath(data)
    #funcs.endGame()

    print "Game %s ended" % data["game"]["id"]


#Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=True)
