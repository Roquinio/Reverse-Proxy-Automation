#import pyyaml
import yaml
import subprocess
import ovh
import json

############ Variables Globales ############ 

DOMAIN_LIST_PATH='/srv/reverse-proxy/etc_nginx/.domain.yml'
TEMPLATE_PATH='/srv/reverse-proxy/etc_nginx/domain.j2'




def check_domain(FULL_DOMAIN):

    CMD_CHECK_CONF="ls /etc/nginx/conf.d/"+FULL_DOMAIN+".conf > /dev/null 2>&1"
    CMD_CHECK_SSL="ls /etc/letsencrypt/live/"+FULL_DOMAIN+"/fullchain.pem > /dev/null 2>&1"


    SUBPROCESS_CONF=subprocess.Popen(CMD_CHECK_CONF,shell=True)
    SUBPROCESS_SSL=subprocess.Popen(CMD_CHECK_SSL,shell=True)


    SUBPROCESS_CONF.wait()
    SUBPROCESS_SSL.wait()

    RETURN_CODE = SUBPROCESS_CONF.poll() + SUBPROCESS_SSL.poll() 
    #print(RETURN_CODE)
    
    if RETURN_CODE != 0:
        print(FULL_DOMAIN,"is not hosted :(")
        return 'NOK'

    
    else:
        print(FULL_DOMAIN,"is already hosted :)")
        return 'OK'


#def new_ovh_domain(FULL_DOMAIN,SUBDOMAIN):
    
#     CMD_CHECK_OVH="nslookup "+FULL_DOMAIN+" > /dev/null 2>&1"
    
#     SUBPROCESS_OVH=subprocess.Popen(CMD_CHECK_OVH,shell=True)
#     SUBPROCESS_OVH.wait()

#     RETURN_CODE = SUBPROCESS_OVH.poll()

#     if RETURN_CODE != 0:
#         print(FULL_DOMAIN,"is not on OVH :(")
#         client = ovh.Client(endpoint='ovh-eu', application_key='', application_secret='', consumer_key='',)
#         result = client.post('/domain/zone/baptisteroques.fr/record', fieldType='CNAME', subDomain=SUBDOMAIN, target='baptisteroques.fr.', ttl=60,)
#         update = client.post('/domain/zone/baptisteroques.fr/refresh')

#     else:
#         print(FULL_DOMAIN,"is already on OVH :)")

    


def new_domain(FULL_DOMAIN,URL,SUBDOMAIN):

    CMD_TEMPLATE_COPY='sudo cp /srv/reverse-proxy/etc_nginx/domain.j2 /etc/nginx/conf.d/'+FULL_DOMAIN+'.conf'
    CMD_TEMPLATE_REPLACE_SUB="sudo sed -i 's%{{ subdomain }}%"+SUBDOMAIN+"%g' /etc/nginx/conf.d/"+FULL_DOMAIN+".conf"
    CMD_TEMPLATE_REPLACE_URL="sudo sed -i 's%{{ url }}%"+URL+"%g' /etc/nginx/conf.d/"+FULL_DOMAIN+".conf"
    CMD_NEW_CERT="sudo systemctl stop nginx.service && sudo certbot certonly --standalone --agree-tos --no-eff-email -d "+FULL_DOMAIN+" --rsa-key-size 4096 > /dev/null 2>&1 ; sudo systemctl start nginx.service"

    SUBPROCESS_COPY=subprocess.Popen(CMD_TEMPLATE_COPY,shell=True)
    SUBPROCESS_COPY.wait()
    SUBPROCESS_SUB=subprocess.Popen(CMD_TEMPLATE_REPLACE_SUB,shell=True)
    SUBPROCESS_URL=subprocess.Popen(CMD_TEMPLATE_REPLACE_URL,shell=True)
    SUBPROCESS_CERT=subprocess.Popen(CMD_NEW_CERT,shell=True)


def main():
    
    with open(DOMAIN_LIST_PATH) as DOMAIN_LIST:
        DATA_DOMAIN = yaml.safe_load(DOMAIN_LIST)
        subdomains=list(DATA_DOMAIN.keys())

        for i in DATA_DOMAIN.keys():
            
            FULL_DOMAIN=(DATA_DOMAIN[i][0]["domain"])
            URL=(DATA_DOMAIN[i][1]["url"])
            SUBDOMAIN=i
            
            if check_domain(FULL_DOMAIN) == 'NOK':
                #new_ovh_domain(FULL_DOMAIN,SUBDOMAIN)
                new_domain(FULL_DOMAIN,URL,SUBDOMAIN)
                print("New domain hosted: ",FULL_DOMAIN)



            


if __name__ == '__main__':
    main()
