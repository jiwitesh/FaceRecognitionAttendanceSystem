# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 05:15:34 2019

@author: Jiwitesh
"""
import tkinter as tk
from tkinter import Message ,Text
import cv2
import os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
import RegistrationPage

class MainScreen():

    def __init__(self):
        self.window=tk.Tk()
        self.window.title("RegistrationPage")
        self.window.resizable(0,0)
        self.window.geometry('680x500')
        self.window.configure(background='#232f3e')

        #helv36 = tk.Font(family='Helvetica', size=36, weight='bold')
        #dialog_title = 'QUIT'
        #dialog_text = 'Are you sure?'
        #answer = messagebox.askquestion(dialog_title, dialog_text)

        # this removes the maximize button

        #window.attributes('-fullscreen', True)

        #self.window.grid_rowconfigure(0, weight=1)
        #self.window.grid_columnconfigure(0, weight=1)

        txt = tk.Entry(self.window,width=10  ,bg="white" ,fg="black",font=('times', 15, ' bold '))
        txt.place(x=220, y=90)

        txt2 = tk.Entry(self.window,width=10  ,bg="white"  ,fg="black",font=('times', 15, ' bold ')  )
        txt2.place(x=220, y=155)

        lbl3 = tk.Label(self.window, text="Notification : ",width=10  ,fg="white"  ,bg="#e47911"  ,height=2 ,font=('times', 15, 'underline '))
        lbl3.place(x=80, y=210)

        self.message = tk.Label(self.window, text="" ,bg="white"  ,fg="black"  ,width=30  ,height=1, activebackground = "#e47911" ,font=('times', 15))
        self.message.place(x=220, y=220)

        lbl3 = tk.Label(self.window, text="Attendance : ",width=10  ,fg="white"  ,bg="#e47911"  ,height=2 ,font=('times', 15, 'underline'))
        lbl3.place(x=80, y=400)

        message2 = tk.Label(self.window, text="" ,fg="#e47911"   ,bg="white",activeforeground = "green",width=30  ,height=1  ,font=('times', 15))
        message2.place(x=220, y=405)

        clearButton = tk.Button(self.window, text="Clear", command=self.clear  ,fg="white"  ,bg="#e47911"  ,width=8  ,height=1 ,activebackground = "#118ce1" ,font=('times', 15, ' bold '))
        clearButton.place(x=350, y=80)
        clearButton2 = tk.Button(self.window, text="Clear", command=self.clear2  ,fg="white"  ,bg="#e47911"  ,width=8  ,height=1, activebackground = "#118ce1" ,font=('times', 15, ' bold '))
        clearButton2.place(x=350, y=150)
        takeImg = tk.Button(self.window, text="Take Images", command=self.TakeImages  ,fg="white"  ,bg="#e47911"  ,width=10  ,height=1, activebackground = "#118ce1" ,font=('times', 15, ' bold '))
        takeImg.place(x=80, y=300)
        trainImg = tk.Button(self.window, text="Train Images", command=self.TrainImages  ,fg="white"  ,bg="#e47911"  ,width=10  ,height=1, activebackground = "#118ce1" ,font=('times', 15, ' bold '))
        trainImg.place(x=220, y=300)
        trackImg = tk.Button(self.window, text="Track Images", command=self.TrackImages  ,fg="white"  ,bg="#e47911"  ,width=10  ,height=1, activebackground = "#118ce1" ,font=('times', 15, ' bold '))
        trackImg.place(x=360, y=300)
        #quitWindow = tk.Button(window, text="Quit", command=close_window  ,fg="white"  ,bg="#e47911"  ,width=10  ,height=1, activebackground = "#118ce1" ,font=('times', 15, ' bold '))
        #quitWindow.place(x=500, y=300)


        registration = tk.Button(self.window, text="Register", command=self.openRegWin  ,fg="white"  ,bg="#e47911"  ,width=10  ,height=1, activebackground = "#118ce1" ,font=('times', 15, ' bold '))
        registration.place(x=550, y=30)

        deactivate = tk.Button(self.window, text="DeActivate", command=self.close_window  ,fg="white"  ,bg="#e47911"  ,width=10  ,height=1, activebackground = "#118ce1" ,font=('times', 15, ' bold '))
        deactivate.place(x=550, y=380)

        quitWindow = tk.Button(self.window, text="Quit", command=self.close_window  ,fg="white"  ,bg="#e47911"  ,width=10  ,height=1, activebackground = "#118ce1" ,font=('times', 15, ' bold '))
        quitWindow.place(x=500, y=300)

        self.window.mainloop()

    #message = tk.Label(window, text="Face-Recognition Attendance" ,bg="White"  ,fg="black"  ,width=50  ,height=3,font=('times', 30, 'italic bold underline'))

    #message.place(x=200, y=20)

    def openRegWin(self):
        RegistrationPage.openRegWindow()
    def clear(self):
        self.txt.delete(0, 'end')
        res = ""
        self.message.configure(text= res)

    def clear2(self):
        self.txt2.delete(0, 'end')
        res = ""
        self.message.configure(text= res)


    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False

    def TakeImages(self):
        Id=(self.txt.get())
        name=(self.txt2.get())
        if(self.is_number(Id) and name.isalpha()):
            cam = cv2.VideoCapture(0)
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector=cv2.CascadeClassifier(harcascadePath)
            sampleNum=0
            while(True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in faces:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                    #incrementing sample number
                    sampleNum=sampleNum+1
                    #saving the captured face in the dataset folder TrainingImage
                    cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                    #display the frame
                    cv2.imshow('frame',img)
                #wait for 100 miliseconds
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum>60:
                    break
            cam.release()
            cv2.destroyAllWindows()
            res = "Images Saved for ID : " + Id +" Name : "+ name
            row = [Id , name]
            with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            self.message.configure(text= res)
        else:
            if(self.is_number(Id)):
                res = "Enter Alphabetical Name"
                self.message.configure(text= res)
            if(name.isalpha()):
                res = "Enter Numeric Id"
                self.message.configure(text= res)

    def TrainImages(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        #recognizer = cv2.createLBPHFaceRecognizer()
        #recognizer = cv2.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        faces,Id = self.getImagesAndLabels("TrainingImage")
        recognizer.train(faces, np.array(Id))
        recognizer.save("TrainingImageLabel\Trainner.yml")
        res = "Image Trained"#+",".join(str(f) for f in Id)
        self.message.configure(text= res)

    def getImagesAndLabels(path):
        #get the path of all the files in the folder
        imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
        #print(imagePaths)

        #create empth face list
        faces=[]
        #create empty ID list
        Ids=[]
        #now looping through all the image paths and loading the Ids and the images
        for imagePath in imagePaths:
            #loading the image and converting it to gray scale
            pilImage=Image.open(imagePath).convert('L')
            #Now we are converting the PIL image into numpy array
            imageNp=np.array(pilImage,'uint8')
            #getting the Id from the image
            Id=int(os.path.split(imagePath)[-1].split(".")[1])
            # extract the face from the training image sample
            faces.append(imageNp)
            Ids.append(Id)
        return faces,Ids

    def TrackImages(self):
        #recognizer = cv2.face.createLBPHFaceRecognizer()
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        #cv2.createLBPHFaceRecognizer()
        recognizer.read("TrainingImageLabel\Trainner.yml")
        harcascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath);
        df=pd.read_csv("StudentDetails\StudentDetails.csv")
        cam = cv2.VideoCapture(0)
        #font = cv2.FONT_HERSHEY_SIMPLEX
        col_names =  ['Id','Name','Date','Time']
        attendance = pd.DataFrame(columns = col_names)
        while True:
            ret, im =cam.read()
            gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            faces=faceCascade.detectMultiScale(gray, 1.2,5)
            for(x,y,w,h) in faces:
                cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
                Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
                if(conf < 50):
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa=df.loc[df['Id'] == Id]['Name'].values
                    tt=str(Id)+"-"+aa
                    attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]

                else:
                    Id='Unknown'
                    tt=str(Id)
                if(conf > 75):
                    noOfFile=len(os.listdir("ImagesUnknown"))+1
                    cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])
                cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)
            attendance=attendance.drop_duplicates(subset=['Id'],keep='first')
            cv2.imshow('im',im)
            if (cv2.waitKey(1)==ord('q')):
                break
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour,Minute,Second=timeStamp.split(":")
        fileName="Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
        attendance.to_csv(fileName,index=False)
        cam.release()
        cv2.destroyAllWindows()
        #print(attendance)
        res=attendance
        self.message2.configure(text= res)


    def close_window (self):
        self.window.destroy()

screen = MainScreen()

#window.quit()