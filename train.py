# -*- coding: utf-8 -*-
"""
Created on Firday Jun 14 2019
@author: Jiwitesh Kumar
"""
import tkinter as tk
from tkinter import *
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
from RegistrationPage import RegistrationPage
import webbrowser
import random

window = tk.Tk()
#helv36 = tk.Font(family='Helvetica', size=36, weight='bold')
window.title("Face_Recogniser")

#dialog_title = 'QUIT'
#dialog_text = 'Are you sure?'
#answer = messagebox.askquestion(dialog_title, dialog_text)

# this removes the maximize button
window.resizable(0,0)
window_height = 600
window_width = 880

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
#window.geometry('880x600')
window.configure(background='#ffffff')

#window.attributes('-fullscreen', True)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

var = StringVar(window)
var.set("Faculty") # initial value

desg = tk.Label(window, text="Role :",width=10  ,fg="white"  ,bg="#17a2b8",height=1 ,font=('times', 15))
desg.place(x=80, y=200)


designation = OptionMenu(window, var, "Employee", "Faculty", "Student", "Visitor")
designation.config(width=18)
designation.config(font=27)
designation.place(x=205, y=200)


genderVar = StringVar(window)
genderVar.set("Male") # initial value

gender = tk.Label(window, text="Gender :",width=10  ,fg="white"  ,bg="#17a2b8",height=1 ,font=('times', 15))
gender.place(x=450, y=200)


genderVal = OptionMenu(window, genderVar, "Male", "Female", "Others")
genderVal.config(width=18)
genderVal.config(font=27)
genderVal.place(x=575, y=200)

#message = tk.Label(window, text="Face-Recognition Attendance" ,bg="White"  ,fg="black"  ,width=50  ,height=3,font=('times', 30, 'italic bold underline'))

#message.place(x=200, y=20)
def manipulateFont(*args):
    newFont = (font.get(), fontSize.get())
    return newFont

def clear():
    txt.delete(0, 'end')
    res = ""
    message.configure(text= res)

def clear2():
    txt2.delete(0, 'end')
    res = ""
    message.configure(text= res)


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

def TakeImages():
    Id=(idTxt.get())
    name=(stNameTxt.get())
    mobileNo=(mblNoTxt.get())
    email=(emailTxt.get())
    if(is_number(Id) and is_number(mobileNo)):
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
                cv2.imwrite("TrainingImage\ "+name +"."+Id +"."+mobileNo +"."+email +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
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
        res = "Images Saved for ID : " + Id +" Name : "+ name +" MobileNo : "+ mobileNo +" Email : "+ email
        row = [Id , name, mobileNo, email]
        with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text= res)
    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name"
            message.configure(text= res)
            if(name.isalpha()):
                res = "Enter Numeric Id"
                message.configure(text= res)

def TrainImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    #recognizer = cv2.createLBPHFaceRecognizer()
       #recognizer = cv2.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector =cv2.CascadeClassifier(harcascadePath)
    faces,Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Image Trained"#+",".join(str(f) for f in Id)
    message.configure(text= res)
    getRandomNumber()

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

