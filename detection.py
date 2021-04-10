# -*- coding: utf-8 -*-
# Steve Mitchell
# June 2017

import numpy as np
#import matplotlib
#import matplotlib.pyplot as plt
#import argparse
import cv2
import imutils
import time

from lineCluster import lineCluster

# preliminary attempt at lane following system
# largely derived from: https://medium.com/pharos-production/
# road-lane-recognition-with-opencv-and-ios-a892a3ab635c

# identify filename of video to be analyzed
cap = cv2.VideoCapture('mov_0087.mp4') #  1) 비디오를 읽어옴

# loop through until entire video file is played
while(cap.isOpened()):

    # read video frame & show on screen
    # ret -> True, false : 프레임이 있는지 없는지,
    # fram -> 찍히는 프레임 
    ret, frame = cap.read() # 2) 프레임 로드 

    if not ret:
        break
    # cv2.imshow("Original Scene", frame)
    # snip section of video frame of interest & show on screen
    snip = frame[0:1080,0:1920] # 3) [0:1080, 0:1920 ]은 전체 화면 크기.... 나중에 이거 기준으로 크기 설정 ..
    cv2.imshow("Snip",snip) # 4) 전체 화면을 화면에 띄움

    # create polygon (trapezoid) mask to select region of interest
    
    # snip.shape : [로우, 칼럼, 타입(binary or bgr ) : print("snip Shape : ", snip.shape)  : (1080, 1920, 3)

    mask = np.zeros((snip.shape[0], snip.shape[1]), dtype="uint8") # snip 크기의 마스크 [0]으로 되어있음 
    cv2.imshow("test",mask)
    pts = np.array([[400, 800], [600, 300], [1320, 300], [1520, 800]], dtype=np.int32) # 해당 범위에 비트 and wise calculation -> othes are black 
    # pts 필터 적용할 크기 멀수록 작아 보여서 마름모 
    cv2.fillConvexPoly(mask, pts,255) # fillconvexPoly : 꽉찬 다각형, 255(가장 흰색) 로 채운다.
    cv2.imshow("Mask", mask)
    # apply mask and show masked image on screen
    masked = cv2.bitwise_and(snip, snip, mask=mask) # 마름모꼴만 남김 
    cv2.imshow("Region of Interest", masked)
    
    # convert to grayscale then black/white to binary image
    frame = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY) # 흑백으로 만들기 ... 이 아래는 흑백으로 봄

    thresh = 200 # 흑백으로 만들어서 200 넘으면 1 아니면 0 
    frame = cv2.threshold(frame, thresh, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow("Black/White", frame)

    # blur image to help with edge detection
    blurred = cv2.GaussianBlur(frame, (11, 11), 0) # 캐니 디텍션을 위한 가우시안 필터 
    # cv2.imshow("Blurred", blurred)

    # identify edges & show on screen
    # 캐니 이미지 -> 직선 검출을 위한 이미지 근사 필터
    edged = cv2.Canny(blurred, 30, 150)
    cv2.imshow("Edged", edged)

    # perform full Hough Transform to identify lane lines
    #lines = cv2.HoughLines(edged, 1, np.pi / 180, 25)
    #lines = cv2.HoughLines(edged, 0.8, np.pi / 180, 150, srn = 100, stn = 200, min_theta = 0, max_theta = np.pi)
    #print(lines)

    lines = cv2.HoughLinesP(edged, 0.8, np.pi / 180, 50, minLineLength = 300, maxLineGap = 100)
    whiteBox = np.ones((snip.shape[0], snip.shape[1]), dtype="uint8") * 255
    whiteBox2 = np.ones((snip.shape[0], snip.shape[1]), dtype="uint8") * 255
    # f = open("lineLog.txt","a+")
    
    if lines is not None:
        #lines = getSignificantLines(lines)
        #print("\nline " )
        
        #f.write("\n\n line ")

        clusteredLines = lineCluster(lines)

        for i in lines:
            cv2.line(whiteBox, (i[0][0], i[0][1]), (i[0][2], i[0][3]), (0, 0, 255), 2)
            cv2.circle(whiteBox, (i[0][0], i[0][1]), 20 , (230,9,68), -1)
            cv2.circle(whiteBox, (i[0][2], i[0][3]), 20 , (39,9,230), -1)
            #print(str(i))
            #f.write(str(i)+"\n")
        cv2.imshow("dst", whiteBox)


        for cline in clusteredLines:
            cline = cline[1].astype(np.int32)
            print("int cline : ", cline)
            cv2.line(whiteBox2, (cline[0,0], cline[0,1] ), (cline[0,2], cline[0,3]),(0, 0, 255), 2 )
        cv2.imshow("clustered", whiteBox2)

    #f.close()

    """
    # define arrays for left and right lanes
    rho_left = []
    theta_left = []
    rho_right = []
    theta_right = []

    # ensure cv2.HoughLines found at least one line
    if lines is not None:

        # loop through all of the lines found by cv2.HoughLines
        for i in range(0, len(lines)):

            # evaluate each row of cv2.HoughLines output 'lines'
            for rho, theta in lines[i]:

                # collect left lanes
                if theta < np.pi/2 and theta > np.pi/4:
                    rho_left.append(rho)
                    theta_left.append(theta)

                    # # plot all lane lines for DEMO PURPOSES ONLY
                    # a = np.cos(theta); b = np.sin(theta)
                    # x0 = a * rho; y0 = b * rho
                    # x1 = int(x0 + 400 * (-b)); y1 = int(y0 + 400 * (a))
                    # x2 = int(x0 - 600 * (-b)); y2 = int(y0 - 600 * (a))
                    #
                    # cv2.line(snip, (x1, y1), (x2, y2), (0, 0, 255), 1)

                # collect right lanes
                if theta > np.pi/2 and theta < 3*np.pi/4:
                    rho_right.append(rho)
                    theta_right.append(theta)

                    # # plot all lane lines for DEMO PURPOSES ONLY
                    # a = np.cos(theta); b = np.sin(theta)
                    # x0 = a * rho; y0 = b * rho
                    # x1 = int(x0 + 400 * (-b)); y1 = int(y0 + 400 * (a))
                    # x2 = int(x0 - 600 * (-b)); y2 = int(y0 - 600 * (a))
                    #
                    # cv2.line(snip, (x1, y1), (x2, y2), (0, 0, 255), 1)

    # statistics to identify median lane dimensions
    left_rho = np.median(rho_left)
    left_theta = np.median(theta_left)
    right_rho = np.median(rho_right)
    right_theta = np.median(theta_right)

    # plot median lane on top of scene snip
    if left_theta > np.pi/4:
        a = np.cos(left_theta); b = np.sin(left_theta)
        x0 = a * left_rho; y0 = b * left_rho
        offset1 = 250; offset2 = 800
        x1 = int(x0 - offset1 * (-b)); y1 = int(y0 - offset1 * (a))
        x2 = int(x0 + offset2 * (-b)); y2 = int(y0 + offset2 * (a))

        cv2.line(snip, (x1, y1), (x2, y2), (0, 255, 0), 6)

    if right_theta > np.pi/4:
        a = np.cos(right_theta); b = np.sin(right_theta)
        x0 = a * right_rho; y0 = b * right_rho
        offset1 = 290; offset2 = 800
        x3 = int(x0 - offset1 * (-b)); y3 = int(y0 - offset1 * (a))
        x4 = int(x0 - offset2 * (-b)); y4 = int(y0 - offset2 * (a))

        cv2.line(snip, (x3, y3), (x4, y4), (255, 0, 0), 6)



    # overlay semi-transparent lane outline on original
    if left_theta > np.pi/4 and right_theta > np.pi/4:
        pts = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], dtype=np.int32)

        # (1) create a copy of the original:
        overlay = snip.copy()
        # (2) draw shapes:
        cv2.fillConvexPoly(overlay, pts, (0, 255, 0))
        # (3) blend with the original:
        opacity = 0.4
        cv2.addWeighted(overlay, opacity, snip, 1 - opacity, 0, snip)

    cv2.imshow("Lined", snip)
    """

    # perform probablistic Hough Transform to identify lane lines
    # lines = cv2.HoughLinesP(edged, 1, np.pi / 180, 20, 2, 1)
    # for x in range(0, len(lines)):
    #     for x1, y1, x2, y2 in lines[x]:
    #         cv2.line(snip, (x1, y1), (x2, y2), (0, 0, 255), 2)


    # press the q key to break out of video
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# clear everything once finished
cap.release()
cv2.destroyAllWindows()
