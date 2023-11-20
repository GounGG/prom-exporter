#!/usr/bin/env python3

import os
from datetime import datetime

import prometheus_client
from OpenSSL import crypto
from flask import Flask, Response
from prometheus_client import CollectorRegistry, CONTENT_TYPE_LATEST
from prometheus_client import Gauge

app = Flask(__name__)

# 定义一个仓库
REGISTRY = CollectorRegistry(auto_describe=False)


class CertValidity():
    kube_cert_validity_period = Gauge(
        'kube_cert_validity_period', 'ceet validity period', ['filename'], registry=REGISTRY)

    def get_certificate_expiry_date(self, cert_path):
        with open(cert_path, 'rt') as f:
            cert_data = f.read()
        cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_data)
        expiry_date = cert.get_notAfter().decode('utf-8')
        dt = datetime.strptime(expiry_date, "%Y%m%d%H%M%SZ")
        timestamp = dt.timestamp()
        return timestamp

    def filter(self):
        for filename in os.listdir(kube_pki_path):
            if filename.endswith('.crt'):
                self.kube_cert_validity_period.labels(filename).set(
                    self.get_certificate_expiry_date(cert_path="{}/{}".format(kube_pki_path, filename)))


@app.route("/metrics")
def cert_validity_period():
    CertValidity().filter()
    return Response(prometheus_client.generate_latest(registry=REGISTRY), mimetype=CONTENT_TYPE_LATEST)


if __name__ == '__main__':
    kube_pki_path = os.getenv('kube_pki_path', "/etc/kubernetes/pki")
    app.run(host="0.0.0.0", port=11601)
