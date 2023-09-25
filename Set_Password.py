import os
import pickle
from tkinter import *                   #python3 -m pip install tk
from cryptography.fernet import Fernet  #python3 -m pip install cryptography


raiz = Tk()

def GetValidUserInfo():
    _userID=StringVar()
    _password=StringVar()
    raiz.title("Set user and passwrod")
    raiz.resizable(False,False)
    raiz.geometry("250x130")
    myFrame = Frame(raiz,width=250,height=130)
    myFrame.pack()	
    _userID.set(os.getenv('username'))
    userLabel = Label(myFrame, text="Valid UserID")
    userLabel.grid(row=1,column=0, padx=10, pady=10)
    userEntry=Entry(myFrame, textvariable=_userID)
    userEntry.grid(row=1,column=1, padx=10, pady=10)
    passwordLabel = Label(myFrame, text="Password")
    passwordLabel.grid(row=2,column=0, padx=10, pady=10)
    passwordEntry=Entry(myFrame, textvariable=_password, show="*")
    passwordEntry.grid(row=2,column=1, padx=10, pady=10)
    botonAceptar=Button(raiz,text="Accept",command=GetGUIInfo)
    botonAceptar.pack()
    raiz.mainloop()
    userId = _userID.get()
    password = _password.get()
    return userId,password

def GetGUIInfo():
    raiz.destroy()    
    return

if __name__ == '__main__':
    userId, password = GetValidUserInfo()
    print("Set User and password for userID:" + userId)
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encPassword = fernet.encrypt(password.encode())
    user_password = {'userID':userId,'encPassword':encPassword,'key':key}
    # Open a file and use dump()
    with open('entry_info.pkl', 'wb') as file:
        # A new file will be created
        pickle.dump(user_password, file)