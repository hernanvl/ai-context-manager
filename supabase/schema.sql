-- AI Context Manager - Phase 1 schema
-- Run in Supabase: SQL Editor -> New query -> paste -> Run

create extension if not exists vector;

-- Projects --------------------------------------------------------------
create table if not exists projects (
    id          uuid primary key default gen_random_uuid(),
    user_id     uuid references auth.users(id) on delete cascade,
    name        text not null,
    description text,
    created_at  timestamptz not null default now()
);

-- Chats -----------------------------------------------------------------
create table if not exists chats (
    id          uuid primary key default gen_random_uuid(),
    project_id  uuid not null references projects(id) on delete cascade,
    title       text not null default 'New chat',
    created_at  timestamptz not null default now()
);

-- Messages (embedding stored inline, 384 dims = all-MiniLM-L6-v2) ------
create table if not exists messages (
    id           uuid primary key default gen_random_uuid(),
    chat_id      uuid not null references chats(id) on delete cascade,
    role         text not null check (role in ('user', 'assistant', 'system')),
    content      text not null,
    token_count  int  not null default 0,
    summarized   boolean not null default false,
    embedding    vector(384),
    created_at   timestamptz not null default now()
);

-- Summaries -------------------------------------------------------------
create table if not exists summaries (
    id            uuid primary key default gen_random_uuid(),
    project_id    uuid not null references projects(id) on delete cascade,
    chat_id       uuid references chats(id) on delete set null,
    summary_type  text not null check (summary_type in ('chat', 'rolling', 'project')),
    content       jsonb not null,   -- {goals, decisions, facts, constraints, open_tasks, tech_notes}
    embedding     vector(384),
    created_at    timestamptz not null default now()
);

-- Context Packs (versioned project state) --------------------------------
create table if not exists context_packs (
    id          uuid primary key default gen_random_uuid(),
    project_id  uuid not null references projects(id) on delete cascade,
    version     int  not null,
    content     jsonb not null,
    markdown    text not null,
    created_at  timestamptz not null default now(),
    unique (project_id, version)
);

-- Indexes ---------------------------------------------------------------
create index if not exists idx_chats_project    on chats(project_id);
create index if not exists idx_messages_chat    on messages(chat_id, created_at);
create index if not exists idx_summaries_proj   on summaries(project_id);
create index if not exists idx_packs_proj       on context_packs(project_id, version desc);
create index if not exists idx_messages_emb  on messages  using hnsw (embedding vector_cosine_ops);
create index if not exists idx_summaries_emb on summaries using hnsw (embedding vector_cosine_ops);

-- Similarity search over messages + summaries of one project ------------
create or replace function match_context(
    query_embedding vector(384),
    p_project_id    uuid,
    match_count     int default 5
)
returns table (source_type text, source_id uuid, content text, similarity float)
language sql stable as $$
    (
      select 'message', m.id, m.content, 1 - (m.embedding <=> query_embedding)
      from messages m join chats c on c.id = m.chat_id
      where c.project_id = p_project_id and m.embedding is not null
    )
    union all
    (
      select 'summary', s.id, s.content::text, 1 - (s.embedding <=> query_embedding)
      from summaries s
      where s.project_id = p_project_id and s.embedding is not null
    )
    order by 4 desc
    limit match_count;
$$;

-- Row Level Security ----------------------------------------------------
-- Blocks direct access via anon/authenticated keys.
-- The FastAPI backend uses the service_role key, which bypasses RLS.
alter table projects      enable row level security;
alter table chats         enable row level security;
alter table messages      enable row level security;
alter table summaries     enable row level security;
alter table context_packs enable row level security;
