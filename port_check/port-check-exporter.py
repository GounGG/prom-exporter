#!/usr/bin/env python3
# coding:utf-8

import argparse
import os
import re
import socket
import subprocess

import prometheus_client
from flask import Flask, Response
from prometheus_client import Gauge
from prometheus_client.core import CollectorRegistry

app = Flask(__name__)

# 定义一个仓库
REGISTRY = CollectorRegistry(auto_describe=False)

class STATUS():
    # Port check
    PortStatus = Gauge('port_status', 'Port check', ['listen', 'port', 'port_name', 'hostname'],
                       registry=REGISTRY)

    def __init__(self):
        self.hostname = socket.gethostname()

    def scan(self):
        cmd = "ss -ntlp"
        ret = subprocess.getoutput(cmd)
        ports = []

        for line in ret.splitlines():
            listen_info = {}
            if line.startswith('LISTEN'):
                host_port = line.split()[3]
                if re.match('[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', host_port) and re.match('0.0.0.0', host_port) == None:
                    host = host_port.split(':')[0]
                else:
                    host = '127.0.0.1'

                port = host_port.split(':')[-1]
                listen_info['host'] = host
                listen_info['port'] = port
                try:
                    # 获取进程名
                    listen_info['port_name'] = re.search('users:\(\((.*)\)', line).group(1).split(",")[0].strip('\"')
                except Exception as e:
                    pass
                ports.append(listen_info)

        return ports

    def filter(self):
        if os.path.isfile('data.json') == False or os.path.getsize('data.json') == 0:
            with open('data.json', 'w') as f:
                f.write(str(self.scan()))
            for listen_info in self.scan():
                if listen_info.get('port_name'):
                    self.PortStatus.labels(listen_info['host'], listen_info['port'], listen_info['port_name'],
                                           self.hostname).set_function(lambda: 0)
                else:
                    self.PortStatus.labels(listen_info['host'], listen_info['port'], None, self.hostname).set_function(
                        lambda: 0)
        else:
            with open('data.json', 'r+') as f:
                data = f.read()
            for data_port in eval(data):
                for listen_info in self.scan():
                    if int(data_port['port']) != int(listen_info['port']):
                        if data_port.get('port_name'):
                            self.PortStatus.labels(data_port['host'], data_port['port'],
                                                   data_port['port_name'], self.hostname).set_function(lambda: 1)
                        else:
                            self.PortStatus.labels(data_port['host'], data_port['port'], None,
                                                   self.hostname).set_function(lambda: 1)

                    else:
                        if data_port.get('port_name'):
                            self.PortStatus.labels(data_port['host'], data_port['port'],
                                                   data_port['port_name'], self.hostname).set_function(lambda: 0)
                        else:
                            self.PortStatus.labels(data_port['host'], data_port['port'], None,
                                                   self.hostname).set_function(lambda: 0)
                        break

        with open('data.json', 'w+') as f:
            f.write(str(self.scan()))



@app.route("/metrics")
def Status():
    STATUS().filter()
    return Response(prometheus_client.generate_latest(registry=REGISTRY), mimetype="text/plain")




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description = 'Get CLB traffic information'
    parser.add_argument("--port", help="exporter port", required=True, type=int)
    args = parser.parse_args()

    app.run(host="0.0.0.0", port=args.port)
