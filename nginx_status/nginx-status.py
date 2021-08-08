# coding:utf-8

import re
import socket

import prometheus_client
import requests
from flask import Response, Flask
from prometheus_client import Gauge
from prometheus_client.core import CollectorRegistry

app = Flask(__name__)

# 定义一个仓库
REGISTRY = CollectorRegistry(auto_describe=False)


# 获取本机IP
def MyIP():
    hostname = socket.getfqdn(socket.gethostname())
    IP = socket.gethostbyname(hostname)
    return IP


class STATUS():
    # 活跃连接数
    active_connections = Gauge('active_connections', 'Active connections', ['HostIP'], registry=REGISTRY)

    # 接收的请求数
    accept_connections = Gauge('accept_connections', 'Accect requests', ['HostIP'], registry=REGISTRY)

    # 处理的请求数
    handled_connections = Gauge('handled_connections', 'handled requests', ['HostIP'], registry=REGISTRY)

    # 总请求数
    total_requests = Gauge('total_requests', 'total requests', ['HostIP'], registry=REGISTRY)

    # 获取请求体的连接数
    read_request_headers_connections = Gauge('read_request_headers_connections', 'read request headers connections',
                                             ['HostIP'], registry=REGISTRY)
    # 响应客户端的连接数
    respones_client_connections = Gauge('respones_client_connections', 'respones client connections', ['HostIP'],
                                        registry=REGISTRY)

    # 等待的连接数
    wait_connections = Gauge('wait_connections', 'waiting connections', ['HostIP'], registry=REGISTRY)

    def __init__(self, hostip):
        self.hostip = hostip
        self.get_info()

    def run(self):
        self.filter()

    def get_info(self):
        url = 'http://127.0.0.1/nginx_status'
        self.r = requests.get(url=url, timeout=30)
        self.info = self.r.text

    def filter(self):
        res = self.info

        self.active_connections.labels(self.hostip).set_function(
            lambda: re.search('Active connections: ([0-9]+)', res).group(1))

        self.accept_connections.labels(self.hostip).set_function(
            lambda: re.search('([0-9]+) ([0-9]+) ([0-9]+)', res).group(1))

        self.handled_connections.labels(self.hostip).set_function(
            lambda: re.search('([0-9]+) ([0-9]+) ([0-9]+)', res).group(2))

        self.total_requests.labels(self.hostip).set_function(
            lambda: re.search('([0-9]+) ([0-9]+) ([0-9]+)', res).group(3))

        self.read_request_headers_connections.labels(self.hostip).set_function(
            lambda: re.search('Reading: ([0-9]+)', res).group(1))

        self.respones_client_connections.labels(self.hostip).set_function(
            lambda: re.search('Writing: ([0-9]+)', res).group(1))

        self.wait_connections.labels(self.hostip).set_function(
            lambda: re.search('Waiting: ([0-9]+)', res).group(1))

    def __del__(self):
        self.r.close()


@app.route("/metrics")
def Status():
    STATUS(hostip=MyIP()).run()
    return Response(prometheus_client.generate_latest(registry=REGISTRY), mimetype="text/plain")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9999)
