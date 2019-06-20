# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 09:32:53 2019

@author: Jiwitesh
"""

import sys
if sys.version_info[0] < 3:
    import Tkinter as tk     ## Python 2.x
else:
    import tkinter as tk     ## Python 3.x
import cv2
from OCRModule import readIdText, pan_number, personName
import OCRModule
import csv

class RegistrationPage():
   def __init__(self):
        self.window=tk.Tk()
        self.window.title("RegistrationPage")
        self.window.resizable(0,0)
        self.window.geometry('680x500')
        self.window.configure(background='#232f3e')


        lbl = tk.Label(self.window, text="ID Number",width=10  ,height=2  ,fg="white"  ,bg="#e47911" ,font=('times', 15) )
        lbl.place(x=80, y=80)

        txt = tk.Entry(self.window,width=10  ,bg="white" ,fg="black",font=('times', 15, ' bold '))
        txt.place(x=220, y=90)

        lbl2 = tk.Label(self.window, text="Person Name",width=10  ,fg="white"  ,bg="#e47911"    ,height=2 ,font=('times', 15))
        lbl2.place(x=80, y=150)

        txt2 = tk.Entry(self.window,width=10  ,bg="white"  ,fg="black",font=('times', 15, ' bold ')  )
        txt2.place(x=220, y=155)

        lbl3 = tk.Label(self.window, text="Notification : ",width=10  ,fg="white"  ,bg="#e47911"  ,height=2 ,font=('times', 15, 'underline '))
        lbl3.place(x=80, y=210)

        self.message = tk.Label(self.window, text="" ,bg="white"  ,fg="black"  ,width=30  ,height=1, activebackground = "#e47911" ,font=('times', 15))
        self.message.place(x=220, y=220)

        message2 = tk.Label(self.window, text="" ,fg="#e47911"   ,bg="white",activeforeground = "green",width=30  ,height=1  ,font=('times', 15))
        message2.place(x=220, y=405)

        takeImg = tk.Button(self.window, text="Take Images", command=self.TakeImages  ,fg="white"  ,bg="#e47911"  ,width=10  ,height=1, activebackground = "#118ce1" ,font=('times', 15, ' bold '))
        takeImg.place(x=80, y=300)
        #quitWindow = tk.Button(window, text="Quit", command=close_window  ,fg="white"  ,bg="#e47911"  ,width=10  ,height=1, activebackground = "#118ce1" ,font=('times', 15, ' bold '))
        #quitWindow.place(x=500, y=300)

        ## doesn't do anything at this time
        ##checkbox = tk.Checkbutton(self.root, text="Keep me logged in")
        ##checkbox.grid(row=3, columnspan=2)
        quitWindow = tk.Button(self.window, text="Quit", command=self.buttonPushed  ,fg="white"  ,bg="#e47911"  ,width=10  ,height=1, activebackground = "#118ce1" ,font=('times', 15, ' bold '))
        quitWindow.place(x=500, y=300)


        self.window.mainloop()

   def TakeImages(self):
       cam = cv2.VideoCapture(0)
       #harcascadePath = "haarcascade_frontalface_default.xml"
       #detector=cv2.CascadeClassifier(harcascadePath)
       #sampleNum=0
       ret, img = cam.read()

       while(True):
           cv2.imshow('img1',img) #display the captured image
           if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y'
               cv2.imwrite('images/c1.png',img)
               cv2.destroyAllWindows()
               break

       df = OCRModule.readIdText(img)
       PAN_NO = OCRModule.pan_number(df)
       PERSON_NAME = OCRModule.personName(df)
       Id=PAN_NO
       name=PERSON_NAME
       res = "Images Saved for ID : " + Id +" Name : "+ name
       row = [Id , name]
       with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
           writer = csv.writer(csvFile)
           writer.writerow(row)
           csvFile.close()
           self.message.configure(text= res)
       #cam.release()
       #cv2.destroyAllWindows()

   def buttonPushed(self):
       self.window.destroy()

   def _login_btn_clickked(self):
       #print("Clicked")
       username = self.entry_1.get()
       password = self.entry_2.get()

      #print(username, password)

       if username == "test" and password == "test":
           print ("OK login")
           #box.showinfo("Login info", "Welcome Tester")
           #button1 = ttk.Button(self.root, text="Please click, Welcome to login!!!",
           #           command=lambda: self.controller.show_frame(StartPage))
           #button1.pack()
       else:
           #box.showerror("Login failed", "Incorrect username")
           print ("Error")
   def openRegWindow():
       LP=RegistrationPage()