import asyncio
from typing import Optional

from fastapi.datastructures import UploadFile
from channel_spammer import Spammer
from fastapi import FastAPI, File
from pydantic import BaseModel


app = FastAPI()


class TelegramData(BaseModel):
    api_id: int
    api_hash: str
    session_name: str
    folders: list
    photo: Optional[bytes]
    text: str


def init_event_loop():
    # necessary for running inner async functions like in Spammer
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)


@app.get("/")
def read_root():
    return {"msg": "Hello!"}


@app.post("/file/")
def upload_file(file: bytes = File(...)):
    pass


@app.post("/spam/")
def run_spammer(data: TelegramData):
    init_event_loop()
    spammer = Spammer(data.session_name, data.api_id, data.api_hash, data.folders)
    spammer.run(b"rr", data.text)
    return {"channels_succeed": spammer.channels_succeed, "channels_fails": spammer.channels_fails}
