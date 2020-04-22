import matplotlib.pyplot as plt
from celluloid import Camera
import numpy as np

'''
    This program can draw Lines of Electric Force(LEF).
    We can locate the positive and negative charges on 30X30 2D Grid. 
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


fig, ax = plt.subplots()
cam = Camera(fig)
plt.xlim(-15, 15)
plt.ylim(-15, 15)


n = 30              # numbers of LEF
Qp = [(-8, 0, 1)]   # positive charge (coord_x, coord_y, quantity)
Qn = [(8, 0, -1)]   # negative charge (coord_x, coord_y, quantity)
v0 = 3
k = 1

for positives in Qp:
    LEF = list()
    isflow = list()
    v = list()
    for _ in range(n):
        LEF.append([[positives[0], positives[1]]])
        v.append([0, 0])
        isflow.append(True)

    margin = 0.5
    angle_step = round((np.pi * 2 / n), 4)
    for i in range(n):
        LEF[i][0][0] += margin * np.cos(angle_step * i)
        LEF[i][0][1] += margin * np.sin(angle_step * i)
        v[i][0] += v0 * np.cos(angle_step * i)
        v[i][1] += v0 * np.sin(angle_step * i)

    step = 0.5
    LEF[i].append([LEF[i][-1][0] + step*v[i][0], LEF[i][-1][1] + step*v[i][1]])
    while True:
        cnt = 0
        for i in range(n):
            if(not isflow[i]):
                continue

            if(LEF[i][-1][0] > 15 or LEF[i][-1][0] < -15 or LEF[i][-1][1] > 15 or LEF[i][-1][1] < -15):
                isflow[i] = False
                continue

            if Qn:
                for negatives in Qn:
                    if(distance(LEF[i][-1][0], LEF[i][-1][1], negatives[0], negatives[1]) < 1):
                        isflow[i] = False
                        continue

            v[i][0], v[i][1] = F(LEF[i][-1][0], LEF[i][-1][1])
            LEF[i].append([LEF[i][-1][0] + step*v[i][0],
                           LEF[i][-1][1] + step*v[i][1]])
            cnt += 1

        if(cnt == 0):
            break

    for lines in LEF:
        x, y = list()
        for coords in lines:
            x.append(coords[0])
            y.append(coords[1])
        plt.plot(x, y)
plt.show()
