#!/bin/bash
read -p 'Domaine: ' domain
echo "Nous allons créer le certificat pour le domaine suivant: $domain"
nginx -t && systemctl stop nginx.service
certbot certonly --standalone --agree-tos --no-eff-email -d $domain --rsa-key-size 4096
systemctl start nginx.service
systemctl status nginx.service
