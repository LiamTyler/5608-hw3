import random
from math import *

class Vec3:
    def __init__( self, x = 0, y = 0, z = 0 ):
        self.x = x
        self.y = y
        self.z = z

    def __add__( self, v ):
        return Vec3( self.x + v.x, self.y + v.y, self.z + v.z )

    def __sub__( self, v ):
        return Vec3( self.x + v.x, self.y + v.y, self.z + v.z )

    def __mul__( self, scalar ):
        return Vec3( self.x * scalar, self.y * scalar, self.z * scalar )

    def __truediv__( self, scalar ):
        return Vec3( self.x / scalar, self.y / scalar, self.z / scalar )

    def dot( self, v ):
        return self.x * v.x + self.y * v.y + self.z * v.z

    def cross( self, v ):
        x = self.y * v.z - self.z * v.y
        y = -self.x * v.z + self.z * v.x
        z = self.x * v.y - self.y * v.x

        return Vec3( x, y, z )

    def normalize( self ):
        l = sqrt( self.x*self.x + self.y*self.y + self.z*self.z )
        return self / l

    def __str__( self ):
        return str( self.x ) + " " + str( self.y ) + " " + str( self.z )
    
    def __repr__( self ):
        return self.__str__()

def RandomViewDir():
    u1 = random.random()
    u2 = random.random()
    theta  = 2 * pi * u1
    radius = sqrt( 1 - u2 * u2 )
    x = radius * cos( theta )
    y = radius * sin( theta )
    z = u2

    return Vec3( x, y, z )

def PhongLobe( exponent ):
    u1 = random.random()
    u2 = random.random()
    phi = 2 * pi * u1
    theta = acos( pow( u2, 1/(exponent+1) ) )
    #print( "theta:", degrees(theta), ", phi:", degrees(phi) )
    x = sin( theta ) * cos( phi )
    y = sin( theta ) * sin( phi )
    z = cos( theta )

    return Vec3( x, y, z ).normalize()

def TBN( T, B, N, v ):
    return T * v.x + B * v.y + N * v.z

# copy old/base obj into output obj file
ofile = open( "part2.obj", 'w' )
ifile = open( "base.obj", 'r' )

for line in ifile:
    ofile.write( line )
ifile.close()

numSamples = 25
phongExponent = 75
R = Vec3( 1, 0, 1 ).normalize() # reflection vector

# TBN vectors / matrix to convert sampled vectors from local to world space
T = Vec3( 1, 0, 0 )
B = T.cross( R ).normalize()
N = R.normalize()


numVertices = 9
for i in range( numSamples ):
    # sample view direction in local space
    V = PhongLobe( phongExponent )
    # convert to world space
    V = TBN( T, B, N, V ).normalize()
    # shorten the vector based on specular strength
    specularMagnitude = pow( max( 0, V.dot( R ) ), phongExponent )
    V *= specularMagnitude

    ofile.write( "v " + V.__str__() )
    ofile.write( '\n' )
    ofile.write( "l 1 " + str( numVertices ) )
    ofile.write( '\n' )
    numVertices += 1

ofile.close()
