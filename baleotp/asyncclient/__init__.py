from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..syncclient import BaleOTP
    
import aiohttp
import json
from typing import Union, Optional

class AsyncBaleOTP:
    def __init__(self, username: str, secret: str):
        self.username = username
        self.secret = secret
    
    def to_sync_client(self):
        return BaleOTP(self.username, self.secret)
    
    async def get_token(self) -> str:
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
        async with aiohttp.ClientSession() as session:
            async with session.post(sign_url, headers=headers, data=body) as response:
                json_data = await response.json()
                return json_data['access_token']
    
    async def send_code(self, number: str, code: Union[str, int]) -> bool:
        try:
            token = await self.get_token()
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
            async with aiohttp.ClientSession() as session:
                async with session.post(send_url, headers=headers, data=json.dumps(body)) as response:
                    json_data = await response.json()
                    if 'balance' in json_data.keys():
                        return True
                    return False
        except BaseException:
            return False