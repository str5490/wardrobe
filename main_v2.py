import cv2
import numpy as np
import math

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

cap = cv2.VideoCapture(0)
#fgbg  = cv2.createBackgroundSubtractorMOG2(varThreshold=100)

frame_write_interval = 0

cv2.namedWindow('frame')
cv2.setMouseCallback('frame', mouse_callback)

background_capture = 0
exist_brackground = False
dummy_frame = True
no_act_count = 0

while(1):
    try:  #an error comes if it does not find anything in window as it cannot find contour of max area
          #therefore this try error statement

        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        if dummy_frame == True:
            dummy_frame = False
            raw_frame = frame.copy()
            continue

        frameDelta = cv2.absdiff(frame, raw_frame)
        raw_frame = frame.copy()
        gray = cv2.cvtColor(frameDelta, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (17, 17), 0)
        thresh = cv2.threshold(gray, 4, 255, cv2.THRESH_BINARY)[1]

        sum_all_bit = np.sum(thresh)
        if sum_all_bit < 50000:
            no_act_count += 1
            if no_act_count >= 10:
                no_act_count = 0
                bg_frame = raw_frame
                cv2.imshow('bg_frame', bg_frame)
                exist_brackground = True
            print (no_act_count)
        else:
            no_act_count = 0

        if exist_brackground == False:
            continue

        frameDelta = cv2.absdiff(frame, bg_frame)
        gray = cv2.cvtColor(frameDelta, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (17,17), 0)
        thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)[1]
        
        # https://webnautes.tistory.com/1257 참조
        kernel = np.ones((5,5), np.uint8) 
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        bg_sub_frame = cv2.bitwise_and(frame, frame, mask=thresh)
        
        #손인식을 할 범위의 사이즈 (100,100),(400,500) 사각형의 모서리
        #roi = frame[100:400, 100:400]
        roi = bg_sub_frame[100:400, 100:400]
        roi_drawing = frame[100:400, 100:400]
        
        #roi 사각형의 프레임을 그려준다.
        cv2.rectangle(frame, (100, 100), (400, 400), (0, 255, 0), 0)

        #roi 범위 안의 색영역추출
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # 추출한 색영역과 비교할 범위 (살색) [색범위,채도,명암]
        l_skinh=cv2.getTrackbarPos('lower_h', 'skin_hsv')
        u_skinh=cv2.getTrackbarPos('upper_h', 'skin_hsv')
        l_skins=cv2.getTrackbarPos('lower_s', 'skin_hsv')
        u_skins=cv2.getTrackbarPos('upper_s', 'skin_hsv')
        l_skinv=cv2.getTrackbarPos('lower_v', 'skin_hsv')
        u_skinv=cv2.getTrackbarPos('upper_v', 'skin_hsv')

        lower_skin = np.array([l_skinh, l_skins, l_skinv], dtype=np.uint8)
        upper_skin = np.array([u_skinh, u_skins, u_skinv], dtype=np.uint8)

        # 추출한 색영역 hsv가 살색 범위만 남긴다.
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        cv2.imshow("Skin color detection", mask)

        #외곽의 픽셀을 1(흰색)으로 채워 노이즈제거 interations -반복횟수
        kernel = np.ones((3, 3), np.uint8) 
        mask = cv2.dilate(mask, kernel, iterations = 5)

        #cv2.GaussianBlur 중심에 있는 픽셀에 높은 가중치 -노이즈제거 

        #cv2.findContours 경계선 찾기 cv2.RETR_TREE 경계선 찾으며 계층관계 구성 cv2.CHAIN_APPROX_SIMPLE 경계선을 그릴 수 있는 point만 저장
        contours,hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        #경계선 중 최대값 찾기
        cnt = max(contours, key = lambda x: cv2.contourArea(x))

        #엡실론 값에 따라 컨투어 포인트의 값을 줄인다. 각지게 만듬 Douglas-Peucker 알고리즘 이용
        epsilon = 0.0005 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt,epsilon, True)
        M = cv2.moments(cnt)
        # print(M.items())
        #외곽의 점을 잇는 컨벡스 홀
        hull = cv2.convexHull(cnt)

        #컨벡스홀 면적과 외곽면적 정의
        areahull = cv2.contourArea(hull)
        areacnt = cv2.contourArea(cnt)

        #컨벡스홀-외곽면적의 비율
        arearatio = ((areahull - areacnt) / areacnt)*100

        #cv2.convexityDefects 컨벡스 결함
        hull = cv2.convexHull(approx, returnPoints = False)
        defects = cv2.convexityDefects(approx, hull)

        # 깊이의 개수
        l = 0

        #시작점, 끝점, 결점을 정한다
        for i in range(defects.shape[0]): #defects 컨벡스 결함의 수 만큼 반복
            s, e, f, d = defects[i,0]
            start = tuple(approx[s][0])
            end = tuple(approx[e][0])
            far = tuple(approx[f][0])
            pt = (100, 180)


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
                cv2.circle(roi_drawing, far, 6, [255, 0, 0], -1)
                cv2.circle(roi_drawing, end, 6, [255, 0, 0], 1)
                cv2.circle(roi_drawing, start, 6, [0, 0, 255], 1)

            #컨벡스홀 라인그리기 start-end로 각각 
            cv2.line(roi_drawing, start, end, [0, 255, 0], 2)
        
        topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
        roi2 = raw_frame[100:400, 100:400]
        rgbroi = cv2.cvtColor(roi2, cv2.COLOR_BGR2RGB)
        px = rgbroi[topmost[1] - 2, topmost[0]]
        cv2.circle(roi_drawing, (topmost[0], topmost[1] - 2), 4, [0, 100, 100], -1)

        l += 1
        detect_pointing_finger = False
        #display corresponding gestures which are in their ranges
        font = cv2.FONT_HERSHEY_SIMPLEX
        if l == 1:
            if areacnt < 2000:
                cv2.putText(frame, 'Put hand in the box', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
            else:
                if arearatio < 10:
                    cv2.putText(frame, '0', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                else:   
                    detect_pointing_finger = True
                    cv2.putText(frame, '1', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
        else :
            cv2.putText(frame, 'reposition', (10, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)

        if detect_pointing_finger == True:
            frame_write_interval += 1
        else:
            frame_write_interval = 0

        cv2.imshow('mask', mask)
        cv2.imshow('frame', frame)
        cv2.imshow('background Subtraction', bg_sub_frame)

        #file write 추가
        if frame_write_interval == 20:
            frame_write_interval = 0
            #이미지 저장 추가
            cv2.imwrite('test.png', raw_frame[100:400, 100:400])
            text_rgb = ','.join(map(str, px))
            text_rgb += ',1,\n'
            print(text_rgb)

            file = open('test.txt', 'w', encoding = 'utf8')
            file.write(text_rgb)
            file.close()
    except:
        cv2.imshow('frame', frame)
        pass
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
