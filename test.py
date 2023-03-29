import base64
from venv import create
import jwt
import hashlib
import time
import json

def create_checksum(http_method, raw_url, headers, request_body):
    string_to_hash = http_method.upper() + '|' + raw_url.lower() + '|' + headers + '|' + request_body    
    base64_string = base64.b64encode(hashlib.sha256(str.encode(string_to_hash)).digest()).decode('utf-8')
    return base64_string    
    
def create_jwt_token(appication_id, api_key, http_method, raw_url, headers, request_body,
                     iat=time.time(), algorithm='HS256', version='V1'):
    checksum = create_checksum(http_method, raw_url, headers, request_body)
    print("CHECKSUM = ", checksum);
    payload = {'appid': appication_id,
               'iat': iat,
               'version': version,
               'checksum': checksum}
    token = jwt.encode(payload, api_key, algorithm=algorithm)
    print("TOKEN_CHECKSUM = ", token);
    

    return token

# Use this region to setup the call info of the TMCM server (server url, application id, api key)
use_url_base = 'https://trahtb.manage.trendmicro.com'
use_application_id = '7E49640B-85C5-4501-B8BB-C99AA02F997C'
use_api_key = 'D51C6142-EA1B-4DB6-8AD2-5471DA90209D'

# This is the path for ProductAgents API
productAgentAPIPath = '/WebApp/API/AgentResource/ProductAgents'
# currently Canonical-Request-Headers will always be empty
canonicalRequestHeaders = ''

# This sample sends a get request to obtain agent info
useQueryString = '?host_name=DESKTOP-C4OKDLK'
useRequestBody = ''
jwt_token = create_jwt_token(use_application_id, use_api_key, 'GET',
                              productAgentAPIPath + useQueryString,
                              canonicalRequestHeaders, useRequestBody, iat=time.time())