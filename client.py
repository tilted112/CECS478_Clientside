import os, requests, json, sys, threading, time
import Decryptor
import Encryptor
import KeyGen
from tkinter import *
from tkinter import messagebox

#global variables, storage for token, username and userid
window = Tk()
token = ""
user = ""
userId = ""

#MainMenu - Signup, Signin, KeyGen
def Menu():
    frame = Frame(window)
    lbl = Label(frame, text="End2End encrypted Chat")
    createUserBtn = Button(frame, text="Signup", bd=3,
                           command=lambda: [frame.pack_forget(), SignUp()])
    signInBtn = Button(frame, text="Signin", bd=3,
                       command=lambda: [frame.pack_forget(), SignIn()])
    keygenBtn = Button(frame, text="Generate Key-Pair", bd=3,
                       command=lambda: [frame.pack_forget(), KeyGenerator()])
    lbl.pack(expand=YES, fill=X)
    createUserBtn.pack(expand=YES, fill=X)
    signInBtn.pack(expand=YES, fill=X)
    keygenBtn.pack(expand=YES, fill=X)
    frame.pack()
    
#SignUp GUI -     
def SignUp():
    frame = Frame(window)
    nameLbl = Label(frame, text="Username")
    nameEntry = Entry(frame, bd=5)
    pwLbl = Label(frame, text="Password")
    pwEntry = Entry(frame, bd=5, show='*')
    pw2Lbl = Label(frame, text="Reenter Password")
    pw2Entry = Entry(frame, bd=5, show='*')
    btn = Button(frame, text="Signup",bd=3,
                 command=lambda: [frame.pack_forget(), CreateNewUser(nameEntry.get(), pwEntry.get(), pw2Entry.get())])
    nameLbl.pack(expand=YES, fill=X)
    nameEntry.pack(expand=YES, fill=X)
    pwLbl.pack(expand=YES, fill=X)
    pwEntry.pack(expand=YES, fill=X)
    pw2Lbl.pack(expand=YES, fill=X)
    pw2Entry.pack(expand=YES, fill=X)
    btn.pack(expand=YES, fill=X)
    frame.pack()

#Create a new User function
def CreateNewUser(name, pw, pw2):
    route = "https://teamus.me/users/signup"
    #both passwords must be equal and not empty
    if(pw == pw2 and pw != ''):
        payload = "name=" + name + "&password=" + pw
        headers = {
                'content-type': "application/x-www-form-urlencoded",
                'cache-control': "no-cache"
                }
        response = requests.request("POST", route, data=payload, headers=headers)
        print(response)
        #if user creation was successful
        if(response.status_code == 200):
            CreateNewUserSuccessful()
        else:
            CreateNewUserFailed()
    else:
        CreateNewUserFailed()

#New User created GUI
def CreateNewUserSuccessful():
    frame = Frame(window)
    lbl = Label(frame, text="Signup completed")
    lbl.pack()
    btn = Button(frame, text="Menu",bd=3,
                 command=lambda: [frame.pack_forget(), Menu()])
    btn.pack(expand=YES, fill=X)
    frame.pack()
    
#New User creation failed GUI
def CreateNewUserFailed():
    frame = Frame(window)
    lbl = Label(frame, text="Signup failed. Try again")
    lbl.pack()
    btn = Button(frame, text="Menu",bd=3,
                 command=lambda: [frame.pack_forget(), Menu()])
    btn.pack(expand=YES, fill=X)
    frame.pack()

#SignIn GUI
def SignIn():
    frame = Frame(window)
    nameLbl = Label(frame, text="Username")
    nameEntry = Entry(frame, bd=5)
    pwLbl = Label(frame, text="Password")
    pwEntry = Entry(frame, bd=5, show='*')
    btn = Button(frame, text="Signin",bd=3,
                 command=lambda: [frame.pack_forget(), Login(nameEntry.get(), pwEntry.get())])
    menuBtn = Button(frame, text="Menu",bd=3,
                     command=lambda: [frame.pack_forget(), Menu()])
    nameLbl.pack(expand=YES, fill=X)
    nameEntry.pack(expand=YES, fill=X)
    pwLbl.pack(expand=YES, fill=X)
    pwEntry.pack(expand=YES, fill=X)
    btn.pack(expand=YES, fill=X)
    menuBtn.pack(expand=YES, fill=X)
    frame.pack()

#Signin function
def Login(name, pw):
    global token 
    global user
    global userId
    route = "https://teamus.me/users/signin"
    payload = "name=" + name + "&password=" + pw
    headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
            }
    response = requests.request("POST", route, data=payload, headers=headers)
    #if signin was successful
    if(response.status_code == 200):
        #get userid and token from response
        userId = response.json().get('id')
        user = name
        token = response.json().get('token')
        ChatMenu()
    else:
        #signin failed
        messagebox.showinfo('Notification','Your login attempt faild. Please try again')
        SignIn()        
     
#Generates a key pair for the chat
def KeyGenerator():
    frame = Frame(window)
    privkLbl = Label(frame, text="Enter filename for private key")
    privkEntry = Entry(frame, bd=5)
    pkLbl = Label(frame, text="Enter filename for public key")
    pkEntry = Entry(frame, bd=5)
    keyGenBtn = Button(frame, text="Generate Keys", bd=3,
                       command=lambda: [frame.pack_forget(), GenerateKeyPair(privkEntry.get(), pkEntry.get())])
    privkLbl.pack(expand=YES, fill=X)
    privkEntry.pack(expand=YES, fill=X)
    pkLbl.pack(expand=YES, fill=X)
    pkEntry.pack(expand=YES, fill=X)
    keyGenBtn.pack(expand=YES, fill=X)
    frame.pack()
    
