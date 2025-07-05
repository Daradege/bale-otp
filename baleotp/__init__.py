import requests
import json
from typing import Union, Optional

class Client:
    def __init__(self, username: str, secret: str):
        self.username = username
        self.secret = secret

    
    def send(self, number: str, code: Union[str, int]) -> bool:
        try:
            sign_url = "http://safir.bale.ai/api/v2/auth/token"
            headers = {
                            "Content-Type": "application/x-www-form-urlencoded",
                            "User-Agent": "PostmanRuntime/7.43.0"
                        }
            body = {
                            "grant_type": "client_credentials",
                            "client_secret": self.secret,
                            "scope": "read",
                            "client_id": self.username
                        }
            response = requests.post(sign_url, headers=headers, data=body)
            sign_r = response.json()
            token = sign_r['access_token']
            send_url = "https://safir.bale.ai/api/v2/send_otp"
            headers = {
                            "Content-Type": "application/x-www-form-urlencoded",
                            "User-Agent": "PostmanRuntime/7.43.0",
                            "Authorization": f"Bearer {token}"
                        }
            body ={
                            "phone": number,
                            "otp": code
                        }
            response = requests.post(send_url, headers=headers, data=json.dumps(body))
            send_r = response.json()
            if 'balance' in send_r.keys():
                return True
            return False
        except:
            return False