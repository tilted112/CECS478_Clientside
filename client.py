import os, requests, json, sys, threading, time
import Decryptor
import Encryptor
from tkinter import *

window = Tk()
token = ""
user = ""

def Menu():
    frame = Frame(window)
    lbl = Label(frame, text="End2End encrypted Chat")
    createUserBtn = Button(frame, text="Signup",
                           command=lambda: [frame.pack_forget(), SignUp()])
    signInBtn = Button(frame, text="Signin",
                       command=lambda: [frame.pack_forget(), SignIn()])
    keygenBtn = Button(frame, text="Generate Key-Pair",
                       command=lambda: [KeyGen()])
    lbl.pack(expand=YES, fill=X)
    createUserBtn.pack(expand=YES, fill=X)
    signInBtn.pack(expand=YES, fill=X)
    keygenBtn.pack(expand=YES, fill=X)
    frame.pack()
    
def SignUp():
    frame = Frame(window)
    nameLbl = Label(frame, text="Username")
    nameEntry = Entry(frame, bd=5)
    pwLbl = Label(frame, text="Password")
    pwEntry = Entry(frame, bd=5)
    pw2Lbl = Label(frame, text="Reenter Password")
    pw2Entry = Entry(frame, bd=5)
    btn = Button(frame, text="Signup",
                 command=lambda: [frame.pack_forget(), CreateNewUser(nameEntry.get(), pwEntry.get(), pw2Entry.get())])
    nameLbl.pack(expand=YES, fill=X)
    nameEntry.pack(expand=YES, fill=X)
    pwLbl.pack(expand=YES, fill=X)
    pwEntry.pack(expand=YES, fill=X)
    pw2Lbl.pack(expand=YES, fill=X)
    pw2Entry.pack(expand=YES, fill=X)
    btn.pack(expand=YES, fill=X)
    frame.pack()

def CreateNewUser(name, pw, pw2):
    #route = "https://teamus.me/users/signup"
    route = "http://localhost:4000/users/signup"
    if(pw == pw2 and pw != ''):
        payload = "name=" + name + "&password=" + pw
        headers = {
                'content-type': "application/x-www-form-urlencoded",
                'cache-control': "no-cache"
                }
        response = requests.request("POST", route, data=payload, headers=headers)
        CreateNewUserSuccessful()
    else:
        CreateNewUserFailed()

def CreateNewUserSuccessful():
    frame = Frame(window)
    lbl = Label(frame, text="Signup completed")
    lbl.pack()
    btn = Button(frame, text="Menu",
                 command=lambda: [frame.pack_forget(), Menu()])
    btn.pack(expand=YES, fill=X)
    frame.pack()
    
def CreateNewUserFailed():
    frame = Frame(window)
    lbl = Label(frame, text="Signup failed. Try again")
    lbl.pack()
    btn = Button(frame, text="Menu",
                 command=lambda: [frame.pack_forget(), Menu()])
    btn.pack(expand=YES, fill=X)
    frame.pack()

def SignIn():
    frame = Frame(window)
    nameLbl = Label(frame, text="Username")
    nameEntry = Entry(frame, bd=5)
    pwLbl = Label(frame, text="Password")
    pwEntry = Entry(frame, bd=5)
    btn = Button(frame, text="Signin",
                 command=lambda: [frame.pack_forget(), Login('till', 'test')])
    menuBtn = Button(frame, text="Menu",
                     command=lambda: [frame.pack_forget(), Menu()])
    nameLbl.pack(expand=YES, fill=X)
    nameEntry.pack(expand=YES, fill=X)
    pwLbl.pack(expand=YES, fill=X)
    pwEntry.pack(expand=YES, fill=X)
    btn.pack(expand=YES, fill=X)
    menuBtn.pack(expand=YES, fill=X)
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
     
def KeyGen():
    print('keyGen')

def StartChat():
    frame = Frame(window)
    nameLbl = Label(frame, text="Enter name of your chatpartner")
    nameEntry = Entry(frame, bd=5)
    pkLbl = Label(frame, text="Enter filename of public key of your chatpartner")
    pkEntry = Entry(frame, bd=5)
    privLbl = Label(frame, text="Enter filename of your private key")
    privEntry = Entry(frame, bd=5)
    chatBtn = Button(frame, text="Start chat",
                     command=lambda: [chatBtn.config(state="disabled"), ChatWindow('till', pkEntry.get(), privEntry.get())])
    menuBtn = Button(frame, text="Menu",
                     command=lambda: [frame.pack_forget(), Menu()])
    nameLbl.pack(expand=YES, fill=X)
    nameEntry.pack(expand=YES, fill=X)
    pkLbl.pack(expand=YES, fill=X)
    pkEntry.pack(expand=YES, fill=X)
    privLbl.pack(expand=YES, fill=X)
    privEntry.pack(expand=YES, fill=X)
    chatBtn.pack(expand=YES, fill=X)
    menuBtn.pack(expand=YES, fill=X)
    frame.pack()
       
def ChatWindow(name, pk, privk):
    chatWindow = Toplevel(window)
    cpName = name
    cpPK = pk
    myPrivk = privk
    threadFlg = True
    
    print("Publickey:" + cpPK)
    print("Privatekey:" + myPrivk)
    
    frame = Frame(chatWindow)
    frame.pack(expand=YES, fill=BOTH)

    chatFrm = Frame(frame, width=600, height=600)
    chatFrm.pack(expand=YES, fill=BOTH)
    chatFrm.grid_columnconfigure(0,weight=1)
    chatFrm.grid_rowconfigure(0,weight=1)
    chatBox = Text(chatFrm, borderwidth=3)
    chatBox.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
    scrollBar = Scrollbar(chatFrm, command=chatBox.yview)
    scrollBar.grid(row=0, column=1, sticky="nsew")
    chatBox['yscrollcommand'] = scrollBar.set
        
    input_field = Entry(chatWindow)
    endBtn = Button(frame, text="End Chat",
                 command=lambda: [endChat()])
    input_field.pack(fill=X)
    endBtn.pack()
    
    
    def getMessages():
        nonlocal myPrivk
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
                message = Decryptor.MyJSONDecrypt(data, myPrivk)
                chatBox.insert(INSERT, '%s\n' % (cpName + ">" + message.decode("latin-1")))
        print("done")
    
    thread = threading.Thread(target=getMessages)
    thread.start()
    
    def sendMessage(event):
        nonlocal cpPK
        nonlocal cpName
        nonlocal input_field
        inputmsg = input_field.get()
        chatBox.insert(INSERT, '%s\n' % (user + ">" + inputmsg))
        jsonMsg = Encryptor.MyJSONEncrypt(inputmsg, cpPK)
        #route = "https://teamus.me/messages/sendmessage"
        route = "http://localhost:4000/messages/sendmessage"
        payload = "token=" + token + "&to=" + cpName + "&message=" + jsonMsg
        headers = {
                'content-type': 'application/x-www-form-urlencoded',
                'cache-type': 'no-cache'
                }
        response = requests.post(route, data=payload, headers=headers)
        input_field.delete(0,'end')
        return 'break'
        
    def endChat():
        print('endChat')
        nonlocal threadFlg
        threadFlg = False
        chatWindow.destroy()
       
    input_field.bind("<Return>", sendMessage)
    #chatWindow.bind("<Destroy>", endChat())
    
Menu()
window.title('End2End Chat by Team us')
window.geometry('300x300')
window.mainloop()