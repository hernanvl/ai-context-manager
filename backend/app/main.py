from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.routers import chats, projects

app = FastAPI(title="AI Context Manager")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.exception_handler(Exception)
async def show_errors(request: Request, exc: Exception):
    # Dev helper: return the real error instead of a bare 500
    return JSONResponse(status_code=500, content={"error": type(exc).__name__, "detail": str(exc)})


app.include_router(projects.router)
app.include_router(chats.router)


@app.get("/health")
def health():
    return {"status": "ok"}
