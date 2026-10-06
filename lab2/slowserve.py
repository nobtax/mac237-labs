import http.server, sys, time
class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        time.sleep(0.3) # stands in for one database query
        body = b'ok\n'
        self.send_response(200)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *a): pass

class Single(http.server.HTTPServer):
    request_queue_size = 64

class Threaded(http.server.ThreadingHTTPServer):
    request_queue_size = 64

mode = sys.argv[1] if len(sys.argv) > 1 else 'single'
srv = (Threaded if mode == 'threaded' else Single)(('127.0.0.1', 8237), Handler)
print(mode, 'server listening on 127.0.0.1:8237, Ctrl-C to stop')
srv.serve_forever()
