from fastapi import APIRouter, HTTPException

from app.config import RECENT_MESSAGES, SYSTEM_PROMPT
from app.db import supabase
from app.schemas import ChatCreate, ChatReply, MessageIn
from app.services.llm import chat_completion
from app.services.tokens import count_tokens

router = APIRouter(prefix="/chats", tags=["chats"])


def _save_message(chat_id: str, role: str, content: str) -> str:
    row = {
        "chat_id": chat_id,
        "role": role,
        "content": content,
        "token_count": count_tokens(content),
    }
    return supabase.table("messages").insert(row).execute().data[0]["id"]


@router.post("")
def create_chat(body: ChatCreate):
    return supabase.table("chats").insert(body.model_dump()).execute().data[0]


@router.get("/{chat_id}/messages")
def get_messages(chat_id: str):
    return (
        supabase.table("messages").select("id, role, content, token_count, created_at")
        .eq("chat_id", chat_id).order("created_at")
        .execute().data
    )


@router.post("/{chat_id}/messages", response_model=ChatReply)
def send_message(chat_id: str, body: MessageIn):
    chat = supabase.table("chats").select("id").eq("id", chat_id).execute().data
    if not chat:
        raise HTTPException(404, "Chat not found")

    # 1. Save the user message
    user_id = _save_message(chat_id, "user", body.content)

    # 2. Load recent history (short-term memory)
    history = (
        supabase.table("messages").select("role, content")
        .eq("chat_id", chat_id).order("created_at", desc=True)
        .limit(RECENT_MESSAGES).execute().data
    )
    history.reverse()

    # 3. Ask the LLM  (Phase 5 will inject the Context Pack + retrieved snippets here)
    prompt = [{"role": "system", "content": SYSTEM_PROMPT}] + history
    reply = chat_completion(prompt)

    # 4. Save the assistant reply
    assistant_id = _save_message(chat_id, "assistant", reply)

    return ChatReply(
        chat_id=chat_id,
        user_message_id=user_id,
        assistant_message_id=assistant_id,
        reply=reply,
    )
