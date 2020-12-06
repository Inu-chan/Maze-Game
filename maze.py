# coding=gbk

import random as rd
import numpy as np
from dataStructures import Queue
from dataStructures import DisJointSet

def pointToInt(point: tuple, row, col) -> int:  # ���Ͻ�(0,0)
    return point[0] * col + point[1]

gateNum = 2

class maze:  # �Թ��࣬�洢�Թ��ĸ���
    def __init__(self, row: int, col: int, unique=True, gate=True):  # row���У�col����,unique·���Ƿ�Ψһ��gate�Ƿ��д�����
        self.row = row
        self.col = col
        self.grid = np.zeros((row * 2, col * 2))  # ��ȫ���0 - 0��ǽ��1����,2-4�Ǵ�����
        self.score = np.zeros((row*2,col*2))  # ����
        self.scoreNum = 0  # ���ֿ�����
        self.djs = DisJointSet(row * col + 3)  # ���鼯�����ڼ����Ƿ�����ͬһ����
        self.way = 0  # ������������ʱδ�ã�
        self.gate = {}  # ������
        self.s = (0,0)  # �Թ����
        self.t = (row-1,col-1)  # �Թ��յ�
        self.makeWay(self.s[0], self.s[1], self.t[0], self.t[1], unique, gate)  # �趨��㡢�յ㣬����һ��·�����޸Ĳ���ֵ
        self.t = (row*2-2,col*2-2)  # ʵ���յ��������е�λ��Ҫ����
        self.grid_l = self.grid.tolist()  # ���б���ʽ�洢
        self.solution = np.zeros((row * 2, col * 2))  # �Թ������·��
        self.path = []
        self.dis = []  # ��㵽�յ����

        bfs(self)  # �����������Ž�
        # self.printPath()  # ��ӡ·��

    def connect(self, x1, x2, y1, y2) -> bool:
        pA = pointToInt((x1, x2), self.row, self.col)
        pB = pointToInt((y1, y2), self.row, self.col)
        return self.djs.same(pA, pB)

    def addGate(self):
        randPoint1 = (rd.randint(0, self.row - 1), rd.randint(0, self.col - 1))
        randPoint2 = (rd.randint(0, self.row - 1), rd.randint(0, self.col - 1))
        while randPoint1 == self.s or randPoint1 == self.t or (randPoint1 in self.gate):
            randPoint1 = (rd.randint(0, self.row - 1), rd.randint(0, self.col - 1))  # ����������㡢�յ㡢�����������ص�������������
        while randPoint2 == self.s or randPoint2 == self.t or (randPoint2 in self.gate) or randPoint2 == randPoint1:
            randPoint2 = (rd.randint(0, self.row - 1), rd.randint(0, self.col - 1))  # ����������㡢�յ㡢�����������ص�������������

        pA = pointToInt(randPoint1, self.row, self.col)
        pB = pointToInt(randPoint2, self.row, self.col)

        randPoint1 = (randPoint1[0]*2, randPoint1[1]*2)
        randPoint2 = (randPoint2[0]*2, randPoint2[1]*2)

        self.djs.merge(pA,pB)
        self.gate[randPoint1] = randPoint2
        self.gate[randPoint2] = randPoint1
        global gateNum
        self.grid[randPoint1[0]][randPoint1[1]] = gateNum
        self.grid[randPoint2[0]][randPoint2[1]] = gateNum
        gateNum += 1

    def makeWay(self, sx, sy, tx, ty, unique, gate):
        if gate:
            for i in range(3):
                self.addGate()
        while not self.connect(sx, sy, tx, ty):
            randPoint = (rd.randint(0, self.row - 1), rd.randint(0, self.col - 1))
            randDir = rd.randint(0, 1)  # �� �� �� ��
            if randDir == 0 and randPoint[1] == self.col - 1:
                continue
            if randDir == 1 and randPoint[0] == self.row - 1:
                continue
            if randDir == 0:
                nextPoint = (randPoint[0], randPoint[1] + 1)
                pA = pointToInt(randPoint, self.row, self.col)
                pB = pointToInt(nextPoint, self.row, self.col)
                if not unique or not self.djs.same(pA, pB):
                    self.djs.merge(pA, pB)
                    self.way += 1
                    self.grid[randPoint[0] * 2][randPoint[1] * 2] = max(1, self.grid[randPoint[0] * 2][randPoint[1] * 2])
                    self.grid[randPoint[0] * 2][randPoint[1] * 2 + 1] = max(1, self.grid[randPoint[0] * 2][randPoint[1] * 2 + 1])
                    self.grid[nextPoint[0] * 2][nextPoint[1] * 2] = max(1, self.grid[nextPoint[0] * 2][nextPoint[1] * 2])
                    if rd.randint(1,6)==5:
                        self.score[randPoint[0] * 2][randPoint[1] * 2 + 1] = 1
                        self.scoreNum += 1
            else:
                nextPoint = (randPoint[0] + 1, randPoint[1])
                pA = pointToInt(randPoint, self.row, self.col)
                pB = pointToInt(nextPoint, self.row, self.col)
                if not unique or not self.djs.same(pA, pB):
                    self.djs.merge(pA, pB)
                    self.way += 1
                    self.grid[randPoint[0] * 2][randPoint[1] * 2] = max(1, self.grid[randPoint[0] * 2][randPoint[1] * 2])
                    self.grid[randPoint[0] * 2 + 1][randPoint[1] * 2] = max(1, self.grid[randPoint[0] * 2 + 1][randPoint[1] * 2])
                    self.grid[nextPoint[0] * 2][nextPoint[1] * 2] = max(1, self.grid[nextPoint[0] * 2][nextPoint[1] * 2])
                    if rd.randint(1,6)==5:
                        self.score[randPoint[0] * 2 + 1][randPoint[1] * 2] = 1
                        self.scoreNum += 1

    def printPath(self):
        print("Solution:",end=' ')
        for step in self.path[:-1]:
            print("(%d,%d)->" % (step[0],step[1]),end='')
        print("(%d,%d)" % (self.path[-1][0],self.path[-1][1]))

