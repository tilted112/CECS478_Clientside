import os, requests, json, sys, threading, time
import Decryptor
import Encryptor
from tkinter import *

window = Tk()
token = ""
user = ""
cpName = ""
cpPK = ""
myPrivk = ""
threadFlg = True

def Menu():
    frame = Frame(window)
    label = Label(frame, text="End2End encrypted Chat")
    label.pack(side="top", fill="x", pady=10)
    createUserBtn = Button(frame, text="Signup",
                           command=lambda: [frame.pack_forget(), SignUp()])
    signInBtn = Button(frame, text="Signin",
                       command=lambda: [frame.pack_forget(), SignIn()])
    createUserBtn.pack()
    signInBtn.pack()
    frame.pack()
    
def SignUp():
    frame = Frame(window)
    nameLbl = Label(frame, text="Username")
    nameEntry = Entry(frame, bd=5)
    pwLbl = Label(frame, text="Password")
    pwEntry = Entry(frame, bd=5)
    btn = Button(frame, text="Signup",
                 command=lambda: [frame.pack_forget(), CreateNewUser(nameEntry.get(), pwEntry.get())])
    nameLbl.pack()
    nameEntry.pack()
    pwLbl.pack()
    pwEntry.pack()
    btn.pack()
    frame.pack()

def CreateNewUser(name, pw):
    #route = "https://teamus.me/users/signup"
    route = "http://localhost:4000/users/signup"
    payload = "name=" + name + "&password=" + pw
    headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
            }
    response = requests.request("POST", route, data=payload, headers=headers)
    CreateNewUserSuccessful()

def CreateNewUserSuccessful():
    frame = Frame(window)
    lbl = Label(frame, text="Signup completed")
    lbl.pack()
    btn = Button(frame, text="Menu",
                 command=lambda: [frame.pack_forget(), Menu()])

def SignIn():
    frame = Frame(window)
    nameLbl = Label(frame, text="Username")
    nameEntry = Entry(frame, bd=5)
    pwLbl = Label(frame, text="Password")
    pwEntry = Entry(frame, bd=5)
    btn = Button(frame, text="Signin",
                 command=lambda: [frame.pack_forget(), Login('till', 'test')])
    nameLbl.pack()
    nameEntry.pack()
    pwLbl.pack()
    pwEntry.pack()
    btn.pack()
    frame.pack()
    
def Login(name, pw):
     #route = "https://teamus.me/users/signin"
    route = "http://localhost:4000/users/signin"
    payload = "name=" + name + "&password=" + pw
    headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
            }
    response = requests.request("POST", route, data=payload, headers=headers)
    global token 
    global user 
    token = response.json().get('token')
    success = response.json().get('success')
    user = name
    if(success):
        print("Signin successful")
        StartChat()
    else:
        print("Signin failed")
        SignIn()        
        
def StartChat():
    frame = Frame(window)
    nameLbl = Label(frame, text="Enter name of your chatpartner")
    nameEntry = Entry(frame, bd=5)
    pkLbl = Label(frame, text="Enter public key of your chatpartner")
    pkEntry = Entry(frame, bd=5)
    privLbl = Label(frame, text="Enter your private key")
    privEntry = Entry(frame, bd=5)
    chatBtn = Button(frame, text="Start chat",
                     command=lambda: [frame.pack_forget(), ChatWindow('till', pkEntry.get(), privEntry.get())])
    menuBtn = Button(frame, text="Menu",
                     command=lambda: [frame.pack_forget(), Menu()])
    nameLbl.pack()
    nameEntry.pack()
    pkLbl.pack()
    pkEntry.pack()
    privLbl.pack()
    privEntry.pack()
    chatBtn.pack()
    menuBtn.pack()
    frame.pack()
    

    
def ChatWindow(name, pk, privk):
    global cpName
    global cpPK
    global myPrivk
    cpName = name
    cpPK = pk
    myPrivk = privk
    
    print("Publickey:" + cpPK)
    print("Privatekey:" + myPrivk)
    
    chatBox = Text(window)
    chatBox.pack()
    input_user = StringVar()
    input_field = Entry(window, text=input_user)
    input_field.pack(side=BOTTOM, fill=X)
    frame = Frame(window)
    
    def getMessages():
        global threadFlg
        while(threadFlg):
            time.sleep(1)
            #route = "https://teamus.me/messages/getmessage"
            route = "http://localhost:4000/messages/getmessage" 
            payload = "token=" + token + "&from=" + cpName
            headers = {
                    'content-type': "application/x-www-form-urlencoded",
                    'cache-control': "no-cache"
                    }
            response = requests.request("POST", route, data=payload, headers=headers)
            print(response.status_code)            
            if(response.status_code == 200):
                data = response.json().get('message')
                print(data)
                message = Decryptor.MyJSONDecrypt(data, "private_key.pem")
                chatBox.insert(INSERT, '%s\n' % (cpName + ">" + message.decode("latin-1")))
                print(message)
        print("done")
    
    thread = threading.Thread(target=getMessages)
    thread.start()
    
    def sendMessage(event):
       inputmsg = input_field.get()
       print(inputmsg)
       if(inputmsg == "!quit"):
           global threadFlg
           threadFlg = False
           return "break"
       else:
           chatBox.insert(INSERT, '%s\n' % (user + ">" + inputmsg))
           jsonMsg = Encryptor.MyJSONEncrypt(inputmsg, "public_key.pem")
           print(jsonMsg)
           #print("encryptor")
           #route = "https://teamus.me/messages/sendmessage"
           route = "http://localhost:4000/messages/sendmessage"
           payload = "token=" + token + "&to=" + cpName + "&message=" + jsonMsg
           #print(payload)
           headers = {
                   'content-type': "application/x-www-form-urlencoded",
                   'cache-control': "no-cache"
                     }
           #print(payload)
           response = requests.post(route, data=payload, headers=headers)
           input_user.set('')
           return "break"
       
    input_field.bind("<Return>", sendMessage)
    
    frame.pack()
    
Menu()
window.mainloop()