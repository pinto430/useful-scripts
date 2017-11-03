#!/bin/env python 
import salt.config
import salt.utils.event
import sys
import time
import tornado

opts = salt.config.client_config('/etc/salt/master')

event = salt.utils.event.get_event(
        'master',
        sock_dir=opts['sock_dir'],
        transport=opts['transport'],
        opts=opts)

while True:
    try:
        while True:
            data = event.get_event_block()
            print(data)
    except tornado.iostream.StreamClosedError as ex:
        print(ex)
        event.close_pub()
        tries = 0
        while not event.cpub:
            if tries > 0:
                time.sleep(1)
            tries += 1
            print('Reconnecting #{0}'.format(tries))
            event.connect_pub()
    except:
        print('Some exception: {0}'.format(sys.exc_info()[0]))
        break
