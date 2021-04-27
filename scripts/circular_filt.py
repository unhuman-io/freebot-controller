#!/usr/bin/env python
from numpy import *
from scipy.fftpack import *
from matplotlib.pyplot import *
import numpy as np

def circular_filt(x, y, nbins=1000, modx=2*pi, ffilt=100, magfilt=0):
    xm = mod(x,modx)
    xi = linspace(0,modx, nbins+1)
    ibins = digitize(xm, xi)
    bc = bincount(ibins)[1:]
    bs = bincount(ibins,weights=y)[1:]
    yavg = bs/bc

    # plot(yavg)
    # show()
    #yavgz = yavg - mean(yavg)

    f = fft(yavg)
    freq = fftfreq(nbins, 1.0/nbins)
    f_filt = f
    f_filt[fabs(freq)>ffilt] = 0
    f_filt[absolute(f_filt)<magfilt] = 0
    #print(f_filt)
    f_filt[0] = 0 # remove average
    yfilt = ifft(f_filt)

    # plot(yavg)
    # plot(yfilt)
    # show()
    return real(yfilt)

def fft_derivative(x, y):
    f = fft(y)
    fderiv = 2*pi*1j*fftfreq(len(x),mean(np.diff(x)))*f
    return real(ifft(fderiv))

def pchip_coeff(x,y,yd):
    n = len(y)
    a = zeros(n)
    b = zeros(n)
    c = zeros(n)
    d = zeros(n)
    for i in range(n):
        inext = i+1        
        if (inext >= n):
            inext = 0
        dx = x[inext] - x[i]
        dx = mod(dx,2*pi)

        a[i] = y[i]
        b[i] = dx*yd[i]
        c[i] = -3*y[i] -2*yd[i]*dx + 3*y[inext] - yd[inext]*dx
        d[i] = 2*y[i] + yd[i]*dx - 2*y[inext] + yd[inext]*dx
    return vstack((a, b, c, d)).T

# x range 0 to 2*pi, coefficents use 0..1 for t between points
def pchip_calc(pchip, x):
    a = pchip[:,0]
    b = pchip[:,1]
    c = pchip[:,2]
    d = pchip[:,3]

    n = len(a)
    table_x = x/2/pi*n
    i = table_x.astype(int)
    t = table_x - i
    i &= n - 1
    #y = a[i] + b[i]*dx + c[i]*dx*dx + d[i]*dx*dx*dx
    y = a[i] + t*(b[i] + t*(c[i] + d[i]*t))
    return y



        # float table_x = x*TABLE_LENGTH;
        # uint32_t i = table_x;
        # float remainder_x = table_x - i;
        # float dx = remainder_x*(1.0/TABLE_LENGTH);
        # i &= TABLE_LENGTH - 1;

        # float a = table_[i][0];
        # float b = table_[i][1];
        # float c = table_[i][2];
        # float d = table_[i][3];

        # float y = a + b*dx + c*dx*dx + d*dx*dx*dx;