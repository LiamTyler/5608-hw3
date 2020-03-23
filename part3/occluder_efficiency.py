import re
import matplotlib.pyplot as plt
import numpy as np
from pyquaternion import *
from math import *
import os
import subprocess

scene1 = """

#
# Camera configuration: the camera is located on the Z axis, and is
# pointed at the center of the scene
#
#LookAt 20 20 20  0 0 0   0 1 0

LookAt 4 4 10   0 2 0  0 1 0
Camera "perspective" "float fov" [30]

Integrator "directlighting" "integer maxdepth" [5]

WorldBegin


#
# Light
#


AttributeBegin
"""


scene2 = """
   Translate 0 4.5 0
   Rotate 45 0 1 0
Shape "trianglemesh" "integer indices" [ 0 1 2 2 3 0 ]
    "point P" [-.6 0 -.6   .6 0 -.6   .6 0 .6   -.6 0 .6 ]
AttributeEnd

#
# Occluder
#


AttributeBegin
Material "matte" "color Kd" [.5 .5 .5]
Translate 0 2 0
Shape "trianglemesh" "point P" [ -1 0 -1   1 0 -1   1 0 1   -1 0 1 ]
      "float uv" [ 0 0 1 0 1 1 0 1 ]
	"integer indices" [ 0 1 2 2 3 0]
AttributeEnd


#
# Ground Plane
#


AttributeBegin
Material "matte" "color Kd" [.5 .5 .5]

Shape "trianglemesh" "point P" [ -100 0 -100   100 0 -100   100 0 100   -100 0 100 ]
      "float uv" [ 0 0 1 0 1 1 0 1 ]
	"integer indices" [ 0 1 2 2 3 0]
AttributeEnd


WorldEnd
"""

os.chdir('C:\\Users\\Liam Tyler\\Documents\\School\\5608\\HW1\\pbrt-v3\\build\\results')

powersOf2 = [ 1, 2, 4, 8, 16, 32, 64 ]

for numEyeSamples in powersOf2:
    print( "Eye:", numEyeSamples )
    for numLightSamples in powersOf2:
        print( "Light:", numLightSamples )
        baseName  = "occluder/occluder_eye_" + str(numEyeSamples) + "_light_" + str(numLightSamples)
        imageName = baseName + ".exr"

        scene = ""
        scene += "Film \"image\" \"string filename\" [\"" + imageName + "\"]  \"integer xresolution\" [300] \"integer yresolution\" [300]\n"
        scene += "Sampler \"random\" \"integer pixelsamples\" [" + str( numEyeSamples ) + "]\n"
        scene += scene1
        scene += "AreaLightSource \"area\" \"color L\" [10 10 10] \"integer nsamples\" [" + str( numLightSamples ) + "]\n"
        scene += scene2
        #print(scene)

        f = open( 'scene.pbrt', 'w')
        f.write( scene )
        f.close()
        cmd = "..\\Release\\pbrt.exe scene.pbrt > " + baseName + "_log.txt"
        os.system(cmd)
        cmd = "..\\Release\\exrdiff.exe ..\\..\\..\\..\\HW3\\part3\\scenes\\occluder_ref.exr " + imageName + " >> " + baseName + "_log.txt"
        os.system(cmd)
