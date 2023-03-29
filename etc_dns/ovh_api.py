# -*- encoding: utf-8 -*-
import json
import ovh

# Instanciate an OVH Client.
# You can generate new credentials with full access to your account on
# the token creation page
client = ovh.Client(
    endpoint='ovh-eu',               # Endpoint of API OVH Europe (List of available endpoints)
    application_key='secret',    # Application Key
    application_secret='secret', # Application Secret
    consumer_key='secret',       # Consumer Key
)

result = client.post('/domain/zone/baptisteroques.fr/record', 
    fieldType='CNAME',
    subDomain='api', 
    target='baptisteroques.fr.', 
    ttl=60, 
)

update = client.post('/domain/zone/baptisteroques.fr/refresh')

# Pretty print
print(result)
print(update)