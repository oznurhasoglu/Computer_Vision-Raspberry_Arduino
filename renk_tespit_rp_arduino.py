#--coding:utf-8-- 
import cv2
import numpy as np
import time
import RPi.GPIO as GPIO
import serial

arduino=serial.Serial('/dev/ttyUSB0',9600)
time.sleep(2)

alt_sınır= np.array([20,100,100])
üst_sınır= np.array([30,255,255])

cap = cv2.VideoCapture(0)

fps_start_time=0
fps=0
alan=2000

while True:
    ret, frame = cap.read()
    #frame=cv2.resize(frame, (640,480))
    fps_end_time= time.time()
    time_diff= fps_end_time - fps_start_time
    fps= 1/(time_diff)
    fps_start_time= fps_end_time
    fps_text= "FPS: {:.2f}".format(fps)
    frame= cv2.flip(frame,1)
    #frame=cv2.bilateralFilter(frame,9,250,250)
    
    hsv_frame= cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    sari_maskeleme= cv2.inRange(hsv_frame, alt_sınır, üst_sınır)
    sari_maskleme= cv2.erode(sari_maskeleme,None,iterations=2)
    sari_maskleme= cv2.dilate(sari_maskleme,None,iterations=2)
    yellow= cv2.bitwise_and(frame,frame,mask= sari_maskeleme)
    
    kontur,_ = cv2.findContours(sari_maskeleme,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    if len(kontur) > 0 :
        maxkontur = max(kontur,key=cv2.contourArea)
        if int(cv2.contourArea(maxkontur)) > alan:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(27, GPIO.OUT)
            GPIO.output(27, GPIO.HIGH)
            GPIO.cleanup()
            i = 0
            dortgen = cv2.minAreaRect(maxkontur)
            kutu = cv2.boxPoints(dortgen)
            kutu = np.int64(kutu)
            sol_ust = kutu[2];sol_alt = kutu[1];sag_ust= kutu[3];sag_alt= kutu[0]
            if abs(kutu[0][0] - kutu[1][0]) < abs(kutu[2][1] - kutu[1][1]):
                sag_alt= kutu[0];sol_alt = kutu[1];sol_ust = kutu[2];sag_ust= kutu[3]
            if abs(kutu[2][1] - kutu[1][1]) < abs(kutu[0][0] - kutu[1][0]):
                sag_alt = kutu[1];sol_alt= kutu[2];sol_ust= kutu[3];sag_ust= kutu[0]
            if abs(kutu[3][0] - kutu[2][0]) < abs(kutu[2][1] - kutu[1][1]):
                sag_alt= kutu[2];sol_alt = kutu[3];sol_ust= kutu[0];sag_ust = kutu[1]
            cv2.drawContours(frame,[kutu],0,(255,0,0),1)
            m= cv2.moments(kutu)
            print(m)

            x = int(m["m10"] / m["m00"])
            y = int(m["m01"] / m["m00"])
            cv2.circle(frame, (x, y), 5, (255, 255, 255), -1)
            cv2.putText(frame, "merkez", (x - 25, y - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        if int(cv2.contourArea(maxkontur)) > alan:
          arduino.write('1'.encode('utf-8'))
          print("led yandı")
        else:
          arduino.write('0'.encode('utf-8'))
          print("led söndü")
    cv2.putText(frame, fps_text, (5,30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,255),1)
    cv2.imshow("Kamera", frame)
    cv2.imshow("Sari Maskeleme", sari_maskeleme)
    k = cv2.waitKey(1)
    if k != -1 or 0xFF ==ord("q"):
        break
cap.release()
cv2.destroyAllWindows()