direction = [(1,0),(0,1),(-1,0),(0,-1)]

pre = dict()  # �洢ÿ�����ǰ���������Ķ����������ģ�

def out(p:tuple, m:maze) -> bool:  # �ж�һ�����Ƿ����
    return not (p[0] <= m.row*2 and p[0] >= 0 and p[1] <= m.col*2 and p[1] >= 0)

def bfs(m: maze):
    vis = set()  # ���ʹ��ĵ���ɵļ��ϣ��Է�ֹ�ظ�����
    dis = dict()  # �洢ÿ�������Դ��ľ���
    q = Queue()
    dis[m.s] = 0
    vis.add(m.s)
    q.push(m.s)

    while not q.empty():
        now = q.pop()

        if now in m.gate:
            nextPoint = m.gate[now]
            if nextPoint not in vis:
                dis[nextPoint] = dis[now]
                vis.add(nextPoint)
                pre[nextPoint] = now
                q.push(nextPoint)
                # continue

        if now == m.t:  # ���յ���
            recordPath(pre[m.t], m.s, m)  # ��ӡ·������������m.solution��
            m.solution[m.t[0]][m.t[1]] = 2  # �յ����·��
            m.path.append((m.t[0], m.t[1]))
            m.dis = dis[now] + 1
            return "Find Path!"

        for i in direction:
            nextPoint = (now[0] + i[0], now[1] + i[1])
            if m.grid[nextPoint[0]][nextPoint[1]] == 0 or out(nextPoint,m):
                continue
            if nextPoint not in vis:
                dis[nextPoint] = dis[now] + 1
                vis.add(nextPoint)
                pre[nextPoint] = now
                q.push(nextPoint)
        # end while
    return "Cannot find path"

def recordPath(p, s, m:maze):  # �ݹ��ҵ���ʱ��·
    if p != s:
        recordPath(pre[p], s, m)
    m.solution[p[0]][p[1]] = 2
    m.path.append((p[0],p[1]))

if __name__ == '__main__':
    r, c = input("�������Թ����С��У��ÿո����").split()
    M = maze(int(r), int(c), unique=True, gate=True)
    print(M.grid)
    # bfs(M)
