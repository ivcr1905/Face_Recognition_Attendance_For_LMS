from flask import Flask, render_template, request, redirect, url_for, session,send_file
app = Flask(__name__)
# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'
@app.route('/nived/', methods=['GET', 'POST'])
@app.route('/nived/attendance')
def attendance():
    import tkinter as tk
    import csv
    import cv2
    import os
    import numpy as np
    from PIL import Image
    import pandas as pd
    import datetime
    import time

    window = tk.Tk()
    window.title("PYTHON MINIPROJECT")
    window.geometry('800x500')

    dialog_title = 'QUIT'
    dialog_text = "are you sure?"
    window.configure(background='grey')
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    def trackImage():
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("Trainner.yml")
        harcascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath)
        df = pd.read_csv("studentDetailss.csv")
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        cam = cv2.VideoCapture(0)
        # create a dataframe to hold the student id,name,date and time
        col_names = {'Id', 'Name', 'Date', 'Time'}
        attendance = pd.DataFrame(columns=col_names)
        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.1, 3)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                #  a confidence less than 50 indicates a good face recognition
                if conf < 60:
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M')
                    aa = df.loc[df['ID'] == Id]['NAME'].values
                    tt = str(Id) + "-" + aa
                    attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
                    row2 = [Id, aa, date, timeStamp]
                    #   open the attendance file for update
                    with open("AttendanceFile.csv", 'a+') as csvFile2:
                        writer2 = csv.writer(csvFile2)
                        writer2.writerow(row2)
                    csvFile2.close()
                    # print attendance updated on the notification board of the GUI
                    res = 'ATTENDANCE UPDATED WITH DETAILS'
                    label4.configure(text=res)

                else:
                    Id = 'Unknown'
                    tt = str(Id)
                    #  store the unknown images in the images unknown folder
                    if conf > 65:
                        noOfFile = len(os.listdir("ImagesUnknown")) + 1
                        cv2.imwrite("ImagesUnknown\Image" + str(noOfFile) + ".jpg", img[y:y + h, x:x + w])
                        res = 'ID UNKNOWN, ATTENDANCE NOT UPDATED'
                        label4.configure(text=res)
                attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
                cv2.putText(img, str(tt), (x, y + h - 10), font, 0.8, (255, 255, 255), 1)
                cv2.imshow('FACE RECOGNIZER', img)
            if cv2.waitKey(1000) == ord('q'):
                break

            cam.release()
            cv2.destroyAllWindows()
    label3 = tk.Label(window, background="grey", fg="blue", text="Notification", width=10, height=1,
                    font=('sans-serif', 20, 'underline'))
    label3.place(x=315, y=155)
    label4 = tk.Label(window, background="white", fg="black", width=55, height=4, font=('Calibri', 14, 'italic'))
    label4.place(x=111, y=205)
    trackImageBtn = tk.Button(window, command=trackImage, background="white", fg="black", text="TRACK IMAGE", width=12,
                            activebackground="blue", height=3, font=('sans-serif', 12))
    trackImageBtn.place(x=345, y=360)

    window.mainloop()
    return "PRESS BACK TO CONTINUE"

if __name__ == '__main__':
    app.debug = True
    app.run()