import bottle
import os
import random
import numpy as np

from api import *

#Defining variables:
#print(outputVector)
#print(np.argmax(outputVector))

#Routes:
@bottle.route('/')
def static():
    return "the server is running"


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

    #Genome calculations:
    a = np.matrix([[random.random(), random.random(), random.random(), random.random()], [random.random(), random.random(), random.random(), random.random()], [random.random(), random.random(), random.random(), random.random()],
               [random.random(), random.random(), random.random(), random.random()], [random.random(), random.random(), random.random(), random.random()], [random.random(), random.random(), random.random(), random.random()],
               [random.random(), random.random(), random.random(), random.random()], [random.random(), random.random(), random.random(), random.random()], [random.random(), random.random(), random.random(), random.random()],
               [random.random(), random.random(), random.random(), random.random()]])

    b = np.matrix([[random.random()], [random.random()], [random.random()], [random.random()], [random.random()],
                   [random.random()], [random.random()], [random.random()], [random.random()], [random.random()]])
    aTranspose = a.getT()
    outputVector = aTranspose*b

    #Get game board data
    snakeHeadX = data["you"]["body"][0]["x"]
    snakeHeadY = data["you"]["body"][0]["y"]
    snakeBodyX = data["you"]["body"][1]["x"]
    snakeBodyY = data["you"]["body"][1]["y"]

    dX = snakeHeadX - snakeBodyX
    dY = snakeHeadY - snakeBodyY

    print "SnakeHeadX = ", snakeHeadX, "\n"
    print "SnakeHeadY = ", snakeHeadY, "\n"

    boardWidth = data["board"]["width"]
    boardHeight = data["board"]["height"]

    #Don't run into self or wall
    if ((dX > 0) or ((snakeHeadX - 1) < 0)):
        #don't move left
        print "don't move left"
        outputVector[2] *= 0
    if ((dX < 0) or ((snakeHeadX + 1) == boardWidth)):
        #don't move right
        print "don't move right"
        outputVector[3] *= 0
    if ((dY > 0) or ((snakeHeadY - 1) < 0)):
        #don't move up
        print "don't move up"
        outputVector[0] *= 0
    if ((dY < 0) or ((snakeHeadY + 1) == boardHeight)):
        #don't move down
        print "don't move down"
        outputVector[1] *= 0


    directions = ['up', 'down', 'left', 'right']
    print outputVector
    direction = directions[np.argmax(outputVector)]

    print "Moving %s" % direction
    return MoveResponse(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    print "Game %s ended" % data["game"]["id"]


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=True)
