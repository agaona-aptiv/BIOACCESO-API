import pandas as pd

alias_hosts = pd.read_excel('api/alias_host.xlsx')
print(alias_hosts)
with open('C:\WINDOWS\system32\drivers\etc\hosts') as f:
    lines = f.readlines()
    print('Host alias found:')
    for line in lines:
        if ('#' not in line):
            print('IP: ', line[:-1])

host_to_add = ''
for (host,alias) in zip(alias_hosts['IP'], alias_hosts['alias']):
    if (host not in str(lines)):
        host_to_add = host_to_add + str(host) + ' ' + alias + '\n'
print(host_to_add)
if len(host_to_add)>0:
    f = open('C:\WINDOWS\system32\drivers\etc\hosts','a+')
    f.writelines('\n# API BIOACCESO Adding Hosts\n')
    lines = f.readlines()
    f.writelines(host_to_add)
    f.writelines('# END OF API BIOACCESO')
    f.close()





    