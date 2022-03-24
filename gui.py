import PySimpleGUI as sg
import time
from app import make_connection, post_req, live_capture


def window_1():
    layout = [[sg.Text("Enter the number of zk devices")],
              [sg.Input(k="n", size=(10))],
              [sg.Submit(), sg.Cancel()]]

    window = sg.Window('ZK Connector', layout)
    while True:
        event, value = window.read()
        if event == "Submit":
            try:
                n = int(value["n"])
                window.close()
                return n
            except ValueError:
                sg.SystemTray.notify('Error', 'Enter a Valid number')
        else:
            break    
    window.close()
    
def create_gui():
    rows = window_1()
    layout = [[sg.Text("URL"), sg.InputText(k='url'),sg.Text("Header") ,sg.InputText(k='header')],
              [sg.Text("IP", size=(45,1)), sg.Text("PORT", size=(45,1)), sg.Text("PASSWORD", size=(45,1))]]
    connections = {}
    for r in range(rows):
        row = [sg.InputText(k='ip'+str(r)), sg.InputText(k='port'+str(r)), sg.InputText(k='pass'+str(r)),\
               sg.Button("Connect", k=str(r)), sg.Button("Disconnect", k='d'+str(r))]
        layout.append(row)
    
    window = sg.Window("ZK Connector", layout)
    while True:
        event, value = window.read()

        if  event == sg.WIN_CLOSED:
            break
        
        elif len(event) == 1:
            try:
                ip = value['ip'+event]
                port = int(value['port'+event])
                password = int(value['pass'+event])
                connections[event] = make_connection(ip, port, password)
                
            except:
                sg.SystemTray.notify('Error', 'make sure your input is correct')


        elif 'd' in event:
            if event[-1] in connections.keys() and connections[event[-1]].is_connect:
                connections[event[-1]].disconnect()
                sg.SystemTray.notify('Success', 'Device disconnected successfully')
            else:
                sg.SystemTray.notify('Error', 'Device not connected or data is wrong')

            
        print(event, value)

    window.close()










if __name__ == "__main__":
    create_gui()
