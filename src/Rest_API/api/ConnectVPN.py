import time
import pickle
from pywinauto import application
from pywinauto import mouse
import warnings
warnings.simplefilter('ignore', category=UserWarning)
from cryptography.fernet import Fernet


def get_user_info():
    with open('entry_info.pkl', 'rb') as file:
        user_password = pickle.load(file)
        fernet = Fernet(user_password['key'])
        userID = user_password['userID']
        password = fernet.decrypt(user_password['encPassword']).decode()
        return userID, password   

if __name__ == '__main__':
    userID, password = get_user_info()
    #Execute C:\Program Files (x86)\DCC Tools\CDA 6\CDA\CDA.exe
    #app_file = r'C:\Program Files (x86)\CheckPoint\Endpoint Connect\TrGUI.exe'
    app_file = r'C:\\Windows\\System32\\notepad.exe'
    print(app_file)
    app =  application.Application(app_file)
    app.start()
    print('Loaded')

    #Get Application Object
    #window_title='TrGUI'
    window_title='Untitled – Notepad'
    acd_app = app.window(title_re = window_title)
    time.sleep(5)

    #Send User
    #mouse.click(button='left', coords=(550, 460))
    #acd_app.type_keys(userID,with_spaces=True)
    time.sleep(2)
    #Send Password
    mouse.click(button='left', coords=(200, 350))
    acd_app.type_keys(password,with_spaces=True)
    time.sleep(2)
    mouse.click(button='left', coords=(75, 480))

