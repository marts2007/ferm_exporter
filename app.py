import socket

import json
import requests
import fcntl, os
import time
from flask import Flask, escape, request

app = Flask(__name__)

@app.route('/claymore/<hostname>/<int:port>')
def claymore(hostname, port):
    HOST = escape(hostname)
    PORT = port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        fcntl.fcntl(s, fcntl.F_SETFL, os.O_NONBLOCK)
        s.sendall(b'{"id":0,"jsonrpc":"2.0","method":"miner_getstat2"}\n')
        data=bytearray()
        time.sleep(0.1)
        while True:
            try:
              tmp=s.recv(1)
              if len(tmp)==0: break;
              data.extend(tmp)
            except socket.error as e:
                break
    result = json.loads(data)
    if 'result' in result:
        result = result['result']
        hashrates = (result[3]).split(';')
        power_usage = result[-1]
        power_usage2 = result[1]
        t_arr = result[6].split(';')
        temps = []
        fans = []
        for x in range(0, (len(t_arr) // 2)):
            temps.append(t_arr[x * 2])
            fans.append(t_arr[x * 2 + 1])
        metrics = ''
        #metrics = 'ferm_monitor_power_usage %s\n' % power_usage
        #metrics = metrics+'ferm_monitor_power_usage2 %s\n' % power_usage2
        for gpu in range(0,len(temps)):
            metrics = metrics+'ferm_monitor_temp{sensor="gpu%(id)s"} %(temp)s\n' % dict(id=gpu,temp=temps[gpu])
            metrics = metrics + 'ferm_monitor_fan{sensor="gpu%(id)s"} %(temp)s\n' % dict(id=gpu, temp=fans[gpu])
            metrics = metrics + 'ferm_monitor_hashrate{sensor="gpu%(id)s"} %(temp)s\n' % dict(id=gpu, temp=hashrates[gpu])
    return metrics

@app.route('/gminer/<hostname>/<int:port>')
def gminer(hostname, port):
    HOST = escape(hostname)
    PORT = port
    data = requests.get("http://{}:{}/stat".format(HOST,PORT))
    result = json.loads(data.text)
    if 'devices' in result:
        temps = []
        fans = []
        metrics = ''
        power_usage = 0
        devices = result['devices']
        for device in devices:
            power_usage = power_usage + device['power_usage']
            metrics = metrics+'ferm_monitor_temp{sensor="gpu%(id)s"} %(temp)s\n' % dict(id=device['gpu_id'], temp=device['temperature'])
            metrics = metrics+'ferm_monitor_hashrate{sensor="gpu%(id)s"} %(hashrate)s\n' % dict(id=device['gpu_id'], hashrate=device['speed']/1000)
        metrics = metrics+'ferm_monitor_power_usage %s\n' % power_usage
    return metrics

@app.route('/nanominer/<hostname>/<int:port>')
def nanominer(hostname, port):
    HOST = escape(hostname)
    PORT = port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        fcntl.fcntl(s, fcntl.F_SETFL, os.O_NONBLOCK)
        s.sendall(b'{"id":0,"jsonrpc":"2.0","method":"miner_getstat2"}\n')
        data=bytearray()
        time.sleep(0.1)
        while True:
            try:
              tmp=s.recv(1)
              if len(tmp)==0: break;
              data.extend(tmp)
            except socket.error as e:
                break
    result = json.loads(data)
    if 'result' in result:
        result = result['result']
        hashrates = (result[3]).split(';')
        power_usage = result[-1]
        power_usage=0
        power_usage2 = result[1]
        t_arr = result[6].split(';')
        temps = []
        fans = []
        for x in range(0, (len(t_arr) // 2)):
            temps.append(t_arr[x * 2])
            fans.append(t_arr[x * 2 + 1])
        metrics = ''
        #metrics = 'ferm_monitor_power_usage %s\n' % power_usage
        #metrics = metrics+'ferm_monitor_power_usage2 %s\n' % power_usage2
        for gpu in range(0,len(temps)):
            metrics = metrics+'ferm_monitor_temp{sensor="gpu%(id)s"} %(temp)s\n' % dict(id=gpu,temp=temps[gpu])
            metrics = metrics + 'ferm_monitor_fan{sensor="gpu%(id)s"} %(temp)s\n' % dict(id=gpu, temp=fans[gpu])
            metrics = metrics + 'ferm_monitor_hashrate{sensor="gpu%(id)s"} %(temp)s\n' % dict(id=gpu, temp=hashrates[gpu])
        return metrics;


@app.route('/nanominerrvn/<hostname>/<int:port>')
def nanominerrvn(hostname, port):
    HOST = escape(hostname)
    PORT = port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        fcntl.fcntl(s, fcntl.F_SETFL, os.O_NONBLOCK)
        s.sendall(b'{"id":0,"jsonrpc":"2.0","method":"miner_getstat2"}\n')
        data=bytearray()
        time.sleep(0.1)
        while True:
            try:
              tmp=s.recv(1)
              if len(tmp)==0: break;
              data.extend(tmp)
            except socket.error as e:
                break
    result = json.loads(data)
    if 'result' in result:
        result = result['result']
        hashrates = (result[3]).split(';')
        t_arr = result[6].split(';')
        temps = []
        fans = []
        for x in range(0, (len(t_arr) // 2)):
            temps.append(t_arr[x * 2])
            fans.append(t_arr[x * 2 + 1])
        metrics = ''
        for gpu in range(0,len(temps)):
            metrics = metrics+'ferm_monitor_temp{sensor="gpu%(id)s"} %(temp)s\n' % dict(id=gpu,temp=temps[gpu])
            metrics = metrics + 'ferm_monitor_fan{sensor="gpu%(id)s"} %(temp)s\n' % dict(id=gpu, temp=fans[gpu])
            metrics = metrics + 'ferm_monitor_hashrate{sensor="gpu%(id)s"} %(temp)s\n' % dict(id=gpu, temp=(float(hashrates[gpu])/1000))
        return metrics;

@app.route('/teamredminer/<hostname>/<int:port>')
def teamredminer(hostname,port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((hostname, port))
        fcntl.fcntl(s, fcntl.F_SETFL, os.O_NONBLOCK)
        s.sendall(b'{"id":0,"jsonrpc":"2.0","command":"devs"}\n')
        data=bytearray()
        time.sleep(1)
        while True:
            try:
              tmp=s.recv(1)
              if len(tmp)==0: break;
              data.extend(tmp)
            except socket.error as e:
              break
    result = json.loads(data)
    if 'DEVS' in result:
        devices = result['DEVS'];
        temps = []
        fans = []
        metrics = ''
        power_usage = 0
        for device in devices:
            metrics = metrics + 'ferm_monitor_temp{sensor="gpu%(id)s"} %(temp)s\n' % dict(
                id=device['GPU'], temp=device['Temperature'])
            metrics = metrics + 'ferm_monitor_hashrate{sensor="gpu%(id)s"} %(hashrate)s\n' % dict(
                id=device['GPU'], hashrate=device['KHS 30s'])
        metrics = metrics + 'ferm_monitor_power_usage %s\n' % power_usage
    return metrics



@app.route('/trex/<hostname>/<int:port>')
def trex(hostname, port):
    HOST = escape(hostname)
    PORT = port
    data = requests.get("http://{}:{}/summary".format(HOST,PORT))
    result = json.loads(data.text)
    if 'gpus' in result:
        temps = []
        fans = []
        metrics = ''
        power_usage = 0
        devices = result['gpus']
        for device in devices:
            power_usage = power_usage + device['power']
            metrics = metrics+'ferm_monitor_temp{sensor="gpu%(id)s"} %(temp)s\n' % dict(id=device['gpu_id'], temp=device['temperature'])
            metrics = metrics+'ferm_monitor_hashrate{sensor="gpu%(id)s"} %(hashrate)s\n' % dict(id=device['gpu_id'], hashrate=device['hashrate_minute']/1000)
            metrics = metrics + 'ferm_monitor_fan{sensor="gpu%(id)s"} %(temp)s\n' % dict(id=device['gpu_id'], temp=device['fan_speed'])
            
        metrics = metrics+'ferm_monitor_power_usage %s\n' % power_usage
    return metrics


@app.route('/miniz/<hostname>/<int:port>')
def miniz(hostname, port):
    HOST = escape(hostname)
    PORT = port
    data = requests.get("http://{}:{}/miner_getstat".format(HOST, PORT))
    result = json.loads(data.text)
    if 'result' in result:
        temps = []
        fans = []
        metrics = ''
        power_usage = 0
        devices = result['result']
        for device in devices:
            power_usage = power_usage + device['gpu_power_usage']
            metrics = metrics + 'ferm_monitor_temp{sensor="gpu%(id)s"} %(temp)s\n' % dict(id=device['gpuid'],
                                                                                          temp=device['temperature'])
            metrics = metrics + 'ferm_monitor_hashrate{sensor="gpu%(id)s"} %(hashrate)s\n' % dict(id=device['gpuid'],
                                                                                                  hashrate=device[
                                                                                                               'speed_sps'] )
            metrics = metrics + 'ferm_monitor_fan{sensor="gpu%(id)s"} %(temp)s\n' % dict(id=device['gpuid'],
                                                                                         temp=device['gpu_fan_speed'])

        metrics = metrics + 'ferm_monitor_power_usage %s\n' % power_usage
    return metrics

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=os.environ.get("API_PORT",5000))
