from http.server import BaseHTTPRequestHandler
from dotenv import load_dotenv
import os

# Loading the env properties into the system
load_dotenv(".env")

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(str(os.getenv("PHONE")).encode())
        return
