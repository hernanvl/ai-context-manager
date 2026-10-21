# Backend (FastAPI)

## Run locally (Windows PowerShell)
```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open http://localhost:8000/docs to try the API.

## Endpoints (Phase 2)
| Method | Path | What |
|---|---|---|
| POST | /projects | Create project |
| GET | /projects | List projects |
| GET | /projects/{id}/chats | List chats of a project |
| POST | /chats | Create chat |
| GET | /chats/{id}/messages | Chat history |
| POST | /chats/{id}/messages | Send message, get AI reply (both saved) |
