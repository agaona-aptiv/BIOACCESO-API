import requests                                             #python3 -m pip install requests
import pickle
from cryptography.fernet import Fernet                      #python3 -m pip install cryptography
#from urllib.request import Request, urlopen 
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import pandas as pd
from datetime import date, timedelta

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

def GetRecords(user,password,hub,from_date,to_date,sap="",device="",site=""):
    url = 'https://'+hub+'/sba_hub/API/public/index.php/api/v1/hubapi/auth/login'
    payload = {"userid": user, "passwd": password}
    login_response = requests.post(url, data=payload,verify=False)
    token = login_response.json()['token']
    POST_URL = 'https://'+ hub+ '/sba_hub/API/public/index.php/api/v1/hubapi/records/all'
    payload = {"from_date": from_date,"to_date": to_date,"sap": sap,"device": device,"site": site}
    REQUEST_TIMEOUT_POST_PENDING = (3, 6)
    users_records = requests.post(url=POST_URL, json=payload, timeout=REQUEST_TIMEOUT_POST_PENDING,auth=BearerAuth(token), verify=False)  # add verify False SSL
    USER_TYPE = ['Empleado','Visita','NOT_DEFINED','NOT_DEFINED']
    AUTORIZED_ACCESS = ['Si','No','No']
    CUBREBOCAS = ['Incorrecto','Correcto']
    ESTATUS_MONITOR = ['Enviado','No Enviado','NOT_DEFINEED_3','ID Seguimiento inválido','NOT_DEFINED_5']
    user_record_list = []
    for user_record in users_records.json():
        try:
            user_record_json ={}
            user_record_json['#Empleado_ID'] = user_record['sap_number']
            user_record_json['Nombre'] = user_record['users']['lastname'] + ' '+ user_record['users']['surname'] + ' '+ user_record['users']['name']
            user_record_json['Dispositivo'] = user_record['devices']['mac_address']
            user_record_json['Alias'] = user_record['devices']['device_type']
            user_record_json['ID_Seguimiento'] = user_record['monitor_id']
            user_record_json['Tipo_Usuario'] = USER_TYPE[user_record['user_type']-1]
            user_record_json['Autorizado?'] = AUTORIZED_ACCESS[user_record['authorized_access']-1]
            user_record_json['Temperatura'] = user_record['temperature']
            user_record_json['Fecha_Registro'] = user_record['date_time']
            user_record_json['Cubrebocas?'] = CUBREBOCAS[user_record['mask']]
            user_record_json['Estatus_Monitor_FCS'] = ESTATUS_MONITOR[user_record['status']-1]
            user_record_json['Fecha_Envio_Monitor_FCS'] = user_record['to_fcs']
            user_record_list.append(user_record_json)        
        except Exception as e:
            print('Error on: ',user_record)
            print('Exception:',str(e))

    data_set = pd.DataFrame.from_records(user_record_list)
    return data_set

def get_user_info(entry_info='entry_info.pkl'):
    with open(entry_info, 'rb') as file:
        user_password = pickle.load(file)
        fernet = Fernet(user_password['key'])
        userID = user_password['userID']
        password = fernet.decrypt(user_password['encPassword']).decode()
        return userID, password 

if __name__ == '__main__':
    day_to_report = str(date.today() - timedelta(days=1))
    from_date = day_to_report + ' 00:00:00'
    to_date = day_to_report + ' 23:59:59'

    #Get Records from CARSO
    user, password = get_user_info(entry_info = 'CARSO.pkl')
    hub = 'CARSO_HUB'                #Solo la IP del HUB o el Alias del HUB arnelec o como le llamen ejemplo  https://IP_DEL_HUB/sba_hub
    data_set = GetRecords(user=user,password=password,hub=hub,from_date=from_date,to_date=to_date)
    data_set.to_excel(day_to_report +'_'+hub+ '_Registros.xlsx',sheet_name='registros', index=False)

    #Get Records from CUPRO
    user, password = get_user_info(entry_info = 'CUPRO.pkl')
    hub = 'CUPRO'                 #Solo la IP del HUB o el Alias del HUB arnelec o como le llamen ejemplo  https://IP_DEL_HUB/sba_hub
    data_set = GetRecords(user=user,password=password,hub=hub,from_date=from_date,to_date=to_date)
    data_set.to_excel(day_to_report +'_'+hub+ '_Registros.xlsx',sheet_name='registros', index=False)