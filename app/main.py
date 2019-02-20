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
    snakeHeadX = data["you"]["body"][0]["x"]
    snakeHeadY = data["you"]["body"][0]["y"]
    snakeBodyX = data["you"]["body"][1]["x"]
    snakeBodyY = data["you"]["body"][1]["y"]
    dX = snakeHeadX - snakeBodyX
    dY = snakeHeadY - snakeBodyY
    boardWidth = data["board"]["width"]
    boardHeight = data["board"]["height"]
    foodData = data["food"]

    print data

    boardArray = funcs.getBoardArray(data)

    #Basic AI (Don't run into self or wall)
    vec = funcs.collisionCheck(outputVector, dX, dY, snakeHeadX, snakeHeadY, boardWidth, boardHeight)

    #Final decision:
    directions = ['up', 'down', 'left', 'right'] #string to be returned
    direction = directions[np.argmax(vec)] #Return element of outputVector with highest weight

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
