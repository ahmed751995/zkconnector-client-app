from zk import ZK, const
import requests, json

url = "http://103.136.40.46:72/api/resource/zkaccess"

zk = ZK('192.168.1.201', port=4370, timeout=5, password=0, force_udp=True, ommit_ping=False)
headers = {
  'Authorization': 'token fdc04965d6f8c41:1044dbe6947eff3',
  'Cookie': 'full_name=Guest; sid=Guest; system_user=no; user_id=Guest; user_image='
}

def post_req(url, headers, data):
    response = requests.request("POST", url, headers=headers, data=data)
    print(response.text)


try:
    conn = zk.connect()
    # re-enable device after all commands already executed
    for attendance in conn.live_capture():
        if attendance is None:
            # implement here timeout logic
            pass
        else:
            payload = {}
            payload["user_id"] = attendance.user_id
            date, time  = attendance.timestamp.isoformat().split("T")
            payload["date"] = date
            payload["time"] = time
            payload_json = json.dumps(payload)
            post_req(url, headers, payload_json)
            
            print (attendance)
except Exception as e:
    print ("Process terminate : {}".format(e))








