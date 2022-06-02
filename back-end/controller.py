from datetime import datetime, timedelta
from flask import Flask, jsonify
from flask_sse import sse
import logging
from flask_apscheduler import APScheduler
from flask_cors import CORS
from threading import Lock

app = Flask(__name__)
CORS(app)
app.config["REDIS_URL"] = 'redis://127.0.0.1:6379'
app.register_blueprint(sse, url_prefix='/stream')
# log = logging.getLogger('apscheduler.executors.default')
# log.setLevel(logging.INFO)
# fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
# h = logging.StreamHandler()
# h.setFormatter(fmt)
# log.addHandler(h)

scheduler = APScheduler()
scheduler.init_app(app)

# Uso a posição 0 da fila como processo na zona crítica
# para diminuir o número de locks necessários

subscribers = []
lock_subscribers = Lock()
subscribers2 = []
lock_subscribers2 = Lock()

def updateStatus(channel: str, msg: str):
    with app.app_context():
        sse.publish(msg, type='message', channel=channel)


class GenericResource(object):
    id_code = '1'

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
                        updateStatus(id + self.id_code, 'HELD')
                    except:
                        print('Acquire Lock error.')
                    else:
                        t = datetime.now() + timedelta(seconds=15)

                        scheduler.add_job(
                            str(datetime.now().timestamp())+id,
                            func=self.release_lock,
                            args=[id],
                            trigger='date',
                            run_date=t
                        )
                        

    def release_lock(self, id) -> None:
        global subscribers
        global lock_subscribers
        global leasing_time

        with lock_subscribers:
            if len(subscribers) == 0:
                pass
            elif id == subscribers[0]:
                subscribers.pop(0)

                updateStatus(id + self.id_code, 'RELEASED')

                if len(subscribers) > 0:
                    try:
                        # Notify the client that he is holding the resource
                        updateStatus(subscribers[0] + self.id_code, 'HELD')
                    except:
                        print('Acquire Lock error.')
                    else:
                        # It sets a timeout for resource usage
                        t = datetime.now() + timedelta(seconds=15)

                        scheduler.add_job(
                            str(datetime.now().timestamp())+subscribers[0],
                            func=self.release_lock,
                            args=[subscribers[0]],
                            trigger='date',
                            run_date=t
                        )

            elif id in subscribers:
                subscribers.remove(id)


class GenericResource2(object):
    id_code = '2'

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
                        updateStatus(id + self.id_code, 'HELD')
                    except:
                        print('Acquire Lock error.')
                    else:
                        # It sets a timeout for resource usage
                        t = datetime.now() + timedelta(seconds=15)

                        scheduler.add_job(
                            str(datetime.now().timestamp())+id,
                            func=self.release_lock,
                            args=[id],
                            trigger='date',
                            run_date=t
                        )
                        

    def release_lock(self, id) -> None:
        global subscribers2
        global lock_subscribers2
        global leasing_time2

        with lock_subscribers2:
            if len(subscribers2) == 0:
                pass
            elif id == subscribers2[0]:
                subscribers2.pop(0)

                updateStatus(id + self.id_code, 'RELEASED')

                if len(subscribers2) > 0:
                    try:
                        # Notify the client that he is holding the resource
                        updateStatus(subscribers2[0] + self.id_code, 'HELD')
                    except:
                        print('Acquire Lock error.')
                    else:
                        # It sets a timeout for resource usage
                        t = datetime.now() + timedelta(seconds=15)

                        scheduler.add_job(
                            str(datetime.now().timestamp())+subscribers2[0],
                            func=self.release_lock,
                            args=[subscribers2[0]],
                            trigger='date',
                            run_date=t
                        )

            elif id in subscribers2:
                subscribers2.remove(id)


resource_a = GenericResource()
resource_b = GenericResource2()

@app.route('/')
def index():
    return jsonify('OK')


@app.route('/acquire/<username>/<resource>')
def acquire(username, resource):
    if resource == '1':
        global resource_a

        scheduler.add_job(
            str(datetime.now().timestamp())+'acquire'+username,
            resource_a.acquire_lock, args=[username]
        )

    else:
        global resource_b

        scheduler.add_job(
            str(datetime.now().timestamp())+'acquire'+username,
            resource_b.acquire_lock, args=[username]
        )

    return jsonify('OK')


@app.route('/release/<username>/<resource>')
def release(username, resource):
    if resource == '1':
        global resource_a

        scheduler.add_job(
            str(datetime.now().timestamp())+'release'+username,
            resource_a.release_lock, args=[username]
        )
    else:
        global resource_b

        scheduler.add_job(
            str(datetime.now().timestamp())+'release'+username,
            resource_b.release_lock, args=[username]
        )

    return jsonify('OK')


@app.route('/connect/<username>')
def connect(username):
    scheduler.add_job(str(datetime.now().timestamp())+updateStatus, args=[username, 'RELEASED'])


if __name__ == '__main__':
    scheduler.start()
    app.run(debug=True, host='0.0.0.0', port=5000)
