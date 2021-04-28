# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import math

sample = [ [663, 800, 834, 304],
[1087,  300, 1258,  797],
[643, 799, 818, 318],
[664, 800 ,835 ,303],
[1086 , 300, 1257 , 798],
[642 ,797, 761 ,472]
]

sample2 = [
    [ 350, 500, 500, 0],
    [ 401,  801 , 905 , 801],

 [ 657 , 797  ,808  ,303],

 [1149,  329, 1329,  799],

 [1152,  300, 1287,  632],

 [1140,  303, 1256,  607],

 [ 628 , 795,  731,  494],

 [ 626 , 797 , 797 , 300],

 [1155 , 305, 1299,  661]]

#직선 : [기울기 , [ [], []]]

def solution():
    print(np.__version__)
    npSample = np.array(sample)
    endPoints = []
    plt.figure()
    significants = []

    for points_ in  npSample:
        print("points : ", points_)
        # 전체 크기 가로 0 - 1920 , 세로 : 0:1080
        # 세로 0, 1080 짜리 라인으로 바꾸자.

        x1_,y1_ = points_[0], points_[1]
        x2_,y2_ = points_[2], points_[3]

        # 직선 구하기 y = ax +b  , x = (y-b)/a
        a = (y2_ - y1_)/(x2_ - x1_)
        b = y2_ - a*x2_

        newX1 = -b/a
        newY1 = 0
        newX2 = (1080-b)/a
        newY2 = 1080

        xs = [newX1,newX2]
        ys = [newY1,newY2]
        print( [newX1,newY1] , [newX2,newY2])
        points_ = np.array([newX1,newY1,newX2,newY2])
        
#       tan = (ys[1] - ys[0]) / (xs[1] - xs[0] +0.0)
#       print("tan", tan)
        theta = np.arctan2(ys[1] - ys[0], xs[1] - xs[0])/np.pi

        if abs(theta) > 0.1:
            # 직선 거리 계산
            changedFlag =  False
            if not significants:
                significants.append( [theta,points_])
                print("initial add")

            for sig in significants:
                if abs(sig[0] - theta) < 0.05 and isCloseLine(sig, theta, points_): #isCloseLine(sig, theta, points_)
                    sig[0] = (sig[0] + theta )/2
                    print("sigg[1]", sig[1])
                    print("points_ ", points_)
                    sig[1] = (sig[1] + points_)/2
                    changedFlag = True
                    break
            
            if not changedFlag:
                significants.append([theta,points_])
                    
            
            plt.plot(xs,ys,"r--")
            plt.scatter(xs,ys)


    # test if clustered 
    plt.figure("clustered")
    for item in significants:
        print(item)
        plt.plot( [item[1][0],item[1][2] ] , [item[1][1],item[1][3]], "r--")
        

    plt.show()

def isCloseLine(sig, theta, points_):
    sigThta, sigPoints = sig[0], sig[1]

    if abs(sigThta - theta) > 0.1:
        return False # 각이 안비슷하면 거짓

    numOfDots = 5
    criteria = 2000  # 기준이 눈대중이라 수정 필요할 수도
    # minimum -> 어처피 기울기가 비슷하기 때문 

    # sig :array([1150,  306, 1290,  661])]
    # points_ : array([634, 796, 783, 349])]
    sigx = np.linspace(sigPoints[0],sigPoints[2],numOfDots)
    sigy = np.linspace(sigPoints[1],sigPoints[3],numOfDots)

    xs = np.linspace(points_[0],points_[2],numOfDots)
    ys = np.linspace(points_[1],points_[3], numOfDots)

    for i in range(numOfDots):
        sigx_ , sigy_ = sigx[i], sigy[i]
        for j in range(numOfDots):
            xs_ , ys_ = xs[j], ys[j]
            distance =  (xs_-sigx_)**2 + (ys_ - sigy_)**2   
            if distance < criteria:
                return True

    return False

solution()