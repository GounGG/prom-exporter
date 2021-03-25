# Usage
```shell
python3 port-check-exporter.py --port 10000
```

# result
```text
# HELP ping_delay network ping delay
# TYPE ping_delay gauge
ping_delay{hostname="ffweb-k8s-client",listen="127.0.0.1",port="6379",port_name="None"} 0.0
ping_delay{hostname="ffweb-k8s-client",listen="127.0.0.1",port="10000",port_name="ndmp"} 0.0
ping_delay{hostname="ffweb-k8s-client",listen="127.0.0.1",port="80",port_name="http"} 0.0
ping_delay{hostname="ffweb-k8s-client",listen="10.88.0.39",port="60020",port_name="None"} 0.0
ping_delay{hostname="ffweb-k8s-client",listen="127.0.0.1",port="8000",port_name="irdmi"} 0.0
ping_delay{hostname="ffweb-k8s-client",listen="127.0.0.1",port="38080",port_name="None"} 0.0
ping_delay{hostname="ffweb-k8s-client",listen="127.0.0.1",port="10050",port_name="zabbix-agent"} 0.0
ping_delay{hostname="ffweb-k8s-client",listen="127.0.0.1",port="36422",port_name="x2-control"} 0.0
ping_delay{hostname="ffweb-k8s-client",listen="10.88.0.39",port="8999",port_name="bctp"} 1.0
ping_delay{hostname="ffweb-k8s-client",listen="127.0.0.1",port="5000",port_name="commplex-main"} 0.0
ping_delay{hostname="ffweb-k8s-client",listen="127.0.0.1",port="8080",port_name="webcache"} 0.0
```
**备注**
- 0 Open
-  1 Close
