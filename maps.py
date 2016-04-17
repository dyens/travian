#!/usr/bin/env python

import re
from locations import MAP_GO
from locations import MAP_X
from locations import MAP_Y
from locations import MAP_OK
from locations import MAP_CENTER
from locations import BROWSER_EDIT
from locations import BROWSER_EDIT_GET_ALL

from control import Click
from control import DoubleClick
from control import Type
from control import Copy
from control import GetCl
from control import Action

import logging



def parse_buf(s):
#    type_name = wild, village, free_oasis, natars
    data = {
        'type_name': None,
        'f': None,
        'g': None,
        'i': None,
        'c': None,
        'culture': None,
        'allaince': None,
        'player_name': None,
        'population': None
    }
    if 'Дикая местность' in s:
        data['type_name'] = 'wild'
        return data

    elif 'Деревня' in s:
        data['type_name'] = 'village'
        n = 0
        strings = s.split('\n')
        for i in strings:
            if i.startswith('Деревня'):
                break
            n += 1
        string = strings[n+7]
        reg = re.compile('Древесина\s*(\d*)\s*Глина\s*(\d*)\s*Железо\s*(\d*)\s*Зерно\s*(\d*)', re.UNICODE)
        match = reg.match(string)
        if not match:
            raise RuntimeError('Wrong data')
        f, g, i, c = (int(i) for i in match.groups())
        data['f'] = f
        data['g'] = g
        data['i'] = i
        data['c'] = c

        string = strings[n+9]
        reg = re.compile('Народ:\s*(\w*)', re.UNICODE)
        match = reg.match(string)
        if not match:
            raise RuntimeError('Wrong data')
        data['culture'] = match.groups()[0]

        string = strings[n+10]
        reg = re.compile('Альянс:\s*(\w*)', re.UNICODE)
        match = reg.match(string)
        if not match:
            raise RuntimeError('Wrong data')
        data['allaince'] = match.groups()[0]

        string = strings[n+11]
        reg = re.compile('Игрок:\s*(\w*)', re.UNICODE)
        match = reg.match(string)
        if not match:
            raise RuntimeError('Wrong data')
        data['player_name'] = match.groups()[0]

        string = strings[n+12]
        reg = re.compile('Население:\s*(\d*)', re.UNICODE)
        match = reg.match(string)
        if not match:
            raise RuntimeError('Wrong data')
        data['population'] = match.groups()[0]
        return data

    elif 'Натары' in s:
        data['type_name'] = 'natars'
        n = 0
        strings = s.split('\n')
        for i in strings:
            if i.startswith('Натары'):
                break
            n += 1
        string = strings[n+7]
        reg = re.compile('Древесина\s*(\d*)\s*Глина\s*(\d*)\s*Железо\s*(\d*)\s*Зерно\s*(\d*)', re.UNICODE)
        match = reg.match(string)
        if not match:
            raise RuntimeError('Wrong data')
        f, g, i, c = (int(i) for i in match.groups())
        data['f'] = f
        data['g'] = g
        data['i'] = i
        data['c'] = c

        string = strings[n+9]
        reg = re.compile('Народ:\s*(\w*)', re.UNICODE)
        match = reg.match(string)
        if not match:
            raise RuntimeError('Wrong data')
        data['culture'] = match.groups()[0]

        string = strings[n+12]
        reg = re.compile('Население:\s*(\d*)', re.UNICODE)
        match = reg.match(string)
        if not match:
            raise RuntimeError('Wrong data')
        data['population'] = match.groups()[0]
        return data

    elif 'Натары' in s:
        data['type_name'] = 'natars'
        n = 0
        strings = s.split('\n')
        for i in strings:
            if i.startswith('Натары'):
                break
            n += 1
        string = strings[n+7]
        reg = re.compile('Древесина\s*(\d*)\s*Глина\s*(\d*)\s*Железо\s*(\d*)\s*Зерно\s*(\d*)', re.UNICODE)
        match = reg.match(string)
        if not match:
            raise RuntimeError('Wrong data')
        f, g, i, c = (int(i) for i in match.groups())
        data['f'] = f
        data['g'] = g
        data['i'] = i
        data['c'] = c

        string = strings[n+9]
        reg = re.compile('Народ:\s*(\w*)', re.UNICODE)
        match = reg.match(string)
        if not match:
            raise RuntimeError('Wrong data')
        data['culture'] = match.groups()[0]

        string = strings[n+12]
        reg = re.compile('Население:\s*(\d*)', re.UNICODE)
        match = reg.match(string)
        if not match:
            raise RuntimeError('Wrong data')
        data['population'] = match.groups()[0]
        return data

    elif 'Столица' in s:
        data['type_name'] = 'main'
        n = 0
        strings = s.split('\n')
        for i in strings:
            if 'Столица' in i:
                break
            n += 1
        
        string = strings[n+7]
        reg = re.compile('Древесина\s*(\d*)\s*Глина\s*(\d*)\s*Железо\s*(\d*)\s*Зерно\s*(\d*)', re.UNICODE)
        match = reg.match(string)
        if not match:
            raise RuntimeError('Wrong data')
        f, g, i, c = (int(i) for i in match.groups())
        data['f'] = f
        data['g'] = g
        data['i'] = i
        data['c'] = c

        string = strings[n+9]
        reg = re.compile('Народ:\s*(\w*)', re.UNICODE)
        match = reg.match(string)
        if not match:
            raise RuntimeError('Wrong data')
        data['culture'] = match.groups()[0]

        string = strings[n+10]
        reg = re.compile('Альянс:\s*(\w*)', re.UNICODE)
        match = reg.match(string)
        if not match:
            raise RuntimeError('Wrong data')
        data['allaince'] = match.groups()[0]

        string = strings[n+11]
        reg = re.compile('Игрок:\s*(\w*)', re.UNICODE)
        match = reg.match(string)
        if not match:
            raise RuntimeError('Wrong data')
        data['player_name'] = match.groups()[0]

        string = strings[n+12]
        reg = re.compile('Население:\s*(\d*)', re.UNICODE)
        match = reg.match(string)
        if not match:
            raise RuntimeError('Wrong data')
        data['population'] = match.groups()[0]
        return data


    elif 'Свободный оазис' in s:
        data['type_name'] = 'free_oasis'
        #TODO: определить войска и бонусы
        return data

    else:
        logging.warning('Неясная ячейка (скорей всего захваченный оазис)')

    return data

def get_cell_params(x, y):
    action = Action([
        Click(*MAP_GO),
        DoubleClick(*MAP_X),
        Type(str(x)),
        DoubleClick(*MAP_Y),
        Type(str(y)),
        Click(*MAP_OK),
        Click(*MAP_CENTER),
        Click(*BROWSER_EDIT),
        Click(*BROWSER_EDIT_GET_ALL),
        Copy(),
        GetCl()
    ])
    buf = action.eval()
    data = parse_buf(buf)
    return data



if __name__ == '__main__':

    MY_COORD = (-43, 78)
    b = get_cell_params(*MY_COORD)
    print(b)
