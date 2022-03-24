from zk import ZK, const
import requests
import json
import time


# url = "http://103.136.40.46:72/api/resource/zkaccess"

# zk = ZK('192.168.1.201', port=4370, timeout=5, password=0, force_udp=True, ommit_ping=False)
# headers = {
#   'Authorization': 'token fdc04965d6f8c41:1044dbe6947eff3',
#   'Cookie': 'full_name=Guest; sid=Guest; system_user=no; user_id=Guest; user_image='
# }

class ZKConnect:
    def __init__(self, ip, port, password):
        self.ip = ip
        self.port = port
        self.password = password
        self.conn = None
        self.close = False
        self.live = False

    def set_default(self):
        self.ip = '192.168.1.201'
        self.port = 4370
        self.password = 0
        print("default setted")

    def make_connection(self):
        try:
            zk = ZK(
                self.ip,
                self.port,
                timeout=5,
                password=self.password,
                force_udp=True,
                ommit_ping=False)
            self.conn = zk.connect()
            self.close = False

        except BaseException:
            raise Exception("can't connect")

    def kill_connection(self):
        self.close = True
        time.sleep(2)
        # while(self.live):
        #     pass
        self.conn.disconnect()

    def is_connected(self):
        return self.conn.is_connect

    def live_capture(self, url, headers):
        print("here")
        self.live = True
        for attendance in self.conn.live_capture():
            print("live cappture started", url)
            if self.close:
                print("live capture closed")
                break

            if attendance:
                print(attendance)
                # payload = {}
                # payload["user_id"] = attendance.user_id
                # date, time  = attendance.timestamp.isoformat().split("T")
                # payload["date"] = date
                # payload["time"] = time
                # payload["punch"] = attendance.punch
                # pyload["status"] = attendance.status
                # payload["uid"] = attendance.uid

                # payload_json = json.dumps(payload)
                # post_req(url, headers, payload_json)
        self.live = False


def post_req(url, headers, data):
    response = requests.request("POST", url, headers=headers, data=data)
    return response
