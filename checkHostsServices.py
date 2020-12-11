#!/usr/bin/env python
import re
import json
import requests
import logging, sys

STATUS_FILE_PATH = "/usr/local/nagios/var/status.dat"

def read_status():
    hosts = {}
    services = {}

    fh = open(STATUS_FILE_PATH)
    status_raw = fh.read()
    pattern = re.compile('([\w]+)\s+\{([\S\s]*?)\}',re.DOTALL)
    matches = pattern.findall(status_raw)
    for def_type, data in matches:
        lines = [line.strip() for line in data.split("\n")]
        pairs = [line.split("=", 1) for line in lines if line != '']
        data = dict(pairs)

        if def_type == "servicestatus":
            services[data['service_description']] = data
            if 'host_name' in data:
                hosts[data['host_name']]['services'].append(data)

        if def_type == "hoststatus":
            data['services'] = []
            hosts[data['host_name']] = data
    return {
        'hosts': hosts,
        'services': services,
    }

if __name__ == "__main__":
    data = read_status()

    #input_json = json.dumps(data['hosts'], sort_keys=True, indent=4)

# Transform json input to python objects

thisdict = json.dumps(data['hosts'], sort_keys=True, indent=4)
msg=""
countHost= 0
countServices= 0
Dict = eval(thisdict)
msg=msg+ "All Hosts Problems:\n"
msg=msg+ "---------------------\n"
for x in Dict:
  if int((Dict[x]['current_state'])) != 0:
   msg=msg+x+": DOWN\n"
   countHost = countHost + 1
msg=msg+"Total: "+ str(countHost)
msg=msg+"\n"
msg=msg+"\n"
msg=msg+"All Services Problem:\n"
msg=msg+"---------------------\n"
for x in Dict:
   i = len(Dict[x]['services']) 
   for a in range(0,i):
    if int((Dict[x]['services'][a]['current_state']))!=0:
     msg=msg+x + ": "+ Dict[x]['services'][a]['service_description']+"\n" 
     countServices= countServices+1
msg=msg+"Total: "+ str(countServices)
msg=msg.replace("_", "\_")
msg=msg.replace("*", "\*")
msg=msg.replace("'", "\'")
msg=msg.replace("[", "\[")


def telegram_bot_sendtext(bot_message):
    bot_token = '952800748:AAEYoMEC9ifiPpJfwi-KoYbV393Mz3-U4mc'
    bot_chatID = '-1001362065838'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

def report():
    my_message = msg
#    print(my_message)
    telegram_bot_sendtext(my_message)
report()
