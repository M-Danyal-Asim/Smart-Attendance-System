import cv2
import numpy as np
import face_recognition
import dlib
from datetime import datetime
import os
import pandas
from tkinter import *

path = 'Image Attendance'
images = []
classNames = []
myList = os.listdir(path)
for cl in myList:
    current_image = cv2.imread(f'{path}/{cl}')
    images.append(current_image)
    classNames.append(os.path.splitext(cl)[0])
#print(myList)
#print(classNames)

def FindEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for lines in myDataList:
            entry  = lines.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')
        print(myDataList)



encodeListKnown = FindEncodings(images)
#print('Encoding Complete')

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        # widget can take all window
        self.pack(fill=BOTH, expand=1)

        # create the buttons
        clickButton = Button(self, text="Open the WebCam", command=self.clickButton, bg = "SteelBlue1")
        clickButton_1 = Button(self, text="Check Attendance", command=self.clickButton_1, bg = "Steelblue1")

        # place button
        clickButton.place(x=95, y=95)
        clickButton_1.place(x=95,y=150)

    def clickButton(self):
        cap = cv2.VideoCapture(0)
        while True:
            success, img = cap.read()
            imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

            facesCurrentFrame = face_recognition.face_locations(imgSmall)
            encodeCurrentFrame = face_recognition.face_encodings(imgSmall, facesCurrentFrame)

            for encodeFace, faceLoc in zip(encodeCurrentFrame, facesCurrentFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDistance = face_recognition.face_distance(encodeListKnown, encodeFace)
                print(faceDistance)
                matchIndex = np.argmin(faceDistance)

                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                    print(name)
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 0)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    markAttendance(name)

            cv2.imshow('Webcam', img)
            if cv2.waitKey(1) == ord('q'):
                break
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

    def clickButton_1(self):
        attendance = pandas.read_csv('Attendance.csv')
        print(attendance)


root = Tk()
app = Window(root)
root.wm_title("Smart Attendance System")
root.geometry("300x300")
app.configure(bg='gainsboro')
root.mainloop()
