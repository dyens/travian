#!/usr/bin/env python

from sortedcontainers import SortedListWithKey
from datetime import datetime
from db import session, Job


class Queue(object):
    '''
    [('upgrade_mine', datetime(2014,3,3,4,5,59), [List Of Params] ), ...]
    '''

    types = [
        'upgrade_mine',
        'atack',
    ]

    queue = SortedListWithKey(key=lambda x: x[1])


    def __init__(self):
        for job in session.query(Job).all():
            work_type = job.work_type
            dt = job.datetime
            params = job.params
            self.add(work_type, dt, params)

    def save_to_db(self):
        Job.clear()
        for i in self.queue:
            job = Job(i[0], i[1], i[2])
            session.add(job)
        session.commit()

    def add(self, work_type, dt, params):
        self.queue.add((work_type, dt, params))

    def update(self, work_type, dt, params):
        self.queue.update(work_type, dt, params)

    def get(self):
        return self.queue[0]

    def get_all(self):
        return self.queue

    def remove(self, arg):
        self.queue.remove(arg)

    def is_empty(self):
        if len(self.queue) == 0:
            return True
        else:
            return False
                       
                   

    

queue = Queue()

def main():
    a = datetime(2014, 1,1)
    b = datetime(2014, 2, 2)
    test = ('upgrade_mine', a, ['gopa'])
    queue.add(*test)
    queue.add('upgrade_mine', b, ['pizda'])
    print(queue.is_empty())
    print(queue.get_all())
    queue.remove(test)
    print(queue.get_all())
    print(queue.get())

if __name__ == '__main__':
    main()
