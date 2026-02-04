import requests
import jwt
import http.server
import time
import threading
import json


SOLVE_URL = 'https://hackattic.com/challenges/jotting_jwts/solve?access_token=9099aaae9c650db1'


class MyHandler(http.server.BaseHTTPRequestHandler):
    jwt_secret = ""
    append = ""
    def do_POST(self):
        print("Request incoming...")
        content_len = int(self.headers.get('Content-Length', 0))
        token = self.rfile.read(content_len).decode()
        print("Token:", token)
        
        try:
            payload = jwt.decode(token, key=self.jwt_secret, algorithms=["HS256"])
            print("Payload:", payload)
            if "append" not in payload:
                solution = json.dumps({"solution": MyHandler.append}).encode()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(solution)))
                self.end_headers()
                self.wfile.write(solution)
                print("Solution sent:", MyHandler.append)
                return

            MyHandler.append += payload['append']
            self.send_response(200)
            self.end_headers()
        except (jwt.InvalidSignatureError, jwt.InvalidTokenError):

            self.send_response(200)
            self.end_headers()




def trigger_requests():
    time.sleep(1)
    response = requests.get('https://hackattic.com/challenges/jotting_jwts/problem?access_token=9099aaae9c650db1')
    MyHandler.jwt_secret = response.json()['jwt_secret']    
    print("JWT secret:", MyHandler.jwt_secret)
    address = 'https://modern-dingos-allow.loca.lt'
    app_url = { 'app_url' : address }
    requests.post(SOLVE_URL, json=app_url)


def main():
    threading.Thread(target=trigger_requests, daemon=True).start()

    server_address = ('0.0.0.0', 8080)
    httpd = http.server.HTTPServer(server_address, MyHandler)
    httpd.serve_forever()


main()
