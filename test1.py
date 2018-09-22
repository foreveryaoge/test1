# -*- coding: utf-8 -*-
#hello world
"""
Created on Tue Sep 18 09:28:24 2018

@author: zhaoyao
"""

import numpy as np
import time
def str_matrix(n,temp=[]):
    matrixD=[]
    for k in range(0,n):
        temp1=[]
        for i in range(k*n,k*n+n):
            temp1.append(temp[i])
        matrixD.append(temp1)
    matrixA=np.array(matrixD)
    return(matrixA)

def way_input():
    while(True):
        n=input("请选择输入矩阵的方式：1、文件输入；2、屏幕输入\n",)
        if n =='1':
            print('已选择文件输入方式\n')
            way='infile.txt'
            a,b,n=readFile(way)
            print('a',a)
            print('b',b)
            return(a,b,n)
            
        elif n=='2':
            print('已选择屏幕输入\n')
            n=int(input('请输入矩阵阶数N:'))
            a=input('请输入矩阵初始状态，例如：2阶矩阵1 2 3 4（间隔一个空格)\n')
            data=a.strip('\n')
            a=data.split(' ')
            a=str_matrix(n,a)
            b=input('请输入矩阵目标状态，例如：2阶矩阵1 2 3 4（间隔一个空格)\n')
            data=b.strip('\n')
            b=data.split(' ')
            b=str_matrix(n,b)
            print('a:',a)
            print('b:',b)
            return(a,b,n)
            
        else:
            print('选择方式错误，请重新选择输入方式！！！！！！！！！！\n')

def readFile(path):
    f=open(path)
    matrixA=[]
    matrixB=[]
    temp=[]
    for data in f.readlines():
        data=data.strip('\n')
        num=data.split(' ')
        temp.append(num)
    n=int(temp[0][0])
    matrixA=str_matrix(n,temp[1])
    matrixB=str_matrix(n,temp[2])
    print('阶N为:',n)
    print('初始状态矩阵为：',matrixA)
    print('目标状态矩阵为：',matrixB)
    print(n)
    return(matrixA,matrixB,n)

class State:
    def __init__(self, state, directionFlag=None, parent=None, depth=1):
        self.state = state    
        self.direction = ['up', 'down', 'right', 'left']
        if directionFlag:
            self.direction.remove(directionFlag)
        self.parent = parent
        self.depth = depth
        num = 0
        for i in range(len(state)):
            for j in range(len(state)):
                if self.state[i, j] != ' 'and self.state[i, j] != self.answer[i, j]:
                    num += 1
        self.cost = num + self.depth

    def getDirection(self):
        return self.direction
								
    def showInfo(self):
        for i in range(self.boarder):
            for j in range(self.boarder):
                print(self.state[i, j], end='  ')
            print("\n")
        print('->')
        return
								
    def getEmptyPos(self):
        postion = np.where(self.state == self.symbol)
        return postion
								
    def generateSubStates(self):
        if not self.direction:
            return []
        subStates = []
        row, col = self.getEmptyPos()
        if 'left' in self.direction and col > 0:    
            s = self.state.copy()
            temp = s.copy()
            s[row, col] = s[row, col-1]
            s[row, col-1] = temp[row, col]
            news = State(s, directionFlag='right', parent=self, depth=self.depth+1)
            subStates.append(news)
        if 'up' in self.direction and row > 0:    
            s = self.state.copy()
            temp = s.copy()
            s[row, col] = s[row-1, col]
            s[row-1, col] = temp[row, col]
            news = State(s, directionFlag='down', parent=self, depth=self.depth+1)
            subStates.append(news)
        if 'down' in self.direction and row < self.boarder-1:
            s = self.state.copy()
            temp = s.copy()
            s[row, col] = s[row+1, col]
            s[row+1, col] = temp[row, col]
            news = State(s, directionFlag='up', parent=self, depth=self.depth+1)
            subStates.append(news)
        if self.direction.count('right') and col <self.boarder-1:
            s = self.state.copy()
            temp = s.copy()
            s[row, col] = s[row, col+1]
            s[row, col+1] = temp[row, col]
            news = State(s, directionFlag='left', parent=self, depth=self.depth+1)
            subStates.append(news)
        return subStates
								
    def solve(self):
        openTable = []
        closeTable = []
        openTable.append(self)
        steps = 0                    
        while len(openTable) > 0:     
            n = openTable.pop(0)
            closeTable.append(n)
            subStates = n.generateSubStates()
            path = []
            for s in subStates:
                if (s.state == s.answer).all():
                    while s.parent and s.parent != originState:
                        path.append(s.parent)
                        s = s.parent
                    path.reverse()
                    return path, steps+1
            openTable.extend(subStates)
            openTable.sort(key=lambda x: x.cost)  
            steps += 1
        else:
            return None, None
										
if __name__ == '__main__':
    symbolOfEmpty = '0'
    State.symbol = symbolOfEmpty
    a,b,n=way_input()
    start=time.clock()
    State.boarder= n
    State.answer = b
    originState = State(a)
    path, steps = originState.solve()
    end=time.clock()
    print(end-start)
    if path:                        
        for node in path:
                node.showInfo()
        print(State.answer)
        print("Total steps is %d" % steps)
				
								
								
								
								
								
								
								
								
								
								
								
								
								
								
								
								
								
								
								
								
								
								