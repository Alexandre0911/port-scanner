import socket
import threading
from queue import Queue



target = str(input('IP Address: ')).lower()
if target == 'localhost':
    target = '192.168.1.1'
else:
    target = target

queue = Queue()
open_ports = []



print('''\nScan Types:
[1] Simple Scan     ->      Port 1 to Port 1024)
[2] Advanced Scan   ->      Port 1 to Port 65536''')

ScanType = int(input('\nScan Type (1 or 2): '))
portnumber = 0
if ScanType == 1:
    portnumber = 1024
elif ScanType == 2:
    portnumber = 65536


def portscan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        return True
    except:
        return False

def fill_queue(port_list):
    for port in port_list:
        queue.put(port)

def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            print('Port {} is open!'.format(port))
            open_ports.append(port)



port_list = range(1, portnumber)
fill_queue(port_list)

thread_list = []

print('\nNumber of Threads To Use: ', end='')
tn = int(input(''))



for t in range(tn):
    thread = threading.Thread(target=worker)
    thread_list.append(thread)

for thread in thread_list:
    thread.start()

for thread in thread_list:
    thread.join()



print('Open ports are: {}'.format(open_ports))



with open('ports.txt', 'w+') as file:
    if target not in file.read():
        file.write('Ports Opened in {} >>>>> {}'.format(target, open_ports))
    else:
        print('The IP Address \033[34m{}\033[m was already scanned.')
    file.close()