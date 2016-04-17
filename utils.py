#!/usr/bin/env python

from mines import get_mine_data
from db import session
from db import Mine
from locations import MINES


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

from maps import get_cell_params
from db import Cell

def update_cells_to_db(radius=10):
    COORD = (-40, 83)
    for x in range(COORD[0]-10, COORD[0]+10):
        for y in range(COORD[1]-10, COORD[1]+10):
            data = get_cell_params(x, y)
            data['x'] = x
            data['y'] = y
            Cell.create_or_update(**data)


if __name__ == '__main__':
    update_cells_to_db()
