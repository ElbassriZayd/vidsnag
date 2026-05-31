-- VidSnag community message wall
create table if not exists public.messages (
  id bigint generated always as identity primary key,
  name text not null check (char_length(trim(name)) between 1 and 24),
  body text not null check (char_length(trim(body)) between 1 and 200),
  is_supporter boolean not null default false,
  is_hidden boolean not null default false,
  created_at timestamptz not null default now()
);

alter table public.messages enable row level security;

-- anyone may READ messages that aren't hidden
create policy "read visible messages" on public.messages
  for select using (is_hidden = false);

-- anyone may POST, but cannot self-grant the supporter badge or hide
create policy "anyone can post" on public.messages
  for insert with check (is_supporter = false and is_hidden = false);

create index if not exists messages_created_idx on public.messages (created_at desc);
