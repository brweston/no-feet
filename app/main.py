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
    a = np.matrix([[0.2, 0.5, 0.4, 0.3], [0.6, 0.9, 0.5, 0.2], [0.2, 0.1, 0.8, 0.7],
               [0.3, 0.5, 0.2, 0.5], [0.2, 0.7, 0.4, 0.9], [0.3, 0.3, 0.7, 0.1],
               [0.2, 0.5, 0.6, 0.9], [0.6, 0.2, 0.4, 0.6], [0.2, 0.6, 0.8, 0.2],
               [0.6, 0.8, 0.6, 0.9]])

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

    if (dX > 0):
        #dont' move left
        outputVector[2] *= 0
    elif (dX < 0):
        #don't move right
        outputVector[3] *= 0
    elif (dY > 0):
        #don't move up
        outputVector[0] *= 0
    elif (dY < 0):
        #don't move down
        outputVector[1] *= 0

    directions = ['up', 'down', 'left', 'right']
    direction = directions[np.argmax(outputVector)]
    #direction = random.choice(directions)

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
