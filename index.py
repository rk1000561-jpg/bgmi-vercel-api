from http.server import BaseHTTPRequestHandler
import requests
import json
from urllib.parse import urlparse, parse_qs, unquote


def get_authorization_token():
    session = requests.Session()

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html"
    }

    session.get("https://www.rooter.gg/", headers=headers)

    user_auth = session.cookies.get("user_auth")

    if not user_auth:
        return None, None

    try:
        token = json.loads(unquote(user_auth)).get("accessToken")
        return token, session
    except:
        return None, None


def fetch_bgmi(uid):
    try:
        token, session = get_authorization_token()

        if not token:
            return {
                "status": False,
                "developer": "@R3XTRON",
                "message": "Token fetch failed"
            }

        url = f"https://bazaar.rooter.io/order/getUnipinUsername?gameCode=BGMI_IN&id={uid}"

        headers = {
            "Authorization": f"Bearer {token}",
            "Device-Type": "web",
            "App-Version": "1.0.0",
            "Device-Id": "vercel-api",
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }

        response = session.get(url, headers=headers)
        data = response.json()

        if data.get("transaction") == "SUCCESS":
            return {
                "status": True,
                "developer": "@R3XTRON",
                "username": data["unipinRes"]["username"],
                "uid": uid,
                "server": "BGMI",
                "region": "India"
            }

        return {
            "status": False,
            "developer": "@R3XTRON",
            "message": data.get("message", "UID not found")
        }

    except:
        return {
            "status": False,
            "developer": "@R3XTRON",
            "message": "Request failed"
        }


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        uid = query.get("uid", [None])[0]

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        if not uid:
            self.wfile.write(json.dumps({
                "status": False,
                "message": "UID required"
            }).encode())
            return

        result = fetch_bgmi(uid)
        self.wfile.write(json.dumps(result).encode())        self.send_header("Content-type","application/json")
        self.end_headers()

        if not uid:
            self.wfile.write(json.dumps({"status":"error","msg":"UID required"}).encode())
            return

        self.wfile.write(json.dumps(fetch(uid)).encode())
