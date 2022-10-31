# Arboretum

## About The Project

This is an implementation of the [Arboretum](https://boardgamegeek.com/boardgame/140934/arboretum) boardgame created by [Dan Cassar](http://dancassar.com/)

This implementation is built by me purely for learning purposes and to be able to play with my friends online
since no digital version exists.

The game can currently be played by 2-3 players. 

## Built With

* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com)
* [SocketIO](https://socket.io/)
* [Javascript](https://developer.mozilla.org/fr/docs/Web/JavaScript)
* [CSS](https://developer.mozilla.org/fr/docs/Web/CSS)
* [HTML](https://developer.mozilla.org/fr/docs/Web/HTML)

### Flask Extensions used

* [Flask SocketIO](https://flask-socketio.readthedocs.io)

## Running the game
Environment variables. Can be set in the .env file or in the operating system.

| Variable | Example Value 
| :---:   |:-------------:|
| SECRET_KEY |  "my_secret"  |

## Running the game

Navigate to the same folder as the app.py file and execute:
```
python -m flask run
```

To run in debug
```
python -m flask --debug run
```
