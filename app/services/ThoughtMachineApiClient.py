from fastapi import HTTPException
from config.config import settings
from pydantic import BaseModel
import certifi
import urllib3
import httpx

# Disable SSL warnings from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Configuration(BaseModel):
    thought_machine_auth_token: str = settings.tm_auth_token
    thought_machine_base_url : str = settings.tm_api_server
    
class ThoughtMachineApiClient:
    def __init__(self, configuration: Configuration):
        self.base_url = configuration.thought_machine_base_url
        self.headers = {
            "X-Auth-Token": configuration.thought_machine_auth_token,
            "Content-Type": "application/json"
        }
    
    async def post(self, body: dict, urls: str):
        url = f"{self.base_url}{urls}"
        async with httpx.AsyncClient(verify=certifi.where()) as client:
            try:
                response = await client.post(url, json=body, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                raise HTTPException(status_code=503, detail=f"Error communicating with Thought Machine API: {e}")