import shelve
import csv
from os import path

USERS_DB_FILE = 'Users_Database'
FAILED_USERS_FILE = 'Users_Not_Reported'

if path.isfile(USERS_DB_FILE + '.db'):
    print('Extracting ' + USERS_DB_FILE + '...')
    with shelve.open(USERS_DB_FILE, 'r') as usersDB:
        with open(USERS_DB_FILE + '.csv', 'w', newline='\n') as reportFile:
            fileWriter = csv.writer(reportFile, delimiter=',')
            fileWriter.writerow(['SAP NUMBER',
                                 'NAME',
                                 'LAST NAME',
                                 'MONITOR ID',
                                 'USER TYPE',
                                 'PHOTO PATH'])
            for user in usersDB:
                fileWriter.writerow([usersDB[user]['sap_number'],
                                     usersDB[user]['name'],
                                     usersDB[user]['last_name'],
                                     usersDB[user]['monitor_id'],
                                     usersDB[user]['user_type'],
                                     usersDB[user]['photo_path']])
    print('Finished!')

if path.isfile(FAILED_USERS_FILE + '.db'):
    print('Extracting ' + FAILED_USERS_FILE + '...')
    with shelve.open(FAILED_USERS_FILE, 'r') as usersDB:
        with open(FAILED_USERS_FILE + '.csv', 'w', newline='\n') as reportFile:
            fileWriter = csv.writer(reportFile, delimiter=',')
            fileWriter.writerow(['SAP NUMBER',
                                 'MONITOR ID',
                                 'USER TYPE',
                                 'TEMPERATURE',
                                 'MASK',
                                 'DATE TIME',
                                 'AUTHORIZED ACCESS',
                                 'DEVICE ID'])
            for user in usersDB:
                fileWriter.writerow([usersDB[user]['sap_number'],
                                     usersDB[user]['monitor_id'],
                                     usersDB[user]['user_type'],
                                     usersDB[user]['temperature'],
                                     usersDB[user]['mask'],
                                     usersDB[user]['date_time'],
                                     usersDB[user]['authorized_access'],
                                     usersDB[user]['device_id']])
    print('Finished!')
