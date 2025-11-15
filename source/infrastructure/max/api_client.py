from typing import Optional, Dict, Any, List
from urllib.parse import urlparse

import aiohttp
import httpx
from pydantic import BaseModel


class NewMessageBody(BaseModel):
    text: str
    attachments: Optional[List[Dict]] = None
    format: Optional[str] = "markdown"


class InlineKeyboard(BaseModel):
    type: str = "inline_keyboard"
    payload: Dict


class Button(BaseModel):
    type: str
    text: str
    url: Optional[str] = None
    payload: Optional[str] = None


class MaxBotClient:
    def __init__(self, token: str, base_url: str):
        self.token = token
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _request(self, method: str, endpoint: str, params: Optional[Dict] = None,
                       json_data: Optional[Dict] = None) -> Dict[str, Any]:
        if params is None:
            params = {}
        params['access_token'] = self.token
        async with self.session.request(method, f"{self.base_url}{endpoint}", params=params, json=json_data) as resp:
            return await resp.json()

    async def send_message(self, chat_id: int, body: NewMessageBody, buttons: Optional[List[List[Button]]] = None) -> \
    Dict[str, Any]:
        payload = body.model_dump(exclude_none=True)
        attachments = payload.get("attachments", [])
        if buttons:
            kb_buttons = []
            for btn_row in buttons:
                row = []
                for b in btn_row:
                    try:
                        b_dict = {
                            'type': b.type,
                            'text': b.text,
                        }

                        if b.type == 'link':
                            b_dict['url'] = b.url or ''  # str or ''
                        elif b.type == 'callback':
                            b_dict['payload'] = b.payload or ''  # str or ''

                        b_dict = {k: str(v) for k, v in b_dict.items()}
                        b_dict = {k: v for k, v in b_dict.items() if v != ''}

                        row.append(b_dict)
                    except Exception as e:
                        # print(f"DEBUG button error: {e}, b={b}")
                        row.append({"type": "callback", "text": "Button", "payload": "default"})
                kb_buttons.append(row)

            kb_payload = {"buttons": kb_buttons}
            # print(f"DEBUG send_message: kb_payload = {kb_payload}")

            kb = InlineKeyboard(payload=kb_payload).model_dump(exclude_none=True)
            attachments.append(kb)

        payload["attachments"] = attachments
        # print(f"DEBUG send_message: full payload = {payload}")

        resp = await self._request("POST", "/messages", params={"chat_id": chat_id}, json_data=payload)
        # print(f"DEBUG send_message: API result = {resp}")
        return resp

    async def get_updates(self, marker: Optional[int] = None, timeout: int = 30, limit: int = 100) -> Dict[str, Any]:
        params = {"timeout": timeout, "limit": limit}
        if marker:
            params["marker"] = marker
        return await self._request("GET", "/updates", params=params)

    async def get_upload_url(self, file_type: str) -> Dict[str, Any]:
        return await self._request("POST", "/uploads", params={"type": file_type})

    async def upload_image_from_url(self, image_url: str) -> str:
        try:
            async with httpx.AsyncClient() as http_client:
                resp = await http_client.get(image_url, timeout=10)
                resp.raise_for_status()
                image_bytes = resp.content

            parsed_url = urlparse(image_url)
            extension = parsed_url.path.split('.')[-1].lower() if '.' in parsed_url.path else 'jpg'
            content_type = f'image/{extension}'
            filename = f'image.{extension}'

            upload_url = await self.get_upload_url("image")
            photo_ids = upload_url.get('photoIds')
            form = aiohttp.FormData()
            form.add_field('data', image_bytes, filename=filename, content_type=content_type)
            async with self.session.post(upload_url['url'], data=form) as resp:
                result = await resp.json()

                token = ''
                if 'photos' in result and isinstance(result['photos'], dict):
                    photo_key = list(result['photos'].keys())[0] if result['photos'] else None
                    if photo_key and 'token' in result['photos'][photo_key]:
                        token = result['photos'][photo_key]['token']

                return token
        except Exception as e:
            print(f"DEBUG upload_image: error = {e}")
            return ''

    async def upload_file(self, upload_url: Dict[str, Any], file_path: str) -> str:
        form = aiohttp.FormData()
        form.add_field('data', open(file_path, 'rb'), filename='file')
        async with self.session.post(upload_url['url'], data=form) as resp:
            result = await resp.json()
            return result.get('token', '')
