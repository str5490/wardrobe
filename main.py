import cv2
import numpy as np
import math
import os, sys
from sklearn.cluster import KMeans
from playsound import playsound
import winsound

def change_TrackbarValue(l_h, u_h, l_s, u_s, l_v, u_v):
    cv2.setTrackbarPos('lower_h','skin_hsv',l_h)
    cv2.setTrackbarPos('upper_h','skin_hsv',u_h)
    cv2.setTrackbarPos('lower_s','skin_hsv',l_s)
    cv2.setTrackbarPos('upper_s','skin_hsv',u_s)
    cv2.setTrackbarPos('lower_v','skin_hsv',l_v)
    cv2.setTrackbarPos('upper_v','skin_hsv',u_v)
# h-색,s-채,v-명 sv(클수록 진하고 밝음)

def nothing(x):
    pass


(l_skinh, u_skinh) = (0, 20)
(l_skins, u_skins) = (105, 255)
(l_skinv, u_skinv) = (40, 220)

cv2.namedWindow('skin_hsv')
cv2.resizeWindow('skin_hsv', 600,300)

cv2.createTrackbar('lower_h','skin_hsv',0,255,nothing)
cv2.createTrackbar('upper_h','skin_hsv',0,255,nothing)
cv2.createTrackbar('lower_s','skin_hsv',0,255,nothing)
cv2.createTrackbar('upper_s','skin_hsv',0,255,nothing)
cv2.createTrackbar('lower_v','skin_hsv',0,255,nothing)
cv2.createTrackbar('upper_v','skin_hsv',0,255,nothing)

change_TrackbarValue(l_skinh, u_skinh, l_skins, u_skins, l_skinv, u_skinv)

def mouse_callback(event, x, y, flags, param):
    global l_skinh, u_skinh, l_skins, u_skins, l_skinv, u_skinv
    if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_RBUTTONDOWN:
        color = frame[y, x]
        one_pixel = np.uint8([[color]])
        hsv = cv2.cvtColor(one_pixel, cv2.COLOR_BGR2HSV)
        hsv = hsv[0][0]

    if event == cv2.EVENT_LBUTTONDOWN:
        print("mouse left clicked: ", hsv)
        if u_skinh < hsv[0]:
            u_skinh = hsv[0]
        elif l_skinh > hsv[0]:
            l_skinh = hsv[0]
        if u_skins < hsv[1]:
            u_skins = hsv[1]
        elif l_skins > hsv[1]:
            l_skins = hsv[1]
        if u_skinv < hsv[2]:
            u_skinv = hsv[2]
        elif l_skinv > hsv[2]:
            l_skinv = hsv[2]
        change_TrackbarValue(l_skinh, u_skinh, l_skins, u_skins, l_skinv, u_skinv)

    if event == cv2.EVENT_RBUTTONDOWN:
        print("mouse write clicked: ", hsv)
        if u_skinh > hsv[0] and l_skinh < hsv[0]:
            if hsv[0] - l_skinh < u_skinh - hsv[0]:
                l_skinh = hsv[0]
            else:
                u_skinh = hsv[0]
        if u_skins > hsv[1] and l_skins < hsv[1]:
            if hsv[1] - l_skins < u_skins - hsv[1]:
                l_skins = hsv[1]
            else:
                u_skins = hsv[1]
        if u_skinv > hsv[2] and l_skinv < hsv[2]:
            if hsv[2] - l_skinv < u_skinv - hsv[2]:
                l_skinv = hsv[2]
            else:
                u_skinv = hsv[2]
        change_TrackbarValue(l_skinh, u_skinh, l_skins, u_skins, l_skinv, u_skinv)

def execute():
    rtn = os.system(exeCode)
    os.remove('test.png')

def playsounds(filePath):
    # if way == 1: # 비동기
    winsound.PlaySound(filePath, winsound.SND_ASYNC | winsound.SND_ALIAS )
    # else: # 동기
    #     winsound.PlaySound(filePath, winsound.SND_FILENAME)
    #     winsound.PlaySound(None, winsound.SND_FILENAME)


# 비동기 -> playsounds(filePath)
# 동기 -> playsound(filePath)

cam_default = cam_num = 0
cap1 = cv2.VideoCapture(cam_default)
cap2 = cv2.VideoCapture(cam_num^1)

color_detect_rect = np.zeros(4)
prev_rect_x = 0
prev_notice = 0
frame_write_interval = 0
cam_change_interval = 0
cam_save_interval = 0
text_file_name = 'color_detection_play.txt'
exeCode = "python classify.py --model fashion.model --labelbin mlb.pickle --image test.png"
filePath = 'voice/notices/'

