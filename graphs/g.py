#!/usr/bin/env python


import numpy as np
import matplotlib.pyplot as plt

data ={
    250: 	7,
    420:        13,
    700: 	21,
    1170:	31,
    1940:	46,
    3250:	70,
    5425:	98,
    9060:	140,
    15125:	203,
    25250:	280,
    42185:	392,
    70440:	525,
    117635:	693,
    196450:	889,
    328075:	1120,
    547875:	1400,
    914970:	1820,
    1527990:	2240,
    2551740:	2800,
    4261405:	3430,
    7116550:	4270,
}

def plotg():
    x = [i for i in data.keys()]
    y = [i for i in data.values()]
    plt.plot(x, y)
    plt.title('Glina')
    plt.grid(True)
    plt.show()
    


def main():
    plotg()

if __name__ == '__main__':
    main()
