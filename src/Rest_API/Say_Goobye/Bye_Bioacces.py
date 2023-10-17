import json
import paramiko
import requests
from urllib.request import Request, urlopen 
import urllib.request
import ssl
import ctypes
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
        print(token)

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

def update_file(host,port,username,password,source_file_path,target_file_path):
    result={}
    result['host']=host
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    sftp = ssh.open_sftp()
    command = 'sudo rm -f ' + target_file_path
    session = ssh.get_transport().open_session()
    session.set_combine_stderr(True)
    session.get_pty()        
    session.exec_command(command)
    stdin = session.makefile('wb', -1)
    stdout = session.makefile('rb', -1)
    stdin.write(password + '\n')
    stdin.flush()
    print(str(stdout.readlines()))
    sftp.put(source_file_path,target_file_path)
    print('FILE_UPDATED')
    sftp.close()
    ssh.close()        
    return result

def set_wall_paper(host,port,username,password,source_file):
    result={}
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    try:
        result['host']=host
        result['Exception'] = 'NA'
        command = ' gsettings set org.gnome.desktop.background picture-uri ' + source_file
        command_comment = 'Wallpaper was set as :' + source_file
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()
        result['status'] = command_comment
    except Exception as e:
        result['status'] = command_comment
        result['Exception'] = str(e)
    ssh.close()        
    return result

def send_command(host,port,username,password,command):
    result={}
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    try:
        session = ssh.get_transport().open_session()
        session.set_combine_stderr(True)
        session.get_pty()        
        session.exec_command(command)
        stdin = session.makefile('wb', -1)
        stdout = session.makefile('rb', -1)
        stdin.write(password + '\n')
        stdin.flush()
        command_comment = str(stdout.readlines())
        print(command_comment)
    except Exception as e:
        print('Exception was found: ' + str(e))
    
    ssh.close()        
    return result

def finish_SBA(host,port,mode,username,password):
    result={}
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    try:
        
        session = ssh.get_transport().open_session()
        session.set_combine_stderr(True)
        session.get_pty()        
        
        command = 'sudo systemctl stop rest.service'
        session.exec_command(command)
        stdin = session.makefile('wb', -1)
        stdout = session.makefile('rb', -1)
        stdin.write(password + '\n')
        stdin.flush()
        lines = stdout.readlines()
        print('# ', command)
        print('\t',lines)

        command = 'sudo systemctl stop handler.service'
        session.exec_command(command)
        stdin = session.makefile('wb', -1)
        stdout = session.makefile('rb', -1)
        stdin.write(password + '\n')
        stdin.flush()
        lines = stdout.readlines()
        print('# ', command)
        print('\t',lines)

        command = 'sudo systemctl stop sba.service'
        session.exec_command(command)
        stdin = session.makefile('wb', -1)
        stdout = session.makefile('rb', -1)
        stdin.write(password + '\n')
        stdin.flush()
        lines = stdout.readlines()
        print('# ', command)
        print('\t',lines)



    except Exception as e:
        print('Exception was found: ' + str(e))

    ssh.close()        
    return result


if __name__ == '__main__':
    host_file = 'hosts.json'
    with open(host_file) as jsonFile:
        hosts = json.load(jsonFile)
        jsonFile.close()
    port = 22
    username = 'edt'
    password = 'admin'
    source_file_path = './screen_say_goobye.jpg'
    target_file_path='/home/edt/Documents/Share/screen_mantenimiento.jpg'
    mode='stop'
    print(list(eval(hosts['hosts'])))
    host_list = list(eval(hosts['hosts']))
    print(type(host_list))
    print(host_list)
        
    for host in host_list:
        print('Processing hots:' + host)
        update_file(host=host,port=port,username=username,password=password,source_file_path = source_file_path,target_file_path=target_file_path)
        set_wall_paper(host=host,port=port,username=username,password=password,source_file=target_file_path)

        command = 'sudo /etc/init.d/cron stop'
        send_command(host=host,port=port,username=username,password=password,command=command)
        command = 'sudo systemctl stop rest.service'
        send_command(host=host,port=port,username=username,password=password,command=command)
        command = 'sudo systemctl stop handler.service'
        send_command(host=host,port=port,username=username,password=password,command=command)
        command = 'sudo systemctl stop sba.service'
        send_command(host=host,port=port,username=username,password=password,command=command)
        command = 'sudo rm -rf /home/edt/Documents/Share/EDT_AccessCTRL'
        send_command(host=host,port=port,username=username,password=password,command=command)
        command = 'sudo rm /home/edt/Documents/Share/_ImagesLog/*'
        send_command(host=host,port=port,username=username,password=password,command=command)
        command = 'sudo rm /home/edt/Documents/Share/_Logs/*'
        send_command(host=host,port=port,username=username,password=password,command=command)

        
        



