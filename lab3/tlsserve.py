import http.server, ssl, secrets
SID = secrets.token_hex(16)
class Handler(http.server.BaseHTTPRequestHandler):
   def do_GET(self):
     body = b'session page\n'
     self.send_response(200)
     self.send_header('Content-Type', 'text/plain')
     self.send_header('Set-Cookie',
                 f'sid={SID}; HttpOnly; Secure; SameSite=Lax; Path=/')
     self.send_header('Content-Length', str(len(body)))
     self.end_headers()
     self.wfile.write(body)
   def log_message(self, *a): pass
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain('lab.crt', 'lab.key')
srv = http.server.HTTPServer(('127.0.0.1', 8443), Handler)
srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
print('https on 127.0.0.1:8443, Ctrl-C to stop')
srv.serve_forever()
