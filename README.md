# Reverse Proxy Automation

## Objectif

L'objectif de ce script était d'automatiser la création de configuration sur mon reverse proxy NGINX pour mes sous-domaines par le biais d'un script **Python** :snake: et une pipeline **.gitlab-ci.yml** 🦊.

Le script *script/new_domain.py* va parcourir les entrées présentes dans le fichier *etc_nginx/.domain.yml* et crée les entrées absentes dans la configurations NGINX et généré un certificat LetsEncrypt :shield:.  

La pipeline n'a que pour but de se connecter au serveur pour effectuer les actions à distance par le biais d'un commit, elle me sert aussi à regénérer mes certificats périodiquement.


## Amélioration

La prochaine étape serais la création automatique d'une entrée CNAME chez mon registrar OVH par le biais de leur API.