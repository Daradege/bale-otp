from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..asyncclient import AsyncBaleOTP

import requests
import json
from typing import Union, Optional

class BaleOTP:
    def __init__(self, username: str, secret: str):
        self.username = username
        self.secret = secret
    
    def to_async_client(self):
        return AsyncBaleOTP(self.username, self.secret)

    def get_token(self) -> str:
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
        json_data = response.json()
        return json_data['access_token']

    def send_code(self, number: str, code: Union[str, int]) -> bool:

        try:
            token = self.get_token()
            send_url = "https://safir.bale.ai/api/v2/send_otp"
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "PostmanRuntime/7.43.0",
                "Authorization": f"Bearer {token}"
            }
            body = {
                "phone": number,
                "otp": code
            }
            response = requests.post(
                send_url, headers=headers, data=json.dumps(body))
            json_data = response.json()

            if 'balance' in json_data.keys():
                return True
            return False
        except BaseException:
            return False