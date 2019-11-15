
from pyzabbix import ZabbixAPI
from datetime import datetime
import pandas as pd

#-------------------------------------------------------------------------
# API_connection

zabbixServer = 'http://127.0.0.1/zabbix/'
zabbixUser = 'user'
zabbixPass = 'pass'
z = ZabbixAPI(url=zabbixServer, user=zabbixUser, password=zabbixPass)
z.timeout = 180

#-------------------------------------------------------------------------
# declaration of variables

LOGIN = []
IP = []
PROBLEM = []
FECHA = []
GROUP = []
STATUS = []
Time_i = 1552314794  # date begin
Time_f = 1570804394  # date end
#-------------------------------------------------------------------------
# get_data

problems_all = z.problem.get(time_from = Time_i,time_till = Time_f )
interface_all = z.hostinterface.get()
triggers_all = z.do_request('trigger.get',
                            {"output": ["triggerid","description","priority"],
                             "selectHosts": "extend",
                             "filter": {"value": 1,"description":"{HOST.NAME} is unavailable by ICMP"},
                             "sortfield": "priority","sortorder": "DESC"})
groups_Total = z.do_request('host.get',
                            {"output": ["hostid","status"],
                                "selectGroups": "extend"
                            })
#-------------------------------------------------------------------------
# proccesing

for i in problems_all:
    for j in triggers_all['result']:
        if (i['objectid'] == j['triggerid']):
            for k in interface_all:
                if j['hosts'][0]['hostid'] == k['hostid']:
                    for L in groups_Total['result']:
                        if k['hostid'] == L['hostid']:
                            GROUP.append(L['groups'][0]['name'])
                            LOGIN.append(j['hosts'][0]['host'])
                            IP.append(k['ip'])
                            PROBLEM.append(i['name'])
                            FECHA.append(datetime.fromtimestamp(int(i['clock'])))
                            STATUS.append(L['status'])

#-------------------------------------------------------------------------
# print and send to csv

pre_data = {'GROUP' : GROUP,
        'LOGIN' : LOGIN,
        'IP'    : IP,
        'PROBLEM' : PROBLEM,
         "DATE"   : FECHA,
         "STATUS" : STATUS
        }
data = pd.DataFrame(pre_data)
data.to_csv("data_problems.csv")
print(data)








