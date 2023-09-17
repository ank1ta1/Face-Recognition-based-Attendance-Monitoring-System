import os
import pickle
import cv2
import face_recognition
import firebase_admin
import numpy as np
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facerecattendance-1a20c-default-rtdb.firebaseio.com/",
    'storageBucket': "facerecattendance-1a20c.appspot.com"
})

bucket = storage.bucket()


capt = cv2.VideoCapture(0)
capt.set(3, 640)
capt.set(4, 480)

imgBackground = cv2.imread('Resources/background1.png')

folderModePath = 'Resources/Modes'
modePath = os.listdir(folderModePath)
imgModeList = []
for path in modePath:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))

# load the encoding file
print("Loading encode file...")

file = open('EncodeFile.p', 'rb')
encodeListKnownwithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownwithIds
# print(studentIds)
print("Encode file loaded")

modetype = 3
counter = 0
id = -1
imgStudent = []

while True:
    success, img = capt.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurrFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    # adding webcam window to the background
    imgBackground[162:162+480, 55:55+640] = img
    # adding modes to the background
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modetype]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurrFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("matches", matches)
            # print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)
            # print("Match Index", matchIndex)

            if matches[matchIndex]:
                # print("Known Face Detected")
                # print(studentIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                imgBackground = cv2.rectangle(imgBackground, (x1+55, y1+162), (x2+55, y2+162), (255, 0, 0), 2)
                id = studentIds[matchIndex]
                if counter == 0:
                    counter = 1
                    modetype = 1

                if counter != 0:
                    if counter == 1:
                        # fetch data
                        studentInfo = db.reference(f'Students/{id}').get()
                        print(studentInfo)
                        # fetch student img
                        iblob = bucket.blob(f'images/{id}.png')
                        array = np.frombuffer(iblob.download_as_string(), np.uint8)
                        imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                        # update attendance

                        datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                          "%Y-%m-%d %H:%M:%S")
                        secondsElapsed = (datetime.now()-datetimeObject).total_seconds()
                        print(secondsElapsed)
                        if secondsElapsed > 30:
                            ref = db.reference(f'Students/{id}')
                            studentInfo['total_attendance'] += 1
                            # print(studentInfo)
                            ref.child('total_attendance').set(studentInfo['total_attendance'])
                            ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        else:
                            modetype = 0
                            counter = 0
                            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modetype]

                    if modetype != 0:
                        if 15 < counter <28:
                            modetype = 2

                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modetype]

                        if counter <= 15:
                            cv2.putText(imgBackground, str(studentInfo['total_attendance']),(861,125),
                                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                            cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                            cv2.putText(imgBackground, id, (1006, 493),
                                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                            cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                            cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                            cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                            (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                            offset = (414-w)//2
                            cv2.putText(imgBackground, str(studentInfo['name']), (808+offset, 445),
                                        cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
                            imgBackground[175:175+216, 909:909+216] = imgStudent

                        counter += 1

                        if counter>=28:
                            counter = 0
                            modetype = 3
                            studentInfo = []
                            imgStudent = []
                            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modetype]


    else:
        modetype = 3
        counter = 0

    # cv2.imshow("Webcam", img)
    cv2.imshow("bg", imgBackground)
    cv2.waitKey(1)