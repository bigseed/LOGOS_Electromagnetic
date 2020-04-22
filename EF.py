import matplotlib.pyplot as plt
from celluloid import Camera
import numpy as np

'''
    This is program can draw a 1C charge movement on Electric Field.
    We can locate electric charges on 30X30 2D Grid, and also set its amount.
    We can how it moves and the direction of force and its velocity.
'''


def distance(x1, y1, x2, y2):
    dis = np.sqrt((x1 - x2)**2+(y1 - y2)**2)
    return round(dis, 5)


def Fx(x, y, q):
    global k
    fx = 0
    for i in q:
        fx += k * i[2] * (x - i[0]) / (distance(x, y, i[0], i[1])**3)
    return fx


def Fy(x, y, q):
    global k
    fy = 0
    for i in q:
        fy += k * i[2] * (y - i[1]) / (distance(x, y, i[0], i[1])**3)
    return fy

# calculate net force acting on charge


def F(x, y):
    global Qp, Qn
    if Qn:
        fx = Fx(x, y, Qp) + Fx(x, y, Qn)
        fy = Fy(x, y, Qp) + Fy(x, y, Qn)
    else:
        fx = Fx(x, y, Qp)
        fy = Fy(x, y, Qp)
    return (fx, fy)


# plotting arrow
def arrow(x, y, k, color):
    global X, Y

    pointX = X + k*x
    pointY = Y + k*y
    d = k*np.sqrt(x**2 + y**2)
    sin = k*y/d
    cos = k*x/d
    r_3 = np.sqrt(3)

    RPX = pointX + d*(-r_3*cos/2 + sin/2)/5
    RPY = pointY + d*(-cos/2 - r_3*sin/2)/5
    LPX = pointX + d*(-r_3*cos/2 - sin/2)/5
    LPY = pointY + d*(cos/2 - r_3*sin/2)/5

    plt.plot([X, pointX], [Y, pointY], c=color)
    plt.plot([pointX, RPX], [pointY, RPY], c=color)
    plt.plot([pointX, LPX], [pointY, LPY], c=color)


def animate(interval):
    animation = cam.animate(interval=interval)
    animation.save('EF.mp4')
    print('Complete')


fig, axis = plt.subplots()
cam = Camera(fig)
plt.xlim(-15, 15)
plt.ylim(-15, 15)

k = 0.05
X, Y = 0, 0
vx, vy = 0, 0

Qp = [(7, 7, 5)]    # positive charge (coord_x, coord_y, quantity)
Qn = [(-7, 7, -5)]  # negative charge (coord_x, coord_y, quantity)
Q = Qp + Qn
n = len(Q)

for moment in range(0, 100):
    for charge in Q:
        qx, qy, qq = charge[0], charge[1], charge[2]
        if qq > 0:
            plt.scatter(qx, qy, c='red', s=qq)
        else:
            plt.scatter(qx, qy, c='blue', s=-qq)
    plt.scatter(X, Y, c='yellow')

    ax, ay = F(X, Y)

    vx += ax
    vy += ay
    X += vx
    Y += vy
    arrow(vx, vy, 10, 'k')
    arrow(ax, ay, 150, 'm')

    cam.snap()

animate(30)
