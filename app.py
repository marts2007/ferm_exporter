import socket

import json
from flask import Flask, escape, request

app = Flask(__name__)

@app.route('/claymore/<hostname>/<int:port>')
def claymore(hostname,port):
    HOST=escape(hostname)
    PORT=port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'{"id":0,"jsonrpc":"2.0","method":"miner_getstat2"}\n')
        data = s.recv(2048)

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
        metrics='ferm_monitor_power_usage %s\n' % power_usage
        metrics=metrics+'ferm_monitor_power_usage2 %s\n' % power_usage2
        for gpu in range(0,len(temps)):
            metrics=metrics+'ferm_monitor_temp{sensor="gpu%(id)s"} %(temp)s\n' % dict(id=gpu,temp=temps[gpu])
            metrics = metrics + 'ferm_monitor_fan{sensor="gpu%(id)s"} %(temp)s\n' % dict(id=gpu, temp=fans[gpu])
            metrics = metrics + 'ferm_monitor_hashrate{sensor="gpu%(id)s"} %(temp)s\n' % dict(id=gpu, temp=hashrates[gpu])
    return metrics






if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
