from hand import hand
import cv2
import handtrackingModule as htm
from djitellopy import tello
import time

class drone(hand):

    detector = ""
    img = ""
    unlockCounter = False
    me = tello.Tello()
    rv = 0
    uv = 0
    fv = 0
    runtime = 0

    def run(self):

        self.me.connect()
        print(self.me.get_battery())
        self.me.streamon()
        self.detector = htm.handDetector()
        print("battery = ",self.me.get_battery(),"%")

        while True:
            self.img = self.me.get_frame_read().frame
            self.img = self.detector.findHands(self.img)
            self.img = cv2.resize(self.img, (360, 240))
            self.lmList = self.detector.findPosition(self.img, draw = False)

            self.fingernumber()
            if self.unlockCounter == False:
                if self.unlock():
                    self.me.takeoff()
                    self.unlockCounter = True
            elif self.unlockCounter == True:
                try:
                    direction = self.gesture()
                    if direction == "down":
                        self.uv = -40
                        self.rv = 0
                        self.fv = 0
                    elif direction == "up":
                        self.uv = 40
                        self.rv = 0
                        self.fv = 0
                    elif direction == "left":
                        self.rv = -40
                        self.uv = 0
                        self.fv = 0
                    elif direction == "right":
                        self.rv = 40
                        self.uv = 0
                        self.fv = 0
                    elif direction == "fbstop":
                        self.fv = 0
                    elif direction == "backward":
                        self.fv = -40
                        self.uv = 0
                        self.rv = 0
                    elif direction == "forward":
                        self.fv = 40
                        self.uv = 0
                        self.rv = 0
                    elif direction == "":
                        self.uv = 0
                        self.rv = 0
                        self.fv = 0
                except:
                    pass

                if self.off():
                    self.me.land()
                    self.unlockCounter = False
                    self.sameindex = []

                self.me.send_rc_control(self.rv,self.fv,self.uv,0)
                print("gesture = ", self.gestures)
            print("unlock = ", self.unlockCounter)


            cv2.rectangle(self.img, (0, 360), (60, 300), (0, 255, 0), cv2.FILLED)
            cv2.putText(self.img, str(self.totalfingers), (30, 30), cv2.FONT_HERSHEY_PLAIN,
                            1, (255, 0, 0), 2)
            cv2.putText(self.img, self.gestures, (30, 200), cv2.FONT_HERSHEY_PLAIN,
                            1, (255, 0, 0), 2)
            if self.unlockCounter == True:
                cv2.putText(self.img, "unlock", (290, 200), cv2.FONT_HERSHEY_PLAIN,
                                1, (255, 0, 0), 2)
            cv2.imshow("Image", self.img)
            cv2.waitKey(1)

            print("rv = {}, fv = {}, uv = {}".format(self.rv, self.fv, self.uv))

            self.runtime += 1
            if self.runtime %4 == 0:
                self.gestures=""
            time.sleep(0.03)
