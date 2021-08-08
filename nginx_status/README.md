# Open nginx status
```bash
server {
    listen 9008 default_server;
    # Define the document root of the server e.g /var/www/html
    root /var/www/html;

    location /nginx_status {
        # Enable Nginx stats
        stub_status on;
        # Only allow access from your IP e.g 1.1.1.1 or localhost #
        allow 127.0.0.1;
        allow 101.231.115.150;
        # Other request should be denied
        deny all;
    }
}
```

# start exporter
```bash
/usr/bin/python3.6 /data/scripts/nginx-status-exporter.py
```

# Import grafana dashboard
