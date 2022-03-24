from zk import ZK, const
import requests, json
import PySimpleGUI as sg


# url = "http://103.136.40.46:72/api/resource/zkaccess"

# zk = ZK('192.168.1.201', port=4370, timeout=5, password=0, force_udp=True, ommit_ping=False)
# headers = {
#   'Authorization': 'token fdc04965d6f8c41:1044dbe6947eff3',
#   'Cookie': 'full_name=Guest; sid=Guest; system_user=no; user_id=Guest; user_image='
# }



def make_connection(ip, port, password):
    try:
        zk = ZK(ip, port, timeout=5, password=password, force_udp=True, ommit_ping=False)
        conn = zk.connect()
        return conn
    except:
        raise Exception("can't connect")


def post_req(url, headers, data):
    response = requests.request("POST", url, headers=headers, data=data)
    return response


def live_capture(url, headers, conn):
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
            payload["punch"] = attendance.punch
            pyload["status"] = attendance.status
            payload["uid"] = attendance.uid
            
            payload_json = json.dumps(payload)
            post_req(url, headers, payload_json)



