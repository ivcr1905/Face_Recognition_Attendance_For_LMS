from flask import Flask, render_template, request, redirect, url_for, session,send_file
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'secret'
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)
# http://localhost:8000/nived/ - the following will be our login page, which will use both GET and POST requests

@app.route('/nived/', methods=['GET', 'POST'])

def login():
    # Output message if something goes wrong...
    msg = ''
    
        # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
            # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
                # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg=msg)
# http://localhost:5000/python/logout - this will be the logout page
@app.route('/nived/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/nived/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)   
# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/nived/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
        
    # User is not loggedin redirect to login page
    
        
    return redirect(url_for('login'))
# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/nived/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

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


    def clear():
        std_name.delete(0, 'end')
        res = ""
        label4.configure(text=res)


    def clear2():
        std_number.delete(0, 'end')
        res = ""
        label4.configure(text=res)


    def takeImage():
        name = (std_name.get())
        Id = (std_number.get())
        if name.isalpha():
            cam = cv2.VideoCapture(0)
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
            sampleNum = 0

            while True:
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.1, 3)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    sampleNum = sampleNum + 1
                    # store each student picture with its name and id
                    cv2.imwrite("TrainingImages\ " + name + "." + Id + '.' + str(sampleNum) + ".jpg",
                                gray[y:y + h, x:x + h])
                    cv2.imshow('FACE RECOGNIZER', img)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # stop the camera when the number of picture exceed 50 pictures for each student
                if sampleNum > 50:
                    break

            cam.release()
            cv2.destroyAllWindows()
            # print the student name and id after a successful face capturing
            res = 'Student details saved with: \n Roll number : ' + Id + ' and  Full Name: ' + name

            row = [Id, name]

            with open('studentDetailss.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            label4.configure(text=res)
        else:

            if name.isalpha():
                res = "Enter correct roll number"
                label4.configure(text=res)


    def getImagesAndLabels(path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faces = []
        Ids = []
        for imagePath in imagePaths:
            pilImage = Image.open(imagePath).convert('L')
            imageNp = np.array(pilImage, 'uint8')
            Id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces.append(imageNp)
            Ids.append(Id)
        return faces, Ids


    def trainImage():
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        faces, Id = getImagesAndLabels("TrainingImages")
        recognizer.train(faces, np.array(Id))
        recognizer.save("Trainner.yml")
        res = "Image Trained"
        label4.configure(text=res)


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
                    with open('AttendanceFile.csv', 'a+') as csvFile2:
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
                # To avoid duplication in the attendance file.
                attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
                # show the student id and name
                cv2.putText(img, str(tt), (x, y + h - 10), font, 0.8, (255, 255, 255), 1)
                cv2.imshow('FACE RECOGNIZER', img)
            if cv2.waitKey(1000) == ord('q'):
                break

            cam.release()
            cv2.destroyAllWindows()


    label1 = tk.Label(window, background="grey", fg="black", text="Name :", width=10, height=1,
                    font=('sans-serif', 16))
    label1.place(x=83, y=40)
    std_name = tk.Entry(window, background="white", fg="black", width=25, font=('Calibri', 14))
    std_name.place(x=280, y=41)
    label2 = tk.Label(window, background="grey", fg="black", text="Roll Number :", width=14, height=1,
                    font=('sans-serif', 16))
    label2.place(x=100, y=90)
    std_number = tk.Entry(window, background="white", fg="black", width=25, font=('sans-serif', 14))
    std_number.place(x=280, y=91)

    clearBtn1 = tk.Button(window, background="BLUE", command=clear, fg="white", text="CLEAR", width=8, height=1,
                        activebackground="red", font=('sans-serif', 10))
    clearBtn1.place(x=580, y=42)
    clearBtn2 = tk.Button(window, background="BLUE", command=clear2, fg="white", text="CLEAR", width=8,
                        activebackground="red", height=1, font=('sans-serif', 10))
    clearBtn2.place(x=580, y=92)

    label3 = tk.Label(window, background="grey", fg="blue", text="Notification", width=10, height=1,
                    font=('sans-serif', 20, 'underline'))
    label3.place(x=320, y=155)
    label4 = tk.Label(window, background="white", fg="black", width=55, height=4, font=('Calibri', 14, 'italic'))
    label4.place(x=95, y=205)

    takeImageBtn = tk.Button(window, command=takeImage, background="white", fg="black", text="CAPTURE IMAGE",
                            activebackground="blue",
                            width=15, height=3, font=('sans-serif', 12))
    takeImageBtn.place(x=130, y=360)
    trainImageBtn = tk.Button(window, command=trainImage, background="white", fg="black", text="TRAINED IMAGE",
                            activebackground="blue",
                            width=15, height=3, font=('sans-serif', 12))
    trainImageBtn.place(x=340, y=360)
    trackImageBtn = tk.Button(window, command=trackImage, background="white", fg="black", text="TRACK IMAGE", width=12,
                            activebackground="blue", height=3, font=('sans-serif', 12))
    trackImageBtn.place(x=550, y=360)

    window.mainloop()

    return "PRESS BACK TO CONTINUE"


@app.route('/nived/attendancesheet')
def attendancesheet():
    import pandas as pd
    

    pd.options.display.max_rows = 9999

    df = pd.read_csv('AttendanceFile.csv')
    length = len(df)
    id=df['ID']
    name=df['NAME']
    date=df['DATE']
    time=df['TIME']
    return render_template("attendancesheet.html",id=id,name=name,date=date,time=time,length=length
    )
@app.route('/nived/studentdetails')
def studentdetails():
    import pandas as pd
    pd.options.display.max_rows=9999

    df=pd.read_csv('studentDetailss.csv')
    length=len(df)
    id=df['ID']
    name=df['NAME']

    return render_template("studentdetails.html",id=id,name=name,length=length)


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1',port=8000)