import subprocess
import json
import re

settings_open = open('/home/admin/tsalert/settings.json', 'r')
settings_load = json.load(settings_open)

interval_time = settings_load["interval_time"]
target_ip = settings_load["target_ip"]
target_com = settings_load["target_com"]
target_oid = settings_load["target_oid"]

#設定ファイルでアラートが有効化されているかどうか判定
def alert_isEnabled(alert_code):
    if alert_code in settings_load["alert_list"]:
        return settings_load["alert_list"][alert_code]["isEnabled"]
    return False

#取得したattributeをmsgに代入
def subst(alert_attribute,alert_msg):
  for k in alert_attribute:
    alert_msg = alert_msg.replace("{."+k+"}",alert_attribute[k])
  return alert_msg

#アラートを改行で分割してリストに格納
alert_s_raw = subprocess.run(["/usr/local/scaligent/bin/tscli alert list --since " + str(interval_time) + "m"],shell=True,stdout=subprocess.PIPE,encoding='utf-8')
alert_s_list_raw = alert_s_raw.stdout.splitlines()

#不要行削除
alert_s_list = []
for alert_s_list_raw_temp in alert_s_list_raw[1:]:
    if len(alert_s_list_raw_temp.split("|")[0]) == 8:
        alert_s_list.append(alert_s_list_raw_temp)

#アラートコードを抽出してtrapごとに分割
trap_list = []
for alert_s in alert_s_list:
    matchobj = re.search("A[0-9]{5}",alert_s.split("|")[0])
    if(matchobj):
        if alert_isEnabled(matchobj.group()):
            alert_attribute = json.loads(alert_s.split("|")[3])
            alert_msg = settings_load["alert_list"][matchobj.group()]["msg"]
            alert_msg = subst(alert_attribute,alert_msg)
            alert_id = "id:" + settings_load["alert_list"][matchobj.group()]["id"]
            alert_msg = "msg:" + alert_msg
            trap_list.append("\n".join([alert_id,alert_msg]))


#trap送信
if(len(trap_list)):
    f = open('/home/admin/tsalert/tsalert.log','w')
    f.write("snmp trap tool\n")
    f.close()
for trap_msg in trap_list:
    trap_cmd = "/usr/bin/snmptrap -v 1 -c " + target_com + " " + target_ip + " '' " + target_oid + " s '" + trap_msg + "'"
    subprocess.run([trap_cmd],shell=True)
    f = open('/home/admin/tsalert/tsalert.log','a')
    f.write(trap_cmd + "\n")
    f.close()
