# -*- coding: utf-8 -*-
import numpy as np
#import matplotlib.pyplot as plt
import math


def lineCluster(lines):
    npSample = lines
    endPoints = []

    significants = []

    for points_ in  npSample:

        stretched = stretchLine(points_[0,0],points_[0,1],points_[0,2],points_[0,3])
        
        if stretched is False:
            continue

        else: 
            points_[0] = stretched


        xs = [points_[0,0],points_[0,2]]
        ys = [points_[0,1],points_[0,3]]
        
        theta = np.arctan2(ys[1] - ys[0], xs[1] - xs[0])/np.pi

        if abs(theta) > 0.1:
            # 직선 거리 계산
            changedFlag =  False
            if not significants:
                significants.append( [theta,points_])

            for sig in significants:
                if abs(sig[0] - theta) < 0.05 and isCloseLine(sig, theta, points_): #isCloseLine(sig, theta, points_)
                    sig[0] = (sig[0] + theta )/2
                    sig[1] = (sig[1] + points_)/2
                    changedFlag = True
                    break
            
            if not changedFlag:
                significants.append([theta,points_])
    

    return get2lines(significants)
    
    

def isCloseLine(sig, theta, points_):
    sigThta, sigPoints = sig[0], sig[1]

    if abs(sigThta - theta) > 0.1:
        return False # 각이 안비슷하면 거짓

    numOfDots = 5
    criteria = 2000  # 기준이 눈대중이라 수정 필요할 수도
    # minimum -> 어처피 기울기가 비슷하기 때문 

    # sig :array([1150,  306, 1290,  661])]
    # points_ : array([634, 796, 783, 349])]
    sigx = np.linspace(sigPoints[0,0],sigPoints[0,2],numOfDots)
    sigy = np.linspace(sigPoints[0,1],sigPoints[0,3],numOfDots)

    xs = np.linspace(points_[0,0],points_[0,2],numOfDots)
    ys = np.linspace(points_[0,1],points_[0,3], numOfDots)

    for i in range(numOfDots):
        sigx_ , sigy_ = sigx[i], sigy[i]
        for j in range(numOfDots):
            xs_ , ys_ = xs[j], ys[j]
            distance =  (xs_-sigx_)**2 + (ys_ - sigy_)**2   
            if distance < criteria:
                return True

    return False

def stretchLine(x1,y1,x2,y2):
  
    # 직선 구하기 y = ax +b  , x = (y-b)/a -> 직선 검출 후 화면 양 끝까지 땡김
    if abs(x2-x1) <0.01:
        return False

    a = (y2 - y1)/(x2 - x1)
    b = y2 - a*x2

    if abs(a)< 0.1:
        return False

    newX1 = -b/a
    newY1 = 0
    newX2 = (1080-b)/a
    newY2 = 1080
    print("streteched:  ", [newX1,newY1,newX2,newY2])
    return np.array([newX1,newY1,newX2,newY2])


def get2lines(significants):
    size = len(significants)
    print( "size : " , size)
    print("111",significants)
    if size <=1 :
        return []
    
    if size == 2:
        return significants
    
    if size > 6:
        return []
    
    minCoherence = math.inf
    minLeft, minRight = [0,1]

    for i in range(0,size):
        for j in range(i+1,size):
            left = significants[i][1][0]
            right = significants[j][1][0]
            print("left",left)
            print("right:" ,right, " -> ")
            right[0] = 1920 - right[0] # 점대칭 ->프레임 크기 맞춰서 파라미터 수정 
            right[2] = 1920 - right[2]
            print(right)    
            right[0] = 1920 - right[0] # 점대칭 ->프레임 크기 맞춰서 파라미터 수정 
            right[2] = 1920 - right[2]
            

        
            if minCoherence > getCoherence(left,right):
                minCoherence = getCoherence(left,right)
                minleft,minRight = i, j 
    print(significants)
    print( minLeft,minRight)
    return [significants[minLeft],significants[minRight]]

def getCoherence(left,right):
    return abs(left[0] - right[0]) + abs(left[2] - right[2])


    


 
    
