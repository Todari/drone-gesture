import math

class hand():

    tipIds = [4, 8, 12, 16, 20]
    unlockindex = []
    lmList = []
    fingers = []
    totalfingers = 0
    unlockTF = False
    angle = 0
    gestures = ""
    sameindex=[]
    distance = 0


    def fingernumber(self):
        if len(self.lmList) != 0:
            self.fingers = []

            if self.lmList[5][1] > self.lmList[17][1]:
                if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0]-1][1]:
                    self.fingers.append(1)
            if self.lmList[5][1] < self.lmList[17][1]:
                if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0]-1][1]:
                    self.fingers.append(1)

            for id in range(1,5):
                if self.lmList[0][2] > self.lmList[9][2]:
                    if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2]:
                        self.fingers.append(1)
                if self.lmList[0][2] < self.lmList[9][2]:
                    if self.lmList[self.tipIds[id]][2] > self.lmList[self.tipIds[id]-2][2]:
                        self.fingers.append(1)


            self.totalfingers = len(self.fingers)
            print("fingers = ", self.totalfingers)


    def unlock(self):
        if len(self.unlockindex) >= 5:
            self.unlockindex = []
        if self.totalfingers not in self.unlockindex:
            self.unlockindex.append(self.totalfingers)
            if len(self.unlockindex) > 1:
                if self.unlockindex[1] != self.unlockindex[0] + 1:
                    self.unlockindex[0] = self.unlockindex[1]
                    del(self.unlockindex[1])
                if len(self.unlockindex) > 2:
                    if self.unlockindex[2] != self.unlockindex[1] + 1:
                        self.unlockindex[0] = self.unlockindex[2]
                        del(self.unlockindex[2])
                        del(self.unlockindex[1])
                    if len(self.unlockindex) > 3:
                        if self.unlockindex[3] != self.unlockindex[2] + 1:
                            self.unlockindex[0] = self.unlockindex[3]
                            del (self.unlockindex[3])
                            del (self.unlockindex[2])
                            del (self.unlockindex[1])
                        else:
                            self.unlockTF = True
                            print("잠금해제")
                            self.unlockindex = []
                            print(self.unlockindex)
                            return True
        self.unlockTF = False
        print("잠금해제 해 주세요")
        print("unlockindex = ",self.unlockindex)
        return False

    def off(self):
        if len(self.lmList) != 0:
            if len(self.sameindex)==0:
                self.sameindex.append(0)
            if (self.sameindex[0] == 0) and (self.lmList[9][1] > 0):
                self.sameindex.append(self.totalfingers)
            if len(self.sameindex) > 1:
                if self.sameindex[-1] != self.sameindex[-2]:
                    self.sameindex = []
                if len(self.sameindex) >= 50:
                    print("종료합니다")
                    return True
        print("offindex",len(self.sameindex))


    def gesture(self):
        if len(self.lmList) != 0:
            tany = self.lmList[9][1] - self.lmList[0][1]
            if tany == 0:
                tany = 0.1
                self.angle = math.degrees(math.atan((self.lmList[0][2] - self.lmList[9][2])/tany))
            else:
                self.angle = math.degrees(math.atan((self.lmList[0][2] - self.lmList[9][2]) / tany))

            if (self.lmList[9][2] > self.lmList[0][2]) and (-45 > self.angle or 45 < self.angle):  # 손가락이 아래
                if (self.lmList[8][2] > self.lmList[6][2]) and (self.lmList[12][2] < self.lmList[10][2]) and (
                        self.lmList[16][2] < self.lmList[14][2]):
                    self.gestures = "down"
                    return "down"

            elif (self.lmList[9][2] < self.lmList[0][2]) and (-45 > self.angle or 45 < self.angle):  # 손가락이 위
                if (self.lmList[8][2] < self.lmList[6][2]) and (self.lmList[12][2] > self.lmList[10][2]) and (
                        self.lmList[16][2] > self.lmList[14][2]):
                    self.gestures = "up"
                    return "up"

            elif (self.lmList[9][1] < self.lmList[0][1]) and (-45 < self.angle < 45):  # 왼쪽으로 기움
                if (self.lmList[8][1] < self.lmList[6][1]) and (self.lmList[12][1] > self.lmList[10][1]):
                    self.gestures = "left"
                    return "left"

            elif (self.lmList[9][1] > self.lmList[0][1]) and (-45 < self.angle < 45):  # 왼쪽오른쪽
                if (self.lmList[8][1] > self.lmList[6][1]) and (self.lmList[12][1] < self.lmList[10][1]) and (
                        self.lmList[16][2] < self.lmList[14][1]):
                    self.gestures = "right"
                    return "right"

            self.distance = ((self.lmList[1][1] - self.lmList[17][1])**2 + (self.lmList[1][2] - self.lmList[17][2])**2)**0.5
            print(self.distance)
            if (self.distance < 30) and self.gestures=="":
                self.gestures = "forward"
                #print(self.gestures)
                return "forward"
            elif (self.distance > 100) and self.gestures=="":
                self.gestures = "backward"
                return "backward"
            elif (30< self.distance < 100) and self.gestures=="":
                return "fbstop"
        else:
            self.gestures = ""
            return ""





