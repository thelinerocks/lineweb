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
            socketio.emit('points', {"p": redis_store.lindex(k, 0)})

def broadcast_mentions():
    while True:
        time.sleep(1)
        keys = redis_store.keys(pattern="mentions-*")
        for k in keys:
            if redis_store.llen(k) == 0:
                continue
            element = redis_store.lpop(k)

            socketio.emit('mentions'.format(k), json.loads(element))

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
    tag1 = "#ichackupper"
    tag2 = "#ichacklower"
    tag_data = {
        tag1 : get_data_for_hashtag(tag1),
        tag2 : get_data_for_hashtag(tag2)
    }
    return flask.render_template("index.html", tag_data=tag_data)
