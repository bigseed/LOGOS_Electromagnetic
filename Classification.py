import matplotlib.pyplot as plt
from celluloid import Camera
import numpy as np

'''
    Classification version of LEF and EF proj.
    Draw LEF(Lines of Electric Force) on palette and
    simulating charge movement on it.
'''


class Electric():
    def __init__(self, Q):
        self.Q = Q
        self.Qp, self.Qn = list(), list()
        for charge in Q:
            if charge[2] > 0:
                self.Qp.append(charge)
            else:
                self.Qn.append(charge)
        self.k = 0.5

    def distance(self, x1, y1, x2, y2):
        dis = np.sqrt((x1 - x2)**2+(y1 - y2)**2)
        return round(dis, 5)

    def Fx(self, x, y, q):
        k = self.k
        fx = 0
        for i in q:
            fx += k * (x - i[0]) / (self.distance(x, y, i[0], i[1])**3)
        return fx

    def Fy(self, x, y, q):
        k = self.k
        fy = 0
        for i in q:
            fy += k * (y - i[1]) / (self.distance(x, y, i[0], i[1])**3)
        return fy

    def F(self, x, y):
        Qp, Qn = self.Qp, self.Qn
        if Qn:
            fx = self.Fx(x, y, Qp) - self.Fx(x, y, Qn)
            fy = self.Fy(x, y, Qp) - self.Fy(x, y, Qn)
        else:
            fx = self.Fx(x, y, Qp)
            fy = self.Fy(x, y, Qp)
        return (fx, fy)

    def arrow(self, X, Y, dx, dy, k, color):
        pointX = X + k*dx
        pointY = Y + k*dy
        d = k*np.sqrt(dx**2 + dy**2)
        sin = k*dy/d
        cos = k*dx/d
        r_3 = np.sqrt(3)

        RPX = pointX + d*(-r_3*cos/2 + sin/2)/5
        RPY = pointY + d*(-cos/2 - r_3*sin/2)/5
        LPX = pointX + d*(-r_3*cos/2 - sin/2)/5
        LPY = pointY + d*(cos/2 - r_3*sin/2)/5

        plt.plot([X, pointX], [Y, pointY], c=color)
        plt.plot([pointX, RPX], [pointY, RPY], c=color)
        plt.plot([pointX, LPX], [pointY, LPY], c=color)

    def paintLEF(self, n):
        v0 = 3
        LEFS = []
        for positives in self.Qp:
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
            LEF[i].append([LEF[i][-1][0] + step*v[i][0],
                           LEF[i][-1][1] + step*v[i][1]])
            while True:
                cnt = 0
                for i in range(n):
                    if(not isflow[i]):
                        continue

                    if(LEF[i][-1][0] > 15 or LEF[i][-1][0] < -15 or LEF[i][-1][1] > 15 or LEF[i][-1][1] < -15):
                        isflow[i] = False
                        continue

                    if self.Qn:
                        for negatives in self.Qn:
                            if(self.distance(LEF[i][-1][0], LEF[i][-1][1], negatives[0], negatives[1]) < 1):
                                isflow[i] = False
                                continue

                    v[i][0], v[i][1] = self.F(LEF[i][-1][0], LEF[i][-1][1])
                    LEF[i].append([LEF[i][-1][0] + step*v[i][0],
                                   LEF[i][-1][1] + step*v[i][1]])
                    cnt += 1

                if(cnt == 0):
                    break
            LEFS.append(LEF)

        for negatives in self.Qn:
            LEF = list()
            isflow = list()
            v = list()
            for _ in range(n):
                LEF.append([[negatives[0], negatives[1]]])
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
            LEF[i].append([LEF[i][-1][0] + step*v[i][0],
                           LEF[i][-1][1] + step*v[i][1]])
            while True:
                cnt = 0
                for i in range(n):
                    if(not isflow[i]):
                        continue

                    if(LEF[i][-1][0] > 15 or LEF[i][-1][0] < -15 or LEF[i][-1][1] > 15 or LEF[i][-1][1] < -15):
                        isflow[i] = False
                        continue

                    if self.Qp:
                        for positives in self.Qp:
                            if(self.distance(LEF[i][-1][0], LEF[i][-1][1], positives[0], positives[1]) < 1):
                                isflow[i] = False
                                continue

                    v[i][0], v[i][1] = self.F(LEF[i][-1][0], LEF[i][-1][1])
                    LEF[i].append([LEF[i][-1][0] - step*v[i][0],
                                   LEF[i][-1][1] - step*v[i][1]])
                    cnt += 1

                if(cnt == 0):
                    break
            LEFS.append(LEF)

        return LEFS

    def paintEF(self, frame, drawLEF=True):
        fig, ax = plt.subplots()
        cam = Camera(fig)
        plt.xlim(-15, 15)
        plt.ylim(-15, 15)

        X, Y = -6, -6
        vx, vy = 0, 0
        LEFS = self.paintLEF(30)

        for _ in range(frame):
            if drawLEF:
                for LEF in LEFS:
                    for lines in LEF:
                        x = []
                        y = []
                        for coords in lines:
                            x.append(coords[0])
                            y.append(coords[1])
                        plt.plot(x, y)

            for charge in self.Q:
                qx, qy, qq = charge[0], charge[1], charge[2]
                if qq > 0:
                    plt.scatter(qx, qy, c='red', s=qq*7)
                else:
                    plt.scatter(qx, qy, c='blue', s=-qq*7)
            plt.scatter(X, Y, c='green')

            ax, ay = self.F(X, Y)

            vx += ax
            vy += ay
            self.arrow(X, Y, vx, vy, 6, 'k')
            self.arrow(X, Y, ax, ay, 90, 'm')
            X += vx
            Y += vy

            cam.snap()

        animation = cam.animate(interval=30)
        animation.save('EF1.mp4')
        print('Complete')


sample1_Q = [(-6, 6, 2), (6, -6, -2)]
sample2_Q = [(-7, 9, 3), (2, -6, -5), (10, 6, -4)]

model = Electric(sample1_Q)
model.paintEF(300)
