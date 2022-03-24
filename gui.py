import PySimpleGUI as sg
import time
from app import ZKConnect
from threading import Thread

def window_1_gui():
    '''
    create window that takes number of zk devices
    '''
    
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
    

def write_data(rows, value, FileName):
    '''
    write data to file .data, create new file if the file doesn't exist
    rows: number of rows for ip and port lines
    value: the gui values
    FileName: the name of the file that will be created
    '''
    data = []
    data.append(value['url']+'\n')
    data.append(value['header'] + '\n')
    for r in range(rows):
        line = value[f'ip{r}'] + ' ' + value[f'port{r}'] + ' ' + value[f'pass{r}'] +'\n'
        data.append(line)
        
    with open(FileName, 'w') as file:
        file.writelines(data)


def read_data(FileName):
    '''
    reading data from {FileName} file and prepare them
    to be displayed in devices gui
    FileName: the name of the file that will be read
    '''
    with open(FileName) as file:
        data = file.readlines()
    value = {}
    value['url'] = data[0].rstrip()
    value['header'] = data[1].rstrip()
    i = 0
    for line in data[2:]:
        d = line.rstrip().split()
        print(d)
        if len(d) == 3:
            value[f'ip{i}'], value[f'port{i}'], value[f'pass{i}'] = d
            i += 1

    return value

        
def devices_gui(rows):
    '''
    create gui for url and header and devices to connect to
    '''
    try:
        value = read_data('.data')
    except FileNotFoundError:
        pass
    
    layout = [[sg.Text("URL"), sg.InputText(value.get('url'), k='url'),sg.Text("Header") ,sg.InputText(value.get('header'), k='header')],
              [sg.Text("IP", size=(45,1)), sg.Text("PORT", size=(45,1)), sg.Text("PASSWORD", size=(45,1))]]

    connections = {}
    
    for r in range(rows):
        row = [sg.InputText(value.get(f'ip{r}'), k=f'ip{r}'), sg.InputText(value.get(f'port{r}'), k=f'port{r}'),\
               sg.InputText(value.get(f'pass{r}'), k=f'pass{r}'), sg.Button("Connect", k=str(r)),\
               sg.Button("Disconnect", k=f'd{r}')]
        layout.append(row)
        
    window = sg.Window("ZK Connector", layout, resizable=True, finalize=True, enable_close_attempted_event=True)
    while True:
        event, value = window.read()

        if  event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT:
            if sg.popup_yes_no('Do you want to save your changes') == 'Yes':
                write_data(rows, value, '.data')
            break
        if len(event) == 1:
            try:
                ip = value[f'ip{event}']
                port = int(value[f'port{event}'])
                password = int(value[f'pass{event}'])

                connections[event] = ZKConnect(ip, port, password)
                connections[event].set_default()
                connections[event].make_connection()
                Thread(target=connections[event].live_capture, args=(ip, value['header'])).start()
                if(connections[event].is_connected()):
                    sg.SystemTray.notify('Success', 'Device connected successfully')

            except:
                sg.SystemTray.notify('Error', 'make sure your input is correct')


        elif 'd' in event:
            if event[-1] in connections.keys() and connections[event[-1]].is_connected():
                connections[event[-1]].kill_connection()
                sg.SystemTray.notify('Success', 'Device disconnected successfully')
            else:
                sg.SystemTray.notify('Error', 'Device not connected or data is wrong')


    window.close()




def create_gui():
    rows = window_1_gui()
    devices_gui(rows)


    
if __name__ == "__main__":
    create_gui()
