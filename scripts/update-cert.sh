#!/bin/bash

nginx -t && systemctl stop nginx && certbot renew --no-random-sleep-on-renew
nginx -t && systemctl start nginx
systemctl status nginx
