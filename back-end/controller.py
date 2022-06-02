from flask import Flask, jsonify
from flask_sse import sse
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS
from threading import Thread
from threading import Lock
from time import time_ns
from RepeatTimer import RepeatTimer
from redis import Redis

redis = Redis.from_url('redis://localhost:6379')
redis.flushall(asynchronous=False)

user = {}

app = Flask(__name__)
CORS(app)
app.config["REDIS_URL"] = 'redis://127.0.0.1:6379'
app.register_blueprint(sse, url_prefix='/stream')
log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.INFO)
fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)

def print_status():
    print('Queue1: {0}   Queue2: {1}                              '
          .format(subscribers, subscribers2), end='\r')


def updateStatus(usr: str, msg: str):
    with app.app_context():
        sse.publish(msg, type='message', channel=usr)


DEFALUT_LEASING_TIME = 15000000000

# Uso a posição 0 da fila como processo na zona crítica
# para diminuir o número de locks necessários

subscribers = []
leasing_time = None
lock_leasing_time = Lock()
lock_subscribers = Lock()
subscribers2 = []
lock_subscribers2 = Lock()
leasing_time2 = None
lock_leasing_time2 = Lock()


class GenericResource(object):
    def acquire_lock(self, id) -> None:
        global subscribers
        global lock_subscribers
        global leasing_time

        with lock_subscribers:
            if id not in subscribers:
                subscribers.append(id)

                if len(subscribers) == 1:
                    try:
                        # Notify the client that he is holding the resource
                        updateStatus(id, 'HELD')
                    except:
                        print('Acquire Lock error.')
                    else:
                        # It sets a timeout for resource usage
                        with lock_leasing_time:
                            leasing_time = time_ns() + DEFALUT_LEASING_TIME

                        

    def release_lock(self, id) -> None:
        global subscribers
        global lock_subscribers
        global leasing_time

        with lock_subscribers:
            if len(subscribers) == 0:
                pass
            elif id == subscribers[0]:
                subscribers.pop(0)

                if len(subscribers) > 0:
                    try:
                        # Notify the client that he is holding the resource
                        updateStatus(subscribers[0], 'HELD')
                    except:
                        print('Acquire Lock error.')
                    else:
                        # It sets a timeout for resource usage
                        with lock_leasing_time:
                            leasing_time = time_ns() + DEFALUT_LEASING_TIME
                else:
                    with lock_leasing_time:
                        leasing_time = None

            elif id in subscribers:
                subscribers.remove(id)


class GenericResource2(object):
    def acquire_lock(self, id) -> None:
        global subscribers2
        global lock_subscribers2
        global leasing_time2

        with lock_subscribers2:
            if id not in subscribers2:
                subscribers2.append(id)

                if len(subscribers2) == 1:
                    try:
                        # Notify the client that he is holding the resource
                        updateStatus(id, 'HELD')
                    except:
                        print('Acquire Lock error.')
                    else:
                        # It sets a timeout for resource usage
                        with lock_leasing_time2:
                            leasing_time2 = time_ns() + DEFALUT_LEASING_TIME

    def release_lock(self, id) -> None:
        global subscribers2
        global lock_subscribers2
        global leasing_time2

        with lock_subscribers2:
            if len(subscribers2) == 0:
                pass
            elif id == subscribers2[0]:
                subscribers2.pop(0)

                if len(subscribers2) > 0:
                    try:
                        # Notify the client that he is holding the resource
                        updateStatus(subscribers2[0], 'HELD')
                    except:
                        print('Acquire Lock error.')
                    else:
                        # It sets a timeout for resource usage
                        with lock_leasing_time2:
                            leasing_time2 = time_ns() + DEFALUT_LEASING_TIME
                else:
                    with lock_leasing_time2:
                        leasing_time2 = None

            elif id in subscribers2:
                subscribers2.remove(id)


class PyScheduler(Thread):
    def __init__(self) -> None:
        super(PyScheduler, self).__init__()

    def run(self) -> None:
        global subscribers
        global lock_subscribers
        global leasing_time
        global subscribers2
        global lock_subscribers2
        global leasing_time2

        while True:
            if leasing_time is not None:
                flag = False

                with lock_leasing_time:
                    # Removing access from current user
                    if leasing_time - time_ns() < 0:
                        flag = True
                        leasing_time = None

                if flag:
                    with lock_subscribers:
                        if len(subscribers) > 0:
                            released_id = subscribers.pop(0)

                            try:
                                # Notify the client that he released the resource
                                updateStatus(released_id, 'RELEASED')
                            except:
                                print('Release Lock error.')

                            if len(subscribers) > 0:
                                try:
                                    # Notify the client that he is holding the resource
                                    updateStatus(subscribers[0], 'HELD')
                                except:
                                    print('Acquire Lock error.')
                                else:
                                    # It sets a timeout for resource usage
                                    with lock_leasing_time:
                                        leasing_time = time_ns() + DEFALUT_LEASING_TIME

            if leasing_time2 is not None:
                flag2 = False

                with lock_leasing_time2:
                    if leasing_time2 - time_ns() < 0:
                        flag2 = True
                        leasing_time2 = None

                if flag2:
                    with lock_subscribers2:
                        if len(subscribers2) > 0:
                            released_id = subscribers2.pop(0)

                            try:
                                # Notify the client that he released the resource
                                updateStatus(released_id, 'RELEASED')
                            except:
                                print('Release Lock error.')

                            if len(subscribers2) > 0:
                                try:
                                    # Notify the client that he is holding the resource
                                    updateStatus(subscribers2[0], 'HELD')
                                except:
                                    print('Acquire Lock error.')
                                else:
                                    # It sets a timeout for resource usage
                                    with lock_leasing_time2:
                                        leasing_time2 = time_ns() + DEFALUT_LEASING_TIME


@app.route('/')
def index():
    return jsonify('OK')


@app.route('/acquire/<username>/<resource>')
def acquire(username, resource):
    if resource == '1':
        pass
    else:
        pass


@app.route('/release/<username>/<resource>')
def release(username, resource):
    if resource == '1':
        pass
    else:
        pass


@app.route('/connect/<username>')
def connect(username):
    user[username] = {}

    user[username]['status'] = 'RELEASED'

    sched.add_job(updateStatus, args=[username, 'RELEASED'])


if __name__ == '__main__':
    sched = BackgroundScheduler(daemon=True)
    sched.start()

    task_scheduler = PyScheduler()
    task_scheduler.start()

    RepeatTimer(2, print_status).start()

    app.run(debug=True, host='0.0.0.0', port=5000)
