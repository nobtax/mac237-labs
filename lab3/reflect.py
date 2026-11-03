import http.server, urllib.parse, html, sys
SAFE = len(sys.argv) > 1 and sys.argv[1] == 'safe'
class Handler(http.server.BaseHTTPRequestHandler):
   def do_GET(self):
      query = urllib.parse.urlparse(self.path).query
      name = urllib.parse.parse_qs(query).get('name', [''])[0]
      shown = html.escape(name) if SAFE else name
      body = ('<!doctype html><title>lab</title><p>Hello, '
            + shown + '</p>').encode()
      self.send_response(200)
      self.send_header('Content-Type', 'text/html; charset=utf-8')
      self.send_header('Content-Length', str(len(body)))
      self.end_headers()
      self.wfile.write(body)
   def log_message(self, *a): pass
print(('safe' if SAFE else 'vulnerable') + ' page on http://127.0.0.1:8238/')
http.server.HTTPServer(('127.0.0.1', 8238), Handler).serve_forever()
