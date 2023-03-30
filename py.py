import base64
import jwt
import hashlib
import requests

from time import time

def create_checksum(http_method, raw_url, headers, request_body):
    string_to_hash = f"{http_method.upper()}|{raw_url.lower()}|{headers}|{request_body}"
    hash_object = hashlib.sha256(str.encode(string_to_hash))
    base64_string = base64.b64encode(hash_object.digest()).decode('utf-8')
    return base64_string

def create_jwt_token(appication_id, api_key, http_method, raw_url, headers, request_body,
                     iat=time(), algorithm='HS256', version='V1'):
    checksum = create_checksum(http_method, raw_url, headers, request_body)
    payload = {'appid': appication_id,
               'iat': iat,
               'version': version,
               'checksum': checksum}
    token = jwt.encode(payload, api_key, algorithm=algorithm)
    return token

# Use this region to setup the call info of the TMCM server (server url, application id, api key)
use_url_base = 'https://seuc7f.manage.trendmicro.com/'
use_application_id = 'D38EF152-A9A5-4966-959C-BEBE220F40B0'
use_api_key = '4DC6C873-945D-40D4-9BA8-B5F4AE5128B1'

# This is the path for ProductAgents API
productAgentAPIPath = '/WebApp/API/AgentResource/ProductAgents'
# currently Canonical-Request-Headers will always be empty
canonicalRequestHeaders = ''

# This sample sends a get request to obtain agent info
useQueryString = '?host_name=DESKTOP-2S4A3NN'
useRequestBody = ''
jwt_token = create_jwt_token(use_application_id, use_api_key, 'GET', productAgentAPIPath + useQueryString, canonicalRequestHeaders, useRequestBody, iat=time())
headers = {'Authorization': 'Bearer ' + jwt_token}
r = requests.get(use_url_base + productAgentAPIPath + useQueryString, headers=headers, data=useRequestBody, verify=False)
print(r.status_code)
print(r.json()['result_code'])
print(r.json()['result_description'])
print(r.json()['result_content'])