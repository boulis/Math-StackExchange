from math import sin, cos, pi, sqrt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Q: http://math.stackexchange.com/questions/2038229/how-tall-should-my-christmas-tree-be/

# Requires the matplotlib python package 

# height solution: http://www.wolframalpha.com/input/?i=29.7+%3D+0.5t*sqrt(1%2B(1%2F4)%5E2*(1%2B(2pi%2F0.3+*sqrt(17)%2F4)%5E2*t%5E2))%2B(1%2B(1%2F4)%5E2)%2F(2*(2pi%2F0.3+*sqrt(17)%2F4)*(1%2F4))*sinh%5E-1((2pi%2F0.3+sqrt(17)%2F4*1%2F4+*t)%2Fsqrt(1%2B(1%2F4)%5E2))
height = 3.295  # this is given as a solution to the equation I link above

# The angular rate at which the twists/ are wound. The larger the number, the denser the twists. 
# We need each twist to be 0.3 meters apart as measured on the surface of the cone. 
a = 2*pi/0.3 * sqrt(17)/4.0
# The radius of the cone at vertical distance 1. 
# Given by the restriction that the width of the base of the cone should be double its height.
# Initially I had equal height/4.0 which is wrong
r = 1/4.0  

# draw the spiral 
pointsPerUnit = 1000  # the density of points to draw our curve smooth (and also do our numerical validation at the end)
# define the domain of the vertical dimention z, because x and y are defined based on z
z = [i/float(pointsPerUnit) for i in range(0, int(height*pointsPerUnit) +1)] 
x = [t*r*cos(a*t) for t in z]
y = [t*r*sin(a*t) for t in z]

# also draw the light bulbs individually
distanceBetweenBulbs = 0.3
# it is not easy to find the position of the bulbs analytically. We would have to solve 100 arc length equation. 
# my initial idea to divide the z azis to 100 equidistannt coordinates does not work, because distance on the 
# spiral is not linearly connected to vertical distance from the corner of the cone. What we can do instead is to 
# calculate each point numerically and appoximately, by using the many points we caclulated before and measure the 
# distance that they cover.


# The first point is a bulb (as well as the last, that we will add at the end)
xbulbs = [0]; ybulbs = [0]; zbulbs = [0] 
bulbs = 1
px, py, pz = (0,0,0)
distanceFromLastBulb = 0
for cx,cy,cz in zip(x,y,z):
    interpointDistance = sqrt((cx-px)*(cx-px) + (cy-py)*(cy-py) + (cz-pz)*(cz-pz))
    if distanceFromLastBulb + interpointDistance > distanceBetweenBulbs:
        # choose a point that is in between the current and the last. Just use linear interpolation on the z axis
        # even though it is not accurate (the real relationship is not linear) it is good enough because our initial 
        # curve is plotted with many points.
        weighPrevPoint = (distanceBetweenBulbs - distanceFromLastBulb) / interpointDistance
        weightCurrPoint = 1 - weighPrevPoint
        estimateZ = weighPrevPoint * pz + weightCurrPoint * cz
        estimateX = estimateZ*r*cos(a*estimateZ)
        estimateY = estimateZ*r*sin(a*estimateZ)
        
        xbulbs.append(estimateX); ybulbs.append(estimateY); zbulbs.append(estimateZ)
        bulbs +=1
        px, py, pz = (estimateX, estimateY, estimateZ)
        distanceFromLastBulb = 0

    else:
        # move to the next point
        distanceFromLastBulb += interpointDistance
        px, py, pz = (cx, cy, cz)

# the last bulb is the last point (let's see how this approxiamtion works. Worked perfectly with the first run!)
xbulbs.append(x[-1]); ybulbs.append(y[-1]); zbulbs.append(z[-1])
print "We placed", bulbs+1, 'bulbs on the wire/spiral.'


fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(x, y, z, linewidth = 2, color='green')
ax.plot(xbulbs, ybulbs, zbulbs, marker = 'o', linewidth = 0, color='red')
plt.show() 


# verifying that the height solution given by the equation indeed produces a spiral wire of length 29.7 meters
px, py, pz = (0,0,0)
distance = 0
for cx,cy,cz in zip(x,y,z):
    distance += sqrt((cx-px)*(cx-px) + (cy-py)*(cy-py) + (cz-pz)*(cz-pz))
    px, py, pz = (cx, cy, cz)

print 'Total length of wire for height', height, 'is:', distance


# This was the wrong calculation where I have taken r = height/4
# http://www.wolframalpha.com/input/?i=29.7%20%3D%200.5t*sqrt(1%2B(t%2F4)%5E2*(1%2B(2pi%2F0.3)%5E2*t%5E2))%2B(1%2B(t%2F4)%5E2)%2F(2*(2pi%2F0.3)*(t%2F4))*sinh%5E-1((2pi%2F0.3%20*t%2F4%20*t)%2Fsqrt(1%2B(t%2F4)%5E2))