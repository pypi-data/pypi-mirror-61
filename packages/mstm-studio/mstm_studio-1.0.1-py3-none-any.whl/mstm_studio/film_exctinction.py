# -*- coding: utf-8 -*-
#
#-----------------------------------------------------#
#                                                     #
# This code is a part of T-matrix fitting project     #
# Contributors:                                       #
#  A. Skidanenko <ann.skidanenko@yandex.ru>,          #
#  L.Avakyan <laavakyan@sfedu.ru>                     #
#                                                     #
#-----------------------------------------------------#

import numpy as np



def gold_film_ex(d, wls, smooth = True):
    """
        Obtain exctinction of gold films via
        linear interpolation of experimental data
        from paper [ ... ]

        Input parameters:
        d: fload
           depth of the gold film, nm
        wls: numpy.array of floats
           wavelengths for which the exctinction will be returned
        smooth: boolean
           if True the smoothing of the output will be performed
           using 5-point averaging formula

        Ouput: numpy.array of floats
           exctinction coefficients
    """
    f = open('gold_film_data.txt')

    ex  = []
    lam = []
    a1  = []
    b   = []

    index = -1
    if d < 0.5:
        print('Warning! Film depth %d is out of the data range!'%d)
    elif 0.5 <= d < 1.0:
        index = 0
        d1 = 0.5
        c = 0.5
    elif 1.0 <= d < 2.0:
        index = 1
        d1 = 1.0
        c = 1.0
    elif 2.0 <= d < 4.0:
        index = 2
        d1 = 2.0
        c = 2.0
    elif 4.0 <= d < 11.5:
        index = 3
        d1 = 4.0
        c = 7.5
    elif 11.5 <= d < 33.0:
        index = 4
        d1 = 11.5
        c = 21.5
    elif 33.0 <= d <= 74.0:
        index = 5
        d1 = 33.0
        c = 41.0
    else:
        print('Warning! Film depth %d is out of the data range!'%d)

    if index == -1:
        return np.zeros(len(wls))

    for line in f:
        l = line.split(' ')
        b.append( float( l[index]   ))
        a1.append(float( l[index+1] ))
        lam.append(float(l[7]))

    b  = np.array(b)
    a1 = np.array(a1)

    #a = np.array(a)
    lam = np.array(lam)
    #print(a)

    ex = (a1 - b) * (d1 - d) / c + b

    ex = np.interp( wls, lam, ex )

    if smooth:
        exx = np.zeros(len(ex))
        for j in range(2, len(ex) - 2):
            exx[j] =  (ex[j-2] + 4*ex[j-1] + 6*ex[j] + 4*ex[j+1] + ex[j+2])/16.0
        ex[2:len(ex)-2] = exx[2:len(ex)-2]

    return ex



if __name__ == '__main__':
    import matplotlib.pyplot as plt
    wls = np.linspace(400, 800, 51)
    d = 50.5
    ex = gold_film_ex( d, wls, False );
    exx = gold_film_ex( d, wls );

    plt.plot( wls, ex, wls, exx )
    #plt.plot( wls, ex )
    plt.xlabel('Wavelength, nm')
    plt.ylabel('Exctinction')
    plt.show()
