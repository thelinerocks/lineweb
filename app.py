import flask
import flask_redis
import flask_socketio
import time
import threading
import json

redis_store = flask_redis.FlaskRedis()
socketio = flask_socketio.SocketIO()

def get_data_for_hashtag(tag):
    return redis_store.lrange(tag, 0, 1000)

def broadcast_thread():
    while True:
        # sleeping for 50ms
        time.sleep(0.2)
        # get all keys for datapoints:
        keys = redis_store.keys(pattern="points-*")
        for k in keys:
            category = k.decode("utf-8").partition('-')[2]
            val = redis_store.lindex(k, 0)
            socketio.emit('points', {"p": float(val)}, namespace="/{}".format(category))

def broadcast_mentions():
    while True:
        time.sleep(2)
        keys = redis_store.keys(pattern="mentions-*")
        for k in keys:
            category = k.decode("utf-8").partition('-')[2]
            if redis_store.llen(k) == 0:
                continue
            element = redis_store.lpop(k)
            try:
                jelement = json.loads(element)
            except ValueError:
                continue
            socketio.emit('mentions'.format(k), jelement, namespace="/{}".format(category))

#, namespace="/{}".format(k)
def create_app():
    app = flask.Flask(__name__)
    redis_store.init_app(app)
    socketio.init_app(app)

    thread = threading.Thread(target=broadcast_thread)
    thread.daemon = True
    thread.start()

    thread = threading.Thread(target=broadcast_mentions)
    thread.daemon = True
    thread.start()
    return app

app = create_app()

@app.route("/")
def line():
    left = {
        "category": "ichackupper",
        "data": get_data_for_hashtag("ichackupper")
    }
    right = {
        "category": "ichacklower",
        "data": get_data_for_hashtag("ichacklower")
    }

    return flask.render_template("index.html", left=left, right=right)
