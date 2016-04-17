#!/usr/bin/env python
import readline
readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode vi')
from datetime import datetime
import threading

def interrupt():
    raise KeyboardInterrupt

def input_with_timeout(prompt, timeout=30.0):
    timer = threading.Timer(timeout, interrupt)
    astring = None
    try:
        timer.start()
        astring = input(prompt)
    except KeyboardInterrupt:
        pass
    timer.cancel()
    return astring

def loop():
    from queue import queue
    messages = []
    if queue.is_empty():
        messages.append('Очередь заданий пуста.')
    while True:
        n = 1
        for message in messages:
            print('%s)\t%s' % (n, message))
            n += 1
        messages = []
        line = input_with_timeout('>>: ')
        if line == 'exit':
            queue.save_to_db()
            break

        print('ENTERED: "%s"' % line)

if __name__ == '__main__':
    loop()