"""def TrackImages():
    #recognizer = cv2.face.createLBPHFaceRecognizer()
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    #cv2.createLBPHFaceRecognizer()
    recognizer.read("TrainingImageLabel\Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);
    df=pd.read_csv("StudentDetails\StudentDetails.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names =  ['Id','Name', 'Date','Time']
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
            if(conf > 50):
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
    message2.configure(text= res)
"""
def TrackImages():
    #recognizer = cv2.face.createLBPHFaceRecognizer()
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    #cv2.createLBPHFaceRecognizer()
    recognizer.read("TrainingImageLabel\Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);    
    df=pd.read_csv("StudentDetails\StudentDetails.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX        
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
                ts = time.time()      
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                Hour,Minute,Second=timeStamp.split(":")
                fileName="Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
                attendance.to_csv(fileName,index=False)
                res=attendance
                message2.configure(text= res)
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
    message2.configure(text= res)

def close_window ():
    window.destroy()

def openRegistrationPage():
    rp = RegistrationPage()
    #RegisterUser.py

def callback(url):
    webbrowser.open_new(url)
                        
    
# create a toplevel menu
menubar = Menu(window)
menubar.add_command(label="RegisterNewUser", command=openRegistrationPage)
menubar.add_command(label="MarkYourAttendance!", command=window.quit)

# display the menu
window.config(menu=menubar)

def getRandomNumber():
    ability = str(random.randint(1,10))
    updateDisplay(ability)

def updateDisplay(myString):
	displayVariable.set(myString)

header = tk.Label(window, text="FaceRecognitionBasedAttendanceSystem",width=70  ,height=2  ,fg="white"  ,bg="#17a2b8" ,font=('times', 18, 'bold', 'underline') )
header.place(x=0, y=0)
stId = tk.Label(window, text="User ID",width=10  ,height=1  ,fg="white"  ,bg="#17a2b8" ,font=('times', 15) )
stId.place(x=80, y=80)

displayVariable = StringVar()
idTxt = tk.Entry(window,width=20 , text=displayVariable ,bg="white" ,fg="black",font=('times', 15, ' bold '))
idTxt.place(x=205, y=80)


stName = tk.Label(window, text="Name",width=10  ,fg="white"  ,bg="#17a2b8",height=1 ,font=('times', 15))
stName.place(x=450, y=80)

stNameTxt = tk.Entry(window,width=20  ,bg="white"  ,fg="black",font=('times', 15, ' bold ')  )
stNameTxt.place(x=575, y=80)

mblNo = tk.Label(window, text="Mobile No:",width=10  ,fg="white"  ,bg="#17a2b8",height=1 ,font=('times', 15))
mblNo.place(x=80, y=140)
    
mblNoTxt = tk.Entry(window,width=20  ,bg="white"  ,fg="black",font=('times', 15, ' bold ')  )
mblNoTxt.place(x=205, y=140)
    
emailId = tk.Label(window, text="Email ID :",width=10  ,fg="white"  ,bg="#17a2b8",height=1 ,font=('times', 15))
emailId.place(x=450, y=140)
    
emailTxt = tk.Entry(window,width=20  ,bg="white"  ,fg="black",font=('times', 15, ' bold ')  )
emailTxt.place(x=575, y=140)


lbl3 = tk.Label(window, text="Notification : ",width=10  ,fg="white"  ,bg="#17a2b8"  ,height=1 ,font=('times', 15, 'underline '))
lbl3.place(x=80, y=260)

message = tk.Label(window, text="" ,bg="#bbc7d4"  ,fg="black"  ,width=52  ,height=1, activebackground = "#bbc7d4" ,font=('times', 15))
message.place(x=205, y=260)

lbl3 = tk.Label(window, text="Attendance : ",width=10  ,fg="white"  ,bg="#17a2b8"  ,height=2 ,font=('times', 15, 'underline'))
lbl3.place(x=80, y=440)

message2 = tk.Label(window, text="" ,fg="#e47911"   ,bg="#bbc7d4",activeforeground = "#f8f9fa",width=52  ,height=2  ,font=('times', 15))
message2.place(x=205, y=440)


takeImg = tk.Button(window, text="Take Images", command=TakeImages  ,fg="white"  ,bg="#17a2b8"  ,width=15  ,height=1, activebackground = "#118ce1" ,font=('times', 15, ' bold '))
takeImg.place(x=80, y=350)
trainImg = tk.Button(window, text="Train Images", command=TrainImages  ,fg="white"  ,bg="#17a2b8"  ,width=15  ,height=1, activebackground = "#118ce1" ,font=('times', 15, ' bold '))
trainImg.place(x=333, y=350)

trackImg = tk.Button(window, text="Mark Attendance", command=TrackImages  ,fg="white"  ,bg="#17a2b8"  ,width=15  ,height=1, activebackground = "#118ce1" ,font=('times', 15, ' bold '))
trackImg.place(x=580, y=350)


quitWindow = tk.Button(window, text="Quit", command=close_window  ,fg="white"  ,bg="#17a2b8"  ,width=10  ,height=1, activebackground = "#118ce1" ,font=('times', 15, ' bold '))
quitWindow.place(x=650, y=510)

link2 = tk.Label(window, text="Copyright © 2019, Ineuron.ai", fg="blue", )
link2.place(x=720, y=580)
#link2.pack()
link2.bind("<Button-1>", lambda e: callback("http://ineuron.ai"))
label = tk.Label(window)  



window.mainloop()

