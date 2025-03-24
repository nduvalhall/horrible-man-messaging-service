from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

import socketio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)


class Message(BaseModel):
    user: str
    timestamp: datetime
    message: str


messages: list[Message] = []


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")


@app.get("/messages")
async def get_messages() -> list[Message]:
    return messages


@app.post("/messages")
async def send_message(message: Message):
    messages.append(message)


sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode="asgi")
app = socketio.ASGIApp(sio, app)


@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.send(sid, "Welcome to the Socket.IO server!")


@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")


@sio.event
async def message(sid, data):
    print(f"Message from {sid}: {data}")
    await sio.emit("response", {"data": f"Received your message: {data}"})
