from http.server import BaseHTTPRequestHandler
import requests, json
from urllib.parse import urlparse, parse_qs, unquote

def fetch(uid):
    try:
        s = requests.Session()
        r = s.get("https://www.rooter.gg/", headers={"User-Agent":"Mozilla/5.0"})
        token = json.loads(unquote(s.cookies.get("user_auth"))).get("accessToken")

        url = f"https://bazaar.rooter.io/order/getUnipinUsername?gameCode=BGMI_IN&id={uid}"
        res = s.get(url, headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": "Mozilla/5.0"
        }).json()

        if res.get("transaction") == "SUCCESS":
            return {
                "status":"success",
                "username": res["unipinRes"]["username"],
                "uid": uid,
                "server":"BGMI"
            }

        return {"status":"error","msg":"failed"}

    except:
        return {"status":"error","msg":"error"}


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        q = parse_qs(urlparse(self.path).query)
        uid = q.get("uid",[None])[0]

        self.send_response(200)
        self.send_header("Content-type","application/json")
        self.end_headers()

        if not uid:
            self.wfile.write(json.dumps({"status":"error","msg":"UID required"}).encode())
            return

        self.wfile.write(json.dumps(fetch(uid)).encode())
