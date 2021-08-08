# coding:utf-8

import argparse
import json
import time, datetime

from ping3 import ping
import subprocess

import prometheus_client
from flask import Flask, Response
from prometheus_client import Gauge
from prometheus_client.core import CollectorRegistry

app = Flask(__name__)

# 定义一个仓库
REGISTRY = CollectorRegistry(auto_describe=False)


class STATUS():
    # 延迟
    PingDelay = Gauge('ping_delay', 'network ping delay', ['zone', 'ip', 'desc'], registry=REGISTRY)

    # 丢包(0 不丢 1 丢)
    PingLoss = Gauge('ping_loss', 'network ping delay', ['zone', 'ip', 'desc'], registry=REGISTRY)

    def __init__(self):
        self.ip = args.ip
        self.zone = args.zone
        self.desc = args.desc

    def mtr(self, ip):
        s, r = subprocess.getstatusoutput("mtr -c 4 --report {0}".format(ip))
        if int(s) == 0:
            with open('mtr-{0}-{1}.txt'.format(ip, datetime.datetime.now().strftime(r'%Y%m%d%H%M%S')), 'a+') as f:
                f.write(r)

    def filter(self):
        res = ping(self.ip, timeout=3, unit='ms', size=56)
        if res == None:
            self.PingLoss.labels(self.zone, self.ip, self.desc).set_function(
            lambda: 1)

            self.mtr(self.ip)

        elif isinstance(res, float):
            self.PingLoss.labels(self.zone, self.ip, self.desc).set_function(
            lambda: 0)
            self.PingDelay.labels(self.zone, self.ip, self.desc).set_function(
            lambda: res)


@app.route("/metrics")
def Status():
    STATUS().filter()
    return Response(prometheus_client.generate_latest(registry=REGISTRY), mimetype="text/plain")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description = 'Get CLB traffic information'
    parser.add_argument("--zone", help="web event name", required=True, type=str)
    parser.add_argument("--ip", help="public ip", required=True, type=str)
    parser.add_argument("--desc", help="dest describe", required=True, type=str)
    parser.add_argument("--port", help="exporter port", required=True, type=int)
    args = parser.parse_args()

    app.run(host="0.0.0.0", port=args.port)