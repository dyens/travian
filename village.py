#!/usr/bin/env python


import re
from datetime import timedelta
from locations import W_COOR
from control import Action, Move, SelectAll, Copy, GetCl

def parse_cl(cl):
    data = {
        'gold': None,
        'silver': None,
        'stock': None,
        'f': None,
        'g': None,
        'c': None,
        'i': None,
        'ambar': None,
        'population': None,
        'build': [],
        'f_v': None,
        'g_v': None,
        'c_v': None,
        'i_v': None,
    }

    strings = cl.split('\n')
    n = 0
    n_res = None
    n_b = None
    n_o = None
    n_prod = None
    n_f = None
    n_e = None
    for s in strings:
        if s.startswith('Золото'):
            reg = re.compile('Золото (\d*)', re.UNICODE)
            match = reg.match(s.strip())
            data['gold'] = int(match.groups()[0])

        if s.startswith('Серебро'):
            reg = re.compile('Серебро (\d*)', re.UNICODE)
            match = reg.match(s.strip())
            data['silver'] = int(match.groups()[0])

        if s.strip().startswith('Склад'):
            n_res = n

        if s.strip().startswith('Строительство'):
            n_b = n

        if s.strip().startswith('Исходящие войска:'):
            n_o = n

        if s.strip().startswith('Производство в час:'):
            n_prod = n

        if s.strip().startswith('Войска:'):
            n_f = n

        if s.strip().startswith('dyens'):
            n_e = n - 1
            break

        n += 1

    if n_res is not None:
        reg = re.compile('Склад\s*(\d*)\.(\d*)', re.UNICODE)
        match = reg.match(strings[n_res].strip())
        data['stock'] = int('%s%s' % match.groups())

        reg = re.compile('Древесина\s*(\d*)', re.UNICODE)
        match = reg.match(strings[n_res+1].strip())
        data['f'] = int(match.groups()[0])

        reg = re.compile('Глина\s*(\d*)', re.UNICODE)
        match = reg.match(strings[n_res+2].strip())
        data['g'] = int(match.groups()[0])

        reg = re.compile('Железо\s*(\d*)', re.UNICODE)
        match = reg.match(strings[n_res+3].strip())
        data['i'] = int(match.groups()[0])

        reg = re.compile('Амбар\s*(\d*)\.(\d*)', re.UNICODE)
        match = reg.match(strings[n_res+4].strip())
        data['ambar'] = int('%s%s' % match.groups())
        
        reg = re.compile('Зерно\s*(\d*)', re.UNICODE)
        match = reg.match(strings[n_res+5].strip())
        data['c'] = int(match.groups()[0])

        reg = re.compile('Потребление зерна\s*(\d*)', re.UNICODE)
        match = reg.match(strings[n_res+6].strip())
        data['population'] = int(match.groups()[0])


    if n_b is not None:
        n_b_e = min([i for i in (n_o, n_prod, n_f, n_e) if i is not None])
        #TODO: Что будет в случае двойного строительства
        for i in range(n_b+2, n_b_e-3, 3): #mb 4????
            name = strings[i+1].strip()
            reg = re.compile('(\d*):(\d*):(\d*)\s*', re.UNICODE)
            h, m, s = reg.match(strings[i+2].strip()).groups()
            delta = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            data['build'].append((name, delta))

    if n_o is not None:
        n_o_e = min([i for i in (n_prod, n_f, n_e) if i is not None])
        #TODO: Сделать это. Но нужно чтоб было послано несколько войск


    if n_prod is not None:
        def get_val(s):
            n = [i for i in s if i.isdigit()]
            return int(''.join(n))

        data['f_v'] = get_val(strings[n_prod+2])
        data['g_v'] = get_val(strings[n_prod+4])
        data['i_v'] = get_val(strings[n_prod+6])
        data['c_v'] = get_val(strings[n_prod+8])

    return data


def get_village_params():
    action = Action([Move(*W_COOR), SelectAll(), Copy(), GetCl()])
    data = action.eval()
    return parse_cl(data)






if __name__ == '__main__':
    print(get_village_params())


#    with open('data.txt', 'r') as f:
#        data = parse_cl(f.read())
#        print(data)
