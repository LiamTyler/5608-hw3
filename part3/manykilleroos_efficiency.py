import re
import matplotlib.pyplot as plt
import numpy as np
from pyquaternion import *
from math import *
import os
import subprocess

#Film "image" "string filename" ["manykilleroos.exr"]  "integer xresolution" [400] "integer yresolution" [400]
#Sampler "lowdiscrepancy" "integer pixelsamples" [64]

scene1 = """Accelerator "kdtree"


#
# CS348B Note: Use the following LookAt declarations to render the
# three versions of the scene for assignment 2
#

Integrator "directlighting" "integer maxdepth" [5]

# Configuration 1: The entire scene from above
#LookAt 10 120 -25  0 0 0   -.081 .976 .203


# Configuration 2: Medium Range 
 LookAt 19 19 -48   10.5 5 -23   0 1 0


# Configuration 3: Close Up -- Near a killeroo head
# LookAt 12 7 -34.5   6 8.5 -24   0 1 0



Camera "perspective" "float fov" [38]


WorldBegin

#
# The scene is lit by a single area light
#

AttributeBegin
"""
#AreaLightSource "area" "color L" [200 200 200] "integer nsamples" [1]

scene2 = """Translate 30 40 -60
Shape "disk" "float radius" [6] 
AttributeEnd


#
# The ground plane
#

AttributeBegin

Texture "grid" "color" "imagemap" "string filename" ["lines.exr"] "float uscale" [8] "float vscale" [8]
Texture "scaled_grid" "color" "scale" "texture tex1" "grid" "color tex2" [ .5 .5 .8 ]
Material "matte" "texture Kd" "scaled_grid"

Scale 100 100 100
Rotate 90 1 0 0
Shape "trianglemesh"     
    "point P" [-1 -1 0  1 -1 0   1 1 0   -1 1 0 ]
    "float uv" [0 0   1 0   1 1   0 1]
    "integer indices" [ 0 2 1 0 3 2 ]

AttributeEnd


#
# Rows of killeroos
#

TransformBegin

Translate -50 0 -25

AttributeBegin
Material "plastic" "color Kd" [.2 .4 1.0] "color Ks" [1 1 1] "float roughness" [.1]
Include "killeroo_row.pbrt"
AttributeEnd

Translate 5 0 10

AttributeBegin
Material "plastic" "color Kd" [.9 .2 .1] "color Ks" [1 1 1] "float roughness" [.1]
Include "killeroo_row.pbrt"
AttributeEnd

Translate -5 0 10

AttributeBegin
Material "plastic" "color Kd" [.4 .4 .8] "color Ks" [1 1 1] "float roughness" [.1]
Include "killeroo_row.pbrt"
AttributeEnd

Translate 5 0 10

AttributeBegin
Material "plastic" "color Kd" [.4 .9 .4] "color Ks" [1 1 1] "float roughness" [.1]
Include "killeroo_row.pbrt"
AttributeEnd

Translate -5 0 10

AttributeBegin
Material "plastic" "color Kd" [.6 .7 .4] "color Ks" [1 1 1] "float roughness" [.1]
Include "killeroo_row.pbrt"
AttributeEnd

Translate 5 0 10

AttributeBegin
Material "plastic" "color Kd" [.9 .5 .3] "color Ks" [1 1 1] "float roughness" [.1]
Include "killeroo_row.pbrt"
AttributeEnd

Translate -5 0 10

AttributeBegin
Material "plastic" "color Kd" [.9 .4 .6] "color Ks" [1 1 1] "float roughness" [.1]
Include "killeroo_row.pbrt"
AttributeEnd

TransformEnd


#
# Kiddie killeroos
#


AttributeBegin
Material "plastic" "color Kd" [.9 .6 .5] "color Ks" [1 1 1] "float roughness" [.1]
Translate 64 0 2
Translate -50 0 -25

TransformBegin
Translate 0 2.9 -3
Scale 0.02 0.02 0.02
Rotate 30 0 1 0
Rotate -90 1 0 0
Include "killeroo_subdiv1.pbrt"
TransformEnd

TransformBegin
Translate -10 2.9 -2
Scale 0.02 0.02 0.02
Rotate -10 0 1 0
Rotate -90 1 0 0
Include "killeroo_subdiv1.pbrt"
TransformEnd

TransformBegin
Translate -9 3.5 -7
Scale 0.025 0.025 0.025
Rotate -50 0 1 0
Rotate -90 1 0 0
Include "killeroo_subdiv1.pbrt"
TransformEnd

TransformBegin
Translate 2 2 -2
Scale 0.015 0.015 0.015
Rotate -45 0 1 0
Rotate -90 1 0 0
Include "killeroo_subdiv1.pbrt"
TransformEnd

TransformBegin
Translate -13 2 5
Scale 0.015 0.015 0.015
Rotate 60 0 1 0
Rotate -90 1 0 0
Include "killeroo_subdiv1.pbrt"
TransformEnd

TransformBegin
Translate -1.5 5.5 3
Scale 0.04 0.04 0.04
Rotate -35 0 1 0
Rotate -90 1 0 0
Include "killeroo_subdiv1.pbrt"
TransformEnd

AttributeEnd



WorldEnd

"""

os.chdir('C:\\Users\\Liam Tyler\\Documents\\School\\5608\\HW1\\pbrt-v3\\build\\results')

powersOf2 = [ 1, 2, 4, 8, 16, 32, 64 ]

for numEyeSamples in powersOf2:
    print( "Eye:", numEyeSamples )
    for numLightSamples in powersOf2:
        print( "Light:", numLightSamples )
        baseName  = "killeroos/manykilleroos_eye_" + str(numEyeSamples) + "_light_" + str(numLightSamples)
        imageName = baseName + ".exr"

        scene = ""
        scene += "Film \"image\" \"string filename\" [\"" + imageName + "\"]  \"integer xresolution\" [400] \"integer yresolution\" [400]\n"
        scene += "Sampler \"lowdiscrepancy\" \"integer pixelsamples\" [" + str( numEyeSamples ) + "]\n"
        scene += scene1
        scene += "AreaLightSource \"area\" \"color L\" [200 200 200] \"integer nsamples\" [" + str( numLightSamples ) + "]\n"
        scene += scene2
        #print(scene)

        f = open( 'scene.pbrt', 'w')
        f.write( scene )
        f.close()
        cmd = "..\\Release\\pbrt.exe scene.pbrt > " + baseName + "_log.txt"
        os.system(cmd)
        cmd = "..\\Release\\exrdiff.exe ..\\..\\..\\..\\HW3\\part3\\scenes\\manykilleroos_ref.exr " + imageName + " >> " + baseName + "_log.txt"
        os.system(cmd)
