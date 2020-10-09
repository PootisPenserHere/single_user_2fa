from http.server import BaseHTTPRequestHandler
from twilio.rest import Client
import os
import base64
import hashlib
import hmac
import time
import struct
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

        # A custom message to be sent, this is mostly for aesthetic the code alone
        # can also be sent
        sms_message = f"Your 2fa code is: {padded_token}"

        # Sending the code over sms with the Twillio api
        message = client.messages \
            .create(
            body=sms_message,
            from_=os.getenv("FROM_NUMBER"),
            to=os.getenv("TO_NUMBER")
        )

        # Checking that the message was sent
        if message.error_code is None:
            response = "The code has been sent at %s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(str(response).encode())
        else:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(str("An error ocurred while attempting to send the sms.").encode())

        return