def GenerateKeyPair(filenamePrivK, filenamePK):
    if(filenamePK != '' and filenamePrivK != ''):
        KeyGen.GenerateKeyPair(filenamePrivK, filenamePK)
        messagebox.showinfo("Notification", "Keypair generated")
    else:
        messagebox.showerror("Error", "Please type in filenames for the keys")
    Menu()
        
    

#ChatMenu GUI - StartChat, Delete User, MainMenu
def ChatMenu():
    global user
    frame = Frame(window)
    userLbl = Label(frame, text="Your logged in as:" + user)
    nameLbl = Label(frame, text="Enter name of your chatpartner")
    nameEntry = Entry(frame, bd=5)
    pkLbl = Label(frame, text="Enter filename of public key of your chatpartner")
    pkEntry = Entry(frame, bd=5)
    privLbl = Label(frame, text="Enter filename of your private key")
    privEntry = Entry(frame, bd=5)
    chatBtn = Button(frame, text="Start chat",
                     command=lambda: [chatBtn.config(state="disabled"), ChatWindow(nameEntry.get(), pkEntry.get(), privEntry.get())])
    menuBtn = Button(frame, text="Menu",
                     command=lambda: [frame.pack_forget(), Menu()])
    deleteBtn = Button(frame, text="Delete User",
                       command=lambda: [frame.pack_forget(), DeleteUser()])
    userLbl.pack(expand=YES, fill=X)
    nameLbl.pack(expand=YES, fill=X)
    nameEntry.pack(expand=YES, fill=X)
    pkLbl.pack(expand=YES, fill=X)
    pkEntry.pack(expand=YES, fill=X)
    privLbl.pack(expand=YES, fill=X)
    privEntry.pack(expand=YES, fill=X)
    chatBtn.pack(expand=YES, fill=X)
    deleteBtn.pack(expand=YES, fill=X)
    menuBtn.pack(expand=YES, fill=X)
    frame.pack()
    
#Delete user in Database function    
def DeleteUser():
    global userId
    global token
    route = "https://teamus.me/users/"
    route = route + userId
    headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache",
            'x-access-token': token
            }
    response = requests.delete(route, data=None, headers=headers)
    #if deletion was successful
    if(response.status_code == 200):
        messagebox.showinfo('Notification', 'User successfully deleted')
        Menu()
    else:
        messagebox.showerror('Error', 'Unable to delete user. Try again.')
        Menu()
   
#Opens a new Window - Chat GUI
def ChatWindow(name, pk, privk):
    chatWindow = Toplevel(window)
    cpName = name
    cpPK = pk
    myPrivk = privk
    threadFlg = True
       
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
        
    msgField = Entry(chatWindow)
    endBtn = Button(frame, text="End Chat",
                 command=lambda: [endChat()])
    msgField.pack(fill=X)
    endBtn.pack(side=BOTTOM)
    
    #Function which checks every second for new messages 
    def getMessages():
        nonlocal myPrivk
        global user
        while(threadFlg):
            time.sleep(1)
            route = "https://teamus.me/messages/getmessage"
            payload = "from=" + cpName + "&to=" + user
            headers = {
                    'content-type': "application/x-www-form-urlencoded",
                    'cache-control': "no-cache",
                    'x-access-token': token
                    }
            response = requests.request("POST", route, data=payload, headers=headers)
            #if new message
            if(response.status_code == 200):
                #get message from response and decrypt it
                data = response.json().get('message')
                message = Decryptor.MyJSONDecrypt(data, myPrivk)
                chatBox.insert(INSERT, '%s\n' % (cpName + ">" + message.decode("latin-1")))
        print("End of chat")
    
    #Function to send a message to the server
    def sendMessage(event):
        nonlocal cpPK
        nonlocal cpName
        nonlocal msgField
        global user
        inputmsg = msgField.get()
        chatBox.insert(INSERT, '%s\n' % (user + ">" + inputmsg))
        jsonMsg = Encryptor.MyJSONEncrypt(inputmsg, cpPK)
        route = "https://teamus.me/messages/sendmessage"
        payload = "from=" + user + "&to=" + cpName + "&message=" + jsonMsg
        headers = {
                'content-type': 'application/x-www-form-urlencoded',
                'cache-type': 'no-cache',
                'x-access-token': token
                }
        response = requests.post(route, data=payload, headers=headers)
        #Clear message field
        msgField.delete(0,'end')
        return 'break'
        
    #Function to end the chat
    def endChat():
        #ask whether user wants to end the chat
        if messagebox.askyesno('Notification', 'Do you really want to end the Chat?'):
            nonlocal threadFlg
            nonlocal chatWindow
            #Stop getMessage function
            threadFlg = False
            #Close ChatWindow
            chatWindow.destroy()
      
    #Start thread to check for new messages
    thread = threading.Thread(target=getMessages)
    thread.start()
    #bind Return-Key on sendMessage function
    msgField.bind("<Return>", sendMessage)
    #chatWindow.bind("<Destroy>", endChat())

#Calls MainMenu, Starts the GUI  
Menu()
window.title('End2End Chat by Team us')
window.geometry('300x300')
window.mainloop()