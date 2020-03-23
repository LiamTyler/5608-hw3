import re
import matplotlib.pyplot as plt

MSE = []
renderTimes = []

SCENE = "occluder"

powersOf2 = [ 1, 2, 4, 8, 16, 32, 64 ]

baseDir = "C:\\Users\\Liam Tyler\\Documents\\School\\5608\HW1\\pbrt-v3\\build\\results\\" + SCENE + "\\"

for numEyeSamples in powersOf2:
    for numLightSamples in powersOf2:
        filename  = baseDir + SCENE + "_eye_" + str(numEyeSamples) + "_light_" + str(numLightSamples) + "_log.txt"
        f = open(filename)
        txt = f.read()
        mse = re.findall(r'MSE\ =\ (\d+.*),', txt )[0]
        renderTime = re.findall(r'PBRT_TOTAL_RENDER_TIME\ =\ (\d+.*)s', txt )[0]
        MSE.append(float(mse))
        renderTimes.append(float(renderTime))


for i in range( 7 ):
    lines = plt.plot( powersOf2, renderTimes[i*7:i*7+7], label=str(powersOf2[i]) + " spp" )

plt.title( SCENE + " Render Times" )
plt.ylabel('Time (s)')
plt.xlabel('Samples Per Light')
plt.xticks( powersOf2 )
plt.legend()
plt.show()

for i in range( 7 ):
    lines = plt.plot( powersOf2, MSE[i*7:i*7+7], label=str(powersOf2[i]) + " spp" )
    
plt.title( SCENE + " MSE" )
plt.ylabel('MSE')
plt.xlabel('Samples Per Light')
plt.xticks( powersOf2 )
plt.yscale( 'log' )
plt.legend()
plt.show()


for i in range( 7 ):
    lines = plt.scatter( renderTimes[i*7:i*7+7], MSE[i*7:i*7+7], label=str(powersOf2[i]) + " spp" )
    
plt.title( SCENE + " Render time vs variance" )
plt.ylabel('MSE')
plt.xlabel('Render Time (s)')
plt.xticks( powersOf2 )
plt.xscale( 'log' )
#plt.axis( [0, 43, 0, 0.00002] )
#plt.yscale( 'log' )
plt.legend()
plt.show()


