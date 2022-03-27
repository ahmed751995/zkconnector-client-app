from zk import ZK, const
import requests
import json
import time
import os
import sys

class ZKConnect:
    def __init__(self, ip, port, password):
        self.ip = ip
        self.port = port
        self.password = password
        self.conn = None
        self.close = False
        self.live = False
        self.header = {}

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
        while(self.live):
            time.sleep(.1)
        self.conn.disconnect()

    def is_connected(self):
        return self.conn.is_connect

    def live_capture(self, url, header):
        self.header['Authorization'] = header
        self.live = True

        for attendance in self.conn.live_capture():
            if self.close:
                break

            if attendance:
                print(attendance)
                payload = {}
                payload["user_id"] = attendance.user_id
                date, time = attendance.timestamp.isoformat().split("T")
                payload["date"] = date
                payload["time"] = time
                payload["punch"] = attendance.punch
                payload["status"] = attendance.status
                payload["uid"] = attendance.uid

                payload_json = json.dumps(payload)

                res = post_req(url, self.header, payload_json)
                if res.status_code != 200:
                    write_failed_requests('.failed', payload_json)

        self.live = False


def post_req(url, header, data):
    response = requests.request("POST", url, headers=header, data=data)
    return response


def write_failed_requests(FileName, req_data):
    if not os.path.exists(FileName):
        with open(FileName, 'w') as file:
            file.writelines([])

    with open(FileName, 'a') as file:
        file.write(req_data + '\n')


def read_failed_requests(FileName):
    try:
        with open(FileName) as file:
            data = file.readlines()
        return data

    except FileNotFoundError:
        return None


class AutoSync():
    def __init__(self, t, url, header):
        self.t = t
        self.url = url
        self.header = header
        self.s = False

    def reset_conf(self, t, url, header):
        self.url = url
        self.header = header
        self.t = t

    def stop_sync(self):
        self.s = False
        
    def sync_status(self):
        return self.s
    
    def sync(self):
        self.s = True
        while self.s:
            time.sleep(self.t)
            data = read_failed_requests('.failed')
            if data is not None and len(data) > 0:
                new_data = []
                for d in data:
                    res = post_req(self.url, self.header, d.rstrip())
                    if res.status_code != 200:
                        new_data.append(d)
                with open('.failed', 'w') as file:
                    file.writelines(new_data)
