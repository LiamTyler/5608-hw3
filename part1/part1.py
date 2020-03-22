from math import *
import numpy as np
import matplotlib.pyplot as plt
import random

def inv_cdf1( x ):
    return 6 - 2*sqrt( 9 - 8*x )

def inv_cdf2( x ):
    return 4*x

def inv_cdf3( x ):
    return -2 + 2*sqrt( 8*x + 1 )

def inv_cdf4( x ):
    return 4*sqrt( x )

def pdf1( x ):
    return (6-x)/16

def pdf2( x ):
    return 1/4

def pdf3( x ):
    return (x+2)/16

def pdf4( x ):
    return x/8

# these sample the variance
def sample1():
    x = inv_cdf1( random.random() )
    return pow( x / pdf1( x ) - 8, 2 )

def sample2():
    x = inv_cdf2( random.random() )
    return pow( x / pdf2( x ) - 8, 2 )

def sample3():
    x = inv_cdf3( random.random() )
    return pow( x / pdf3( x ) - 8, 2 )

def sample4():
    x = inv_cdf4( random.random() )
    return pow( x / pdf4( x ) - 8, 2 )


# plot integrand f(x) = x
Xs = [ x / 50 for x in range( 201 ) ]
plt.plot( Xs, Xs, label='F(x)' )
# plot each pdf
plt.plot( Xs, [ pdf1(x) for x in Xs ], c='r', label='PDF 1' )
plt.plot( Xs, [ pdf2(x) for x in Xs ], c='g', label='PDF 2' )
plt.plot( Xs, [ pdf3(x) for x in Xs ], c='c', label='PDF 3' )
plt.plot( Xs, [ pdf4(x) for x in Xs ], c='y', label='PDF 4' )
plt.xlabel( "X" )
plt.ylabel( "Y" )
plt.xlim( 0, 4 )
plt.ylim( 0, 1 )
plt.legend()
plt.title( "Integrand and PDFs" )
plt.show()


def CalculateRequiredSamples( sampleFunc ):
    numSamples = 0
    runningTotalVariance = 0
    error = 1
    while error > 0.008:
        runningTotalVariance += sampleFunc()
        numSamples += 1
        variance = runningTotalVariance / numSamples
        error = sqrt( variance / numSamples )

    return numSamples

print( "sampling function 1: required samples =", CalculateRequiredSamples( sample1 ) )
print( "sampling function 2: required samples =", CalculateRequiredSamples( sample2 ) )
print( "sampling function 3: required samples =", CalculateRequiredSamples( sample3 ) )
print( "sampling function 4: required samples =", CalculateRequiredSamples( sample4 ) )
