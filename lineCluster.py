# -*- coding: utf-8 -*-
import numpy as np
#import matplotlib.pyplot as plt
import math


def lineCluster(lines):
    npSample = lines
    endPoints = []

    significants = []

    for points_ in  npSample:
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
    
    return significants
    

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


#if __name__ =="__main__":
#    lineCluster()