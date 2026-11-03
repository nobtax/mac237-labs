import http.server, sys
PORT = int(sys.argv[1])
ALLOW = sys.argv[2] if len(sys.argv) > 2 else None
BODY = ('served by 127.0.0.1:%d' % PORT).encode()
class Handler(http.server.BaseHTTPRequestHandler):
   def do_GET(self):
      self.send_response(200)
      self.send_header('Content-Type', 'text/plain')
      if ALLOW:
         self.send_header('Access-Control-Allow-Origin', ALLOW)
      self.send_header('Content-Length', str(len(BODY)))
      self.end_headers()
      self.wfile.write(BODY)
   def log_message(self, *a): pass
print('origin http://127.0.0.1:%d allow-origin=%s' % (PORT, ALLOW))
http.server.HTTPServer(('127.0.0.1', PORT), Handler).serve_forever()
