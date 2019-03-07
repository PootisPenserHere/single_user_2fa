from http.server import BaseHTTPRequestHandler
from dotenv import load_dotenv
import os
import base64
import hashlib
import hmac
import time
import struct

# Loading the env properties into the system
load_dotenv(".env")


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        tm = int(time.time() / 30)
        secret = base64.b32decode(str(os.getenv("SECRET")).encode())
        b = struct.pack(">q", tm)
        hm = hmac.HMAC(secret, b, hashlib.sha1).digest()
        offset = hm[-1] & 0x0F
        truncatedHash = hm[offset:offset + 4]
        code = struct.unpack(">L", truncatedHash)[0]
        code &= 0x7FFFFFFF;
        code %= 1000000;

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(str(code).encode())
        return
