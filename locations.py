#!/usr/bin/env python

W_COOR = (45, 831)

RES_GO = (247, 161)
VIL_GO = (300, 161)
MAP_GO = (392, 161)

MINE_UPGRADE = (380, 532)

#рудники -> f - лес, c - зерно, g - глина, i - железо
F1 = (321, 364)
F2 = (479, 377)
F3 = (419, 543)
F4 = (405, 601)

G1 = (376, 415)
G2 = (432, 423)
G3 = (312, 596)
G4 = (495, 576)


I1 = (262, 405)
I2 = (517, 420)
I3 = (473, 454)
I4 = (560, 454)


C1 = (410, 365)
C2 = (203, 454)
C3 = (283, 456)
C4 = (210, 516)
C5 = (540, 511)

F_MINES = [F1, F2, F3, F4]
F_MINES_DICT = {'F%d' %(n+1): F_MINES[n] for n in range(len(F_MINES))}
G_MINES = [G1, G2, G3, G4]
G_MINES_DICT = {'G%d' %(n+1): G_MINES[n] for n in range(len(G_MINES))}
I_MINES = [I1, I2, I3, I4]
G_MINES_DICT = {'I%d' %(n+1): I_MINES[n] for n in range(len(I_MINES))}
C_MINES = [C1, C2, C3, C4, C5]
G_MINES_DICT = {'C%d' %(n+1): C_MINES[n] for n in range(len(C_MINES))}
MINES = []
MINES.extend(F_MINES)
MINES.extend(G_MINES)
MINES.extend(I_MINES)
MINES.extend(C_MINES)
MINES_DICT = {}
MINES_DICT.update(F_MINES)
MINES_DICT.update(G_MINES)
MINES_DICT.update(I_MINES)
MINES_DICT.update(C_MINES)


MAP_X = (628, 695)
MAP_Y = (685, 695)
MAP_OK = (753, 695)
MAP_CENTER = (517, 500)
BROWSER_EDIT = (76, 10)
BROWSER_EDIT_GET_ALL = (107, 167)
