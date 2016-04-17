#!/usr/bin/env python

from locations import W_COOR
from locations import MINES
from locations import RES_GO
from locations import MINE_UPGRADE
from control import Action, Move, SelectAll, GetCl, Copy, Click
from db import Mine, session
import re
import logging
from queue import queue


def mine_data_parse(x, y, data):
    '''
    Шахта не должна строиться!!
    '''
    strings = data.split('\n')
    n = 0
    for s in strings:
        if s.startswith('Расходы на строительство до уровня'):
            break
        n+=1

    kind = strings[n-5].strip()

    reg = re.compile('Производство:\s*(\d*) в час', re.UNICODE)
    match = reg.match(strings[n-2])
    if not match:
        raise RuntimeError('Wrong data')
    output = int(match.groups()[0])

    reg = re.compile('Производство на уровне (\d*):\s*(\d*) в час', re.UNICODE)
    match = reg.match(strings[n-1])
    if not match:
        raise RuntimeError('Wrong data')
    level, n_output = (int(i) for i in match.groups())
    level = level - 1


    reg = re.compile('Древесина(\d*)Глина(\d*)Железо(\d*)Зерно(\d*)Потребление зерна(\d*)', re.UNICODE)
    match = reg.match(strings[n+1])
    if not match:
        raise RuntimeError('Wrong data')
    r_f, r_g, r_i, r_c, r_g_c = (int(i) for i in match.groups())

    return (x, y, kind, level, output, n_output, r_g, r_f, r_i, r_c, r_g_c)



def get_mine_data(*c):
    x, y = c
    action = Action([Click(*RES_GO), Click(*c), Move(*W_COOR), SelectAll(), Copy(), GetCl()])
    data = action.eval()
    return mine_data_parse(x, y, data)

def create_mines_to_db():
    for m in MINES:
        d = get_mine_data(*m)
        new_mine = Mine(*d)
        session.add(new_mine)
    session.commit()

def update_mines_to_db():
    for m in MINES:
        (x, y, kind, level,
         output, n_output,
         r_g, r_f, r_i, r_c, r_g_c) = get_mine_data(*m)
        db_mine = session.query(Mine).filter_by(x=x, y=y).first()
        if not db_mine:
            raise RuntimeError('Шахта %s, %s не обнаружена' % (x, y))
        db_mine.x = x
        db_mine.y = y
        db_mine.kind = kind
        db_mine.level = level
        db_mine.output = output
        db_mine.n_output = n_output
        db_mine.r_g = r_g
        db_mine.r_f = r_f
        db_mine.r_i = r_i
        db_mine.r_c = r_c
        db_mine.r_g_c = r_g_c
        db_mine.constructed = False
    session.commit()


def upgrade_mine(mine):
    #  TODO: check availables upgrade
    x = mine.x
    y = mine.y
    action = Action([Click(*RES_GO), Click(x, y), Move(*W_COOR), SelectAll(), Copy(), GetCl()])
    data = action.eval()
    (x, y, kind, level, output, n_output, r_g, r_f, r_i, r_c, r_g_c) = mine_data_parse(x, y, data)
    mine.constructed = True
    session.add(mine)
    session.commit()
    # TODO Положить в очередь задание по обновлению данных для mine 
    action = Action([Click(*MINE_UPGRADE)])
    action.eval()

def upgrade_mine_by_job(job):
    '''
    params = 'kind=Лесопилка,level=4'
    '''
    #TODO: требует доробокти
    param_string = job[2]
    reg = re.compile('kind=(\w*),level=(\d*)', re.UNICODE)
    match = reg.match(param_string)
    if not match:
        queue.remove(job)
        logging.warning('Неправильные параметры для апгрейда шахты')
        return
    kind, level = match.groups()
    level = int(level)
    mine = session.query(Mine).filter_by(
        kind = kind,
        level = level,
        constructed = False
    ).first()
    if not mine:
        queue.remove(job)
        logging.warning('Не найдена шахта для апгрейда')
        return
    queue.remove(job)
    upgrade_mine(mine)

        

        




    

def main():
    mine = session.query(Mine).filter_by(
        kind = 'Лесопилка',
        level = 4
    ).first()
    upgrade_mine(mine)
   


if __name__ == '__main__':
    main()