cv2.namedWindow('frame')
cv2.setMouseCallback('frame', mouse_callback)

playsound("{}notice.wav".format(filePath))

while True:
    try:  #an error comes if it does not find anything in window as it cannot find contour of max area
          #therefore this try error statement

        _, frame1 = cap1.read()
        _, frame2 = cap2.read()
        
        if cam_num == cam_default:
            frame = frame1
        else:
            frame = frame2
        frame = cv2.flip(frame, 1)
        raw_frame = frame.copy()
        
        if cam_num == cam_default:
            #손인식을 할 범위의 사이즈 (100,100),(400,400) 사각형의 모서리
            #roi = frame[100:400, 100:400]
            roi = frame
            
            #roi 범위 안의 색영역추출
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

            # 추출한 색영역과 비교할 범위 (살색) [색범위,채도,명암]
            l_skinh = cv2.getTrackbarPos('lower_h', 'skin_hsv')
            u_skinh = cv2.getTrackbarPos('upper_h', 'skin_hsv')
            l_skins = cv2.getTrackbarPos('lower_s', 'skin_hsv')
            u_skins = cv2.getTrackbarPos('upper_s', 'skin_hsv')
            l_skinv = cv2.getTrackbarPos('lower_v', 'skin_hsv')
            u_skinv = cv2.getTrackbarPos('upper_v', 'skin_hsv')

            lower_skin = np.array([l_skinh, l_skins, l_skinv], dtype = np.uint8)
            upper_skin = np.array([u_skinh, u_skins, u_skinv], dtype = np.uint8)

            # 추출한 색영역 hsv가 살색 범위만 남긴다. (0 or 255)
            mask = cv2.inRange(hsv, lower_skin, upper_skin)
            cv2.imshow("Skin color detection", mask)

            #cv2.GaussianBlur 중심에 있는 픽셀에 높은 가중치 = 노이즈제거 (0 ~ 255)
            mask = cv2.GaussianBlur(mask, (21,21), 0)
            mask = cv2.threshold(mask, 50, 255, cv2.THRESH_BINARY)[1]

            #외곽의 픽셀을 1(흰색)으로 채워 노이즈제거 interations -반복횟수
            kernel = np.ones((3, 3), np.uint8) 
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            
            #cv2.findContours 경계선 찾기 cv2.RETR_TREE 경계선 찾으며 계층관계 구성 cv2.CHAIN_APPROX_SIMPLE 경계선을 그릴 수 있는 point만 저장
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            #경계선 중 최대값 찾기
            cnt = max(contours, key = lambda x: cv2.contourArea(x))

            #엡실론 값에 따라 컨투어 포인트의 값을 줄인다. 각지게 만듬 Douglas-Peucker 알고리즘 이용
            epsilon = 0.0005 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            M = cv2.moments(cnt)

            #중심점
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.circle(roi, (cx, cy), 6, [255, 255, 0], -1)

            #외곽의 점을 잇는 컨벡스 홀
            hull = cv2.convexHull(cnt)
            cv2.drawContours(roi, [hull], 0, (0, 255, 0), 2)

            #컨벡스홀 면적과 외곽면적 정의
            areahull = cv2.contourArea(hull)
            areacnt = cv2.contourArea(cnt)

            #컨벡스홀-외곽면적의 비율
            arearatio = ((areahull - areacnt) / areacnt) * 100

            # 깊이의 개수
            l = 0
            notice = 0
            detect_cam_change_finger = False
            detect_pointing_finger = False
            
            if areacnt < 2000:
                #"좀 더 안쪽을 가리켜주세요" 명령 추가
                # playsounds("{}1.wav".format(filePath))
                if areacnt > 100:
                    notice = 1
                cv2.putText(frame, 'Put hand in the box', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
            else:
                #cv2.convexityDefects 컨벡스 결함
                hull = cv2.convexHull(approx, returnPoints = False)

                defects = cv2.convexityDefects(approx, hull)

                #시작점, 끝점, 결점을 정한다
                for i in range(defects.shape[0]): #defects 컨벡스 결함의 수 만큼 반복
                    s, e, f, d = defects[i, 0]
                    start = tuple(approx[s][0])
                    end = tuple(approx[e][0])
                    far = tuple(approx[f][0])

                    # end,for,start 점의 삼각형 길이
                    a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                    b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                    c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                    s = (a + b + c) / 2
                    ar = math.sqrt(s * (s - a) * (s - b) * (s - c))

                    #컨벡스 결함으로 이루어진 삼각형에서의 깊이
                    d = (2 * ar) / a

                    # 코사인 법칙을 이용한 손가락 사이 각도 **2 = ^2
                    angle = math.acos((b**2 + c**2 - a**2)/(2 * b * c)) * 57
                
                    # 각도와 깊이를 확인해 far end start 각점에 표시
                    if angle <= 90 and d > 50:
                        l += 1
                        cv2.circle(roi, far, 6, [255, 0, 0], -1)
                        cv2.circle(roi, end, 6, [255, 0, 0], 1)
                        cv2.circle(roi, start, 6, [0, 0, 255], 1)

                    #컨벡스홀 라인그리기 start-end로 각각 
                    #cv2.line(roi, start, end, [0, 255, 0], 2)

                length_from_center = np.zeros(len(approx), dtype=int)
                for i in range(len(approx)):
                    length_from_center[i] = math.sqrt((approx[i][0][0] - cx)**2 + (approx[i][0][1] - cy)**2)
                farthest_point = np.argmax(length_from_center)
                
                topmost = approx[farthest_point][0]
                color_detect_rect = [topmost[0] - 20, topmost[1] - 45, topmost[0] + 20, topmost[1] - 5]
                cv2.circle(roi, (topmost[0], topmost[1] - 2), 4, [0, 100, 100], -1)
                cv2.rectangle(roi, (color_detect_rect[0], color_detect_rect[1]), (color_detect_rect[2], color_detect_rect[3]), (0, 255, 0), 0)
                
                hand_moving = False
                if abs(prev_rect_x - color_detect_rect[2]) > 7:
                    print (abs(prev_rect_x - color_detect_rect[2]))
                    hand_moving = True
                prev_rect_x = color_detect_rect[2]
                
                roi2 = raw_frame[color_detect_rect[1]:color_detect_rect[3], color_detect_rect[0]:color_detect_rect[2]]
                rgbroi = cv2.cvtColor(roi2, cv2.COLOR_BGR2RGB)
                rgbroi = rgbroi.reshape((-1, 3))
                rgbroi = np.float32(rgbroi)
                
                #K-MEANS
                criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
                k = 2
                ret,label,center = cv2.kmeans(rgbroi,k,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
                
                center = np.uint8(center)
                res = center[label.flatten()]
                res2 = res.reshape((roi2.shape))
                px = center[0]

                #display corresponding gestures which are in their ranges
                font = cv2.FONT_HERSHEY_SIMPLEX
                if l == 0:
                    if arearatio < 12:
                        if cam_num == cam_default :
                            notice = 2
                        cv2.putText(frame, '0', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                    else:   
                        detect_pointing_finger = True
                        cv2.putText(frame, '1', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                elif l == 1:  #손가락 2개일 때 캠 전환
                    detect_cam_change_finger = True
                    cv2.putText(frame, '2', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                else :
                    notice = 5
                    # playsounds(1,"{}hatsan.wav".format(filePath)) # 손가락 두개를 펴서 저에게 보여주세요
                    cv2.putText(frame, 'reposition', (10, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)

            if detect_cam_change_finger == True:
                cam_change_interval += 1
                if cam_change_interval >= 40:
                    cam_change_interval = 0
                    cam_num ^= 1
                    print('cam_num = ',cam_num)
                    #playsounds("{}4.wav".format(filePath)) # 옷꺼내세요
                    notice = 4
                    notice_interval = 40
                    
            if hand_moving == True:
                frame_write_interval = 0
            if detect_pointing_finger == True:
                frame_write_interval += 1
                if frame_write_interval >= 20:
                    frame_write_interval = 0
                    
                    if cam_num == cam_default:
                        text_rgb = ','.join(map(str, px))
                        text_rgb += ',0,1,\n'
                        print(text_rgb)

                        file = open(text_file_name, 'w', encoding = 'utf8')
                        file.write(text_rgb)
                        file.close()
            else:
                frame_write_interval = 0
        else:
            cam_change_interval = 0
            frame_write_interval = 0
            
            print(cam_save_interval)
            cam_save_interval += 1
            if cam_save_interval >= 300:
                # 사진찍을게요
                # playsounds('voice/notices/6.wav')
                notice = 6
                notice_interval = 40
                cv2.imwrite('test.png', raw_frame)
                cam_num ^= 1
                print('cam_num = ',cam_num)
                cam_save_interval = 0
            
        if notice != prev_notice:
            notice_interval += 1
        else:
            notice_interval = 0
        if notice_interval >= 40:
            notice_interval = 0
            prev_notice = notice
            if notice > 0:
                playsounds(filePath + str(notice) + '.wav')
        
        if os.path.exists("test.png"):
            execute()

        cv2.imshow('mask', mask)
    except:
        pass
        
    cv2.imshow('frame', frame)
        
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap1.release()
cap2.release()
