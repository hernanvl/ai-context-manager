"""Request/response models."""
from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None


class ChatCreate(BaseModel):
    project_id: str
    title: str = "New chat"


class MessageIn(BaseModel):
    content: str


class ChatReply(BaseModel):
    chat_id: str
    user_message_id: str
    assistant_message_id: str
    reply: str
