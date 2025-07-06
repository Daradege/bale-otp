from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..asyncclient import AsyncBaleOTP

import requests
import json
from typing import Union, Optional
from random import randint
from ..helpers import transform_number

class BaleOTP:
    def __init__(self, username: str, secret: str, base_url: str = "https://safir.bale.ai/api/v2/"):
        self.username = username
        self.secret = secret
        self.base_url = base_url
    
    def to_async_client(self):
        return AsyncBaleOTP(self.username, self.secret, self.base_url)

    def get_token(self) -> str:
        sign_url = self.base_url+"auth/token"
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

    def send_code(self, number: str, code: Optional[Union[str, int]] = None) -> bool:
        try:
            if not code:
                otp_code = randint(1000, 99999)
            token = self.get_token()
            send_url = self.base_url+"send_otp"
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "PostmanRuntime/7.43.0",
                "Authorization": f"Bearer {token}"
            }
            body = {
                "phone": transform_number(number),
                "otp": code or otp_code
            }
            response = requests.post(
                send_url, headers=headers, data=json.dumps(body))
            json_data = response.json()
            if 'balance' in json_data.keys():
                return True if code else otp_code
            return False
        except BaseException:
            return False