from fastapi import APIRouter, HTTPException

from app.db import supabase
from app.schemas import ProjectCreate

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("")
def create_project(body: ProjectCreate):
    res = supabase.table("projects").insert(body.model_dump()).execute()
    return res.data[0]


@router.get("")
def list_projects():
    return supabase.table("projects").select("*").order("created_at", desc=True).execute().data


@router.get("/{project_id}")
def get_project(project_id: str):
    res = supabase.table("projects").select("*").eq("id", project_id).execute()
    if not res.data:
        raise HTTPException(404, "Project not found")
    return res.data[0]


@router.get("/{project_id}/chats")
def list_chats(project_id: str):
    return (
        supabase.table("chats").select("*")
        .eq("project_id", project_id).order("created_at", desc=True)
        .execute().data
    )
