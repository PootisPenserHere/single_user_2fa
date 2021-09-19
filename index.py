from http.server import BaseHTTPRequestHandler
import os
import base64
import hashlib
import hmac
import time
import struct
import boto3
from datetime import datetime

# Setting up the credentials for twillio
account_sid = os.getenv("TWILLIO_ACCOUND_SID")
auth_token = os.getenv("TWILLIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # A new 2fa code will be generated based on the current timestamp
        tm = int(time.time() / 30)
        secret = base64.b32decode(str(os.getenv("SECRET")).encode())
        b = struct.pack(">q", tm)
        hm = hmac.HMAC(secret, b, hashlib.sha1).digest()
        offset = hm[-1] & 0x0F
        truncated_hash = hm[offset:offset + 4]
        code = struct.unpack(">L", truncated_hash)[0]
        code &= 0x7FFFFFFF;
        code %= 1000000;
        
        # The code is converted to string and padded with zeros to the left
        padded_token = str(code).zfill(6)

        # Sending the code over sms with the aws sns
        sns = boto3.resource(
            'sns',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
            region_name='us-east-1'
        )

        topic = sns.Topic(os.getenv('SNS_TOPIC'))

        topic.publish(
            Message=f"Your 2fa code is: {padded_token}"
        )

        return
