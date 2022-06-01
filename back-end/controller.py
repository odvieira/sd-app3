from threading import Thread
from threading import Lock
from time import time_ns
from RepeatTimer import RepeatTimer

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
                    res = "HELD {0}".format(subscribers)
                    try:
                        # Notify the client that he is helding the resource
                        remote_ref_callback = Proxy(
                            "PYRONAME:client{0}.callback"
                            .format(subscribers[0]))
                    except:
                        print('Acquire Lock error.')
                    else:
                        # It sets a timeout for resource usage
                        with lock_leasing_time:
                            leasing_time = time_ns() + DEFALUT_LEASING_TIME

                        message = '{0} {1}'.format(
                            str(type(self))[17:-2], res).encode()

                        remote_ref_callback.notify(
                            message.decode()
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

                if len(subscribers) > 0:
                    res = "HELD {0}".format(subscribers)
                    try:
                        # Notify the client that he is helding the resource
                        remote_ref_callback = Proxy(
                            "PYRONAME:client{0}.callback"
                            .format(subscribers[0]))
                    except:
                        print('Acquire Lock error.')
                    else:
                        # It sets a timeout for resource usage
                        with lock_leasing_time:
                            leasing_time = time_ns() + DEFALUT_LEASING_TIME

                        message = '{0} {1}'.format(
                            str(type(self))[17:-2], res).encode()

                        remote_ref_callback.notify(
                            message.decode()
                        )

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
                    res = "HELD {0}".format(subscribers2)
                    try:
                        # Notify the client that he is helding the resource
                        remote_ref_callback = Proxy(
                            "PYRONAME:client{0}.callback"
                            .format(subscribers2[0]))
                    except:
                        print('Acquire Lock error.')
                    else:
                        # It sets a timeout for resource usage
                        with lock_leasing_time2:
                            leasing_time2 = time_ns() + DEFALUT_LEASING_TIME

                        message = '{0} {1}'.format(
                            str(type(self))[17:-2], res).encode()

                        remote_ref_callback.notify(
                            message.decode()
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

                if len(subscribers2) > 0:
                    res = "HELD {0}".format(subscribers2)
                    try:
                        # Notify the client that he is helding the resource
                        remote_ref_callback = Proxy(
                            "PYRONAME:client{0}.callback"
                            .format(subscribers2[0]))
                    except:
                        print('Acquire Lock error.')
                    else:
                        # It sets a timeout for resource usage
                        with lock_leasing_time2:
                            leasing_time2 = time_ns() + DEFALUT_LEASING_TIME
                        message = '{0} {1}'.format(
                            str(type(self))[17:-2], res).encode()

                        remote_ref_callback.notify(
                            message.decode()
                        )

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

                            res = "RELEASED {0}".format(subscribers)

                            try:
                                # Notify the client that he released the resource
                                remote_ref_callback = Proxy(
                                    "PYRONAME:client{0}.callback"
                                    .format(released_id))
                            except:
                                print('Release Lock error.')
                            else:
                                message = '{0} {1}'.format(
                                    str(type(self))[17:-2], res).encode()

                                remote_ref_callback.notify(
                                    message.decode()
                                )

                            # Maybe insert a block here to wait until the client
                            # informs that stoped the usage

                            if len(subscribers) > 0:
                                res = "HELD {0}".format(subscribers)
                                try:
                                    # Notify the client that he is helding the resource
                                    remote_ref_callback = Proxy(
                                        "PYRONAME:client{0}.callback"
                                        .format(subscribers[0]))
                                except:
                                    print('Acquire Lock error.')
                                else:
                                    # It sets a timeout for resource usage
                                    with lock_leasing_time:
                                        leasing_time = time_ns() + DEFALUT_LEASING_TIME

                                    message = '{0} {1}'.format(
                                        str(type(self))[17:-2], res).encode()

                                    remote_ref_callback.notify(
                                        message.decode()
                                    )

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

                            res = "RELEASED {0}".format(subscribers2)

                            try:
                                # Notify the client that he released the resource
                                remote_ref_callback = Proxy(
                                    "PYRONAME:client{0}.callback"
                                    .format(released_id))
                            except:
                                print('Release Lock error.')
                            else:
                                message = '{0} {1}'.format(
                                    str(type(self))[17:-2], res).encode()

                                remote_ref_callback.notify(
                                    message.decode()
                                )

                            # Maybe insert a block here to wait until the client
                            # informs that stoped the usage

                            if len(subscribers2) > 0:
                                res = "HELD {0}".format(subscribers2)
                                try:
                                    # Notify the client that he is helding the resource
                                    remote_ref_callback = Proxy(
                                        "PYRONAME:client{0}.callback"
                                        .format(subscribers2[0]))
                                except:
                                    print('Acquire Lock error.')
                                else:
                                    # It sets a timeout for resource usage
                                    with lock_leasing_time2:
                                        leasing_time2 = time_ns() + DEFALUT_LEASING_TIME

                                    message = '{0} {1}'.format(
                                        str(type(self))[17:-2], res).encode()

                                    remote_ref_callback.notify(
                                        message.decode()
                                    )


def print_status():
    print('Queue1: {0}   Queue2: {1}                              '
          .format(subscribers, subscribers2), end='\r')

if __name__ == '__main__':
    task_scheduler = PyScheduler()
    task_scheduler.start()

    RepeatTimer(1, print_status).start()