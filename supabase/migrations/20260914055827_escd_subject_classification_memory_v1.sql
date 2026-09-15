
create table if not exists dcse_cp.escd_subjects (
  id uuid primary key default gen_random_uuid(),
  subject_key text not null unique,
  canonical_name text not null,
  subject_type text not null default 'other'
    check (subject_type in ('product','project','topic','person','process','system','vendor','client','other')),
  lane text not null default 'DCSE',
  summary text,
  status text not null default 'active'
    check (status in ('active','superseded','archived')),
  aliases text[] not null default '{}'::text[],
  metadata jsonb not null default '{}'::jsonb
    check (jsonb_typeof(metadata)='object'),
  created_by_user_id uuid not null default auth.uid(),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists dcse_cp.escd_subject_links (
  id uuid primary key default gen_random_uuid(),
  subject_id uuid not null references dcse_cp.escd_subjects(id) on delete restrict,
  object_type text not null
    check (object_type in (
      'conversation','conversation_turn','operation_turn','item','knowledge',
      'asset','ddna','project','decision','file','other'
    )),
  object_ref text not null,
  relation_type text not null default 'RELATED'
    check (relation_type in (
      'PRIMARY','ABOUT','PRODUCED','INPUT','EVIDENCE','DEPENDS_ON',
      'SUPERSEDES','RELATED'
    )),
  confidence numeric(5,4) not null default 1.0
    check (confidence >= 0 and confidence <= 1),
  provenance jsonb not null default '{}'::jsonb
    check (jsonb_typeof(provenance)='object'),
  created_by_user_id uuid not null default auth.uid(),
  created_at timestamptz not null default now(),
  unique(subject_id, object_type, object_ref, relation_type)
);

create table if not exists dcse_cp.escd_turn_classifications (
  id uuid primary key default gen_random_uuid(),
  conversation_turn_id uuid not null unique
    references dcse_cp.conversation_turns(id) on delete restrict,
  operation_turn_id uuid
    references dcse_cp.escd_operation_turns(id) on delete set null,
  primary_category text not null
    check (primary_category in (
      'CHAT_ONLY','TASK','IDEA','KNOWLEDGE','ASSET','DDNA','DECISION','PROJECT'
    )),
  secondary_categories text[] not null default '{}'::text[],
  disposition text not null default 'CANDIDATE'
    check (disposition in ('CANDIDATE','MATERIALIZED','HOLD','REJECTED','SUPERSEDED')),
  normalized_intent text not null,
  confidence numeric(5,4) not null default 0
    check (confidence >= 0 and confidence <= 1),
  rationale text,
  candidate_payload jsonb not null default '{}'::jsonb
    check (jsonb_typeof(candidate_payload)='object'),
  materialized_object_type text,
  materialized_object_ref text,
  created_by_user_id uuid not null default auth.uid(),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists dcse_cp.escd_knowledge_records (
  id uuid primary key default gen_random_uuid(),
  knowledge_key text not null unique,
  title text not null,
  content text not null,
  authority_classification text not null default 'DERIVED'
    check (authority_classification in (
      'OBSERVED','VERIFIED','LIKELY','UNKNOWN','DCS_DIRECTION','DERIVED'
    )),
  confidence numeric(5,4) not null default 0.5
    check (confidence >= 0 and confidence <= 1),
  status text not null default 'staged'
    check (status in ('staged','active','superseded','archived')),
  source_turn_id uuid references dcse_cp.conversation_turns(id) on delete set null,
  source_operation_turn_id uuid references dcse_cp.escd_operation_turns(id) on delete set null,
  subject_id uuid references dcse_cp.escd_subjects(id) on delete set null,
  supersedes_id uuid references dcse_cp.escd_knowledge_records(id) on delete set null,
  evidence_refs jsonb not null default '[]'::jsonb
    check (jsonb_typeof(evidence_refs)='array'),
  provenance jsonb not null default '{}'::jsonb
    check (jsonb_typeof(provenance)='object'),
  created_by_user_id uuid not null default auth.uid(),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists idx_escd_subjects_name
  on dcse_cp.escd_subjects(lower(canonical_name));
create index if not exists idx_escd_subject_links_object
  on dcse_cp.escd_subject_links(object_type, object_ref);
create index if not exists idx_escd_turn_classifications_category
  on dcse_cp.escd_turn_classifications(primary_category, disposition, created_at desc);
create index if not exists idx_escd_knowledge_records_subject
  on dcse_cp.escd_knowledge_records(subject_id, updated_at desc);
create index if not exists idx_escd_knowledge_records_status
  on dcse_cp.escd_knowledge_records(status, updated_at desc);

drop trigger if exists trg_escd_subjects_updated_at on dcse_cp.escd_subjects;
create trigger trg_escd_subjects_updated_at
before update on dcse_cp.escd_subjects
for each row execute function dcse_cp.touch_updated_at();

drop trigger if exists trg_escd_turn_classifications_updated_at on dcse_cp.escd_turn_classifications;
create trigger trg_escd_turn_classifications_updated_at
before update on dcse_cp.escd_turn_classifications
for each row execute function dcse_cp.touch_updated_at();

drop trigger if exists trg_escd_knowledge_records_updated_at on dcse_cp.escd_knowledge_records;
create trigger trg_escd_knowledge_records_updated_at
before update on dcse_cp.escd_knowledge_records
for each row execute function dcse_cp.touch_updated_at();

alter table dcse_cp.escd_subjects enable row level security;
alter table dcse_cp.escd_subject_links enable row level security;
alter table dcse_cp.escd_turn_classifications enable row level security;
alter table dcse_cp.escd_knowledge_records enable row level security;

drop policy if exists escd_subjects_owner_rw on dcse_cp.escd_subjects;
create policy escd_subjects_owner_rw on dcse_cp.escd_subjects
for all to authenticated
using (dcse_cp.is_dcs_owner() and created_by_user_id = auth.uid())
with check (dcse_cp.is_dcs_owner() and created_by_user_id = auth.uid());

drop policy if exists escd_subject_links_owner_rw on dcse_cp.escd_subject_links;
create policy escd_subject_links_owner_rw on dcse_cp.escd_subject_links
for all to authenticated
using (
  dcse_cp.is_dcs_owner()
  and exists (
    select 1 from dcse_cp.escd_subjects s
    where s.id=subject_id and s.created_by_user_id=auth.uid()
  )
)
with check (
  dcse_cp.is_dcs_owner()
  and created_by_user_id=auth.uid()
  and exists (
    select 1 from dcse_cp.escd_subjects s
    where s.id=subject_id and s.created_by_user_id=auth.uid()
  )
);

drop policy if exists escd_turn_classifications_owner_rw on dcse_cp.escd_turn_classifications;
create policy escd_turn_classifications_owner_rw on dcse_cp.escd_turn_classifications
for all to authenticated
using (
  dcse_cp.is_dcs_owner()
  and created_by_user_id=auth.uid()
)
with check (
  dcse_cp.is_dcs_owner()
  and created_by_user_id=auth.uid()
);

drop policy if exists escd_knowledge_records_owner_rw on dcse_cp.escd_knowledge_records;
create policy escd_knowledge_records_owner_rw on dcse_cp.escd_knowledge_records
for all to authenticated
using (dcse_cp.is_dcs_owner() and created_by_user_id=auth.uid())
with check (dcse_cp.is_dcs_owner() and created_by_user_id=auth.uid());

revoke all on dcse_cp.escd_subjects from anon, authenticated;
grant select,insert,update on dcse_cp.escd_subjects to authenticated;
grant all on dcse_cp.escd_subjects to service_role;

revoke all on dcse_cp.escd_subject_links from anon, authenticated;
grant select,insert,update on dcse_cp.escd_subject_links to authenticated;
grant all on dcse_cp.escd_subject_links to service_role;

revoke all on dcse_cp.escd_turn_classifications from anon, authenticated;
grant select,insert,update on dcse_cp.escd_turn_classifications to authenticated;
grant all on dcse_cp.escd_turn_classifications to service_role;

revoke all on dcse_cp.escd_knowledge_records from anon, authenticated;
grant select,insert,update on dcse_cp.escd_knowledge_records to authenticated;
grant all on dcse_cp.escd_knowledge_records to service_role;

create or replace function dcse_cp.escd_append_conversation_turn(
  p_conversation_id uuid,
  p_actor_label text,
  p_actor_role text,
  p_summary text,
  p_metadata jsonb default '{}'::jsonb
)
returns dcse_cp.conversation_turns
language plpgsql
security definer
set search_path to 'pg_catalog','dcse_cp'
as $$
declare
  v_next integer;
  v_row dcse_cp.conversation_turns;
begin
  if auth.role() <> 'service_role' and not dcse_cp.is_dcs_owner() then
    raise exception 'dcs_owner_required';
  end if;

  if not exists (
    select 1 from dcse_cp.conversations c
    where c.id=p_conversation_id
      and (auth.role()='service_role' or c.created_by=auth.uid() or c.created_by is null)
  ) then
    raise exception 'conversation_not_accessible';
  end if;

  perform 1 from dcse_cp.conversations where id=p_conversation_id for update;

  select coalesce(max(turn_index),0)+1
    into v_next
  from dcse_cp.conversation_turns
  where conversation_id=p_conversation_id;

  insert into dcse_cp.conversation_turns(
    conversation_id,turn_index,actor_label,actor_role,summary,metadata
  ) values (
    p_conversation_id,v_next,
    coalesce(nullif(btrim(p_actor_label),''),'ESCD'),
    nullif(btrim(p_actor_role),''),
    p_summary,
    coalesce(p_metadata,'{}'::jsonb)
  )
  returning * into v_row;

  update dcse_cp.conversations
  set updated_at=now()
  where id=p_conversation_id;

  return v_row;
end;
$$;

revoke all on function dcse_cp.escd_append_conversation_turn(uuid,text,text,text,jsonb)
from public,anon;
grant execute on function dcse_cp.escd_append_conversation_turn(uuid,text,text,text,jsonb)
to authenticated,service_role;

create or replace function dcse_cp.escd_resolve_subjects(
  p_text text,
  p_limit integer default 10
)
returns table(
  id uuid,
  subject_key text,
  canonical_name text,
  subject_type text,
  lane text,
  confidence numeric
)
language sql
security definer
set search_path to 'pg_catalog','dcse_cp'
as $$
  select
    s.id,s.subject_key,s.canonical_name,s.subject_type,s.lane,
    case
      when lower(coalesce(p_text,'')) = lower(s.canonical_name) then 1.0::numeric
      when lower(coalesce(p_text,'')) like '%'||lower(s.canonical_name)||'%' then 0.98::numeric
      when exists (
        select 1 from unnest(s.aliases) a
        where lower(coalesce(p_text,'')) like '%'||lower(a)||'%'
      ) then 0.95::numeric
      else 0.0::numeric
    end as confidence
  from dcse_cp.escd_subjects s
  where s.status='active'
    and (
      lower(coalesce(p_text,'')) like '%'||lower(s.canonical_name)||'%'
      or exists (
        select 1 from unnest(s.aliases) a
        where lower(coalesce(p_text,'')) like '%'||lower(a)||'%'
      )
    )
    and (auth.role()='service_role' or (dcse_cp.is_dcs_owner() and s.created_by_user_id=auth.uid()))
  order by confidence desc,s.canonical_name
  limit greatest(1,least(coalesce(p_limit,10),50));
$$;

revoke all on function dcse_cp.escd_resolve_subjects(text,integer) from public,anon;
grant execute on function dcse_cp.escd_resolve_subjects(text,integer) to authenticated,service_role;

create or replace function dcse_cp.escd_materialize_classification(
  p_classification_id uuid,
  p_force boolean default false
)
returns jsonb
language plpgsql
security definer
set search_path to 'pg_catalog','dcse_cp'
as $$
declare
  c dcse_cp.escd_turn_classifications;
  t dcse_cp.conversation_turns;
  v_title text;
  v_ref text;
  v_id uuid;
  v_subject uuid;
begin
  select * into c from dcse_cp.escd_turn_classifications where id=p_classification_id;
  if not found then raise exception 'classification_not_found'; end if;

  if auth.role()<>'service_role' and (not dcse_cp.is_dcs_owner() or c.created_by_user_id<>auth.uid()) then
    raise exception 'classification_not_accessible';
  end if;

  if c.disposition='MATERIALIZED' then
    return jsonb_build_object(
      'classification_id',c.id,
      'object_type',c.materialized_object_type,
      'object_ref',c.materialized_object_ref,
      'already_materialized',true
    );
  end if;

  if c.confidence < 0.85 and not p_force then
    raise exception 'classification_confidence_below_materialization_threshold';
  end if;

  select * into t from dcse_cp.conversation_turns where id=c.conversation_turn_id;
  if not found then raise exception 'source_turn_not_found'; end if;

  v_title := coalesce(
    nullif(c.candidate_payload->>'title',''),
    left(regexp_replace(t.summary,'\s+',' ','g'),120)
  );

  select sl.subject_id into v_subject
  from dcse_cp.escd_subject_links sl
  where sl.object_type='conversation_turn'
    and sl.object_ref=t.id::text
    and sl.relation_type in ('PRIMARY','ABOUT')
  order by case when sl.relation_type='PRIMARY' then 0 else 1 end, sl.confidence desc
  limit 1;

  if c.primary_category in ('TASK','IDEA') then
    insert into dcse_cp.escd_items(
      item_key,title,summary,status,task_class,context,actionable,
      source_system,source_id,normalized_intent,source_refs,evidence_refs,
      created_by_user_id
    ) values (
      'ESCD-'||c.primary_category||'-'||upper(substr(replace(c.id::text,'-',''),1,12)),
      v_title,
      t.summary,
      'captured',
      case when c.primary_category='TASK' then 'DO' else 'CAPTURE' end,
      lower(c.primary_category),
      c.primary_category='TASK',
      'ESCD_CONVERSATION',
      t.id::text,
      c.normalized_intent,
      jsonb_build_array(jsonb_build_object(
        'type','conversation_turn',
        'id',t.id::text,
        'conversation_id',t.conversation_id::text
      )),
      '[]'::jsonb,
      c.created_by_user_id
    )
    returning id into v_id;

    v_ref := v_id::text;

    if v_subject is not null then
      insert into dcse_cp.escd_subject_links(
        subject_id,object_type,object_ref,relation_type,confidence,provenance,created_by_user_id
      ) values (
        v_subject,'item',v_ref,'PRODUCED',c.confidence,
        jsonb_build_object('classification_id',c.id::text),
        c.created_by_user_id
      )
      on conflict do nothing;
    end if;

    update dcse_cp.escd_turn_classifications
    set disposition='MATERIALIZED',
        materialized_object_type=lower(c.primary_category),
        materialized_object_ref=v_ref
    where id=c.id;

    return jsonb_build_object('classification_id',c.id,'object_type',lower(c.primary_category),'object_ref',v_ref);
  end if;

  if c.primary_category='KNOWLEDGE' then
    insert into dcse_cp.escd_knowledge_records(
      knowledge_key,title,content,authority_classification,confidence,status,
      source_turn_id,source_operation_turn_id,subject_id,evidence_refs,provenance,
      created_by_user_id
    ) values (
      'KN-'||upper(substr(replace(c.id::text,'-',''),1,12)),
      v_title,
      coalesce(nullif(c.candidate_payload->>'content',''),t.summary),
      coalesce(nullif(c.candidate_payload->>'authority_classification',''),'DERIVED'),
      c.confidence,
      'staged',
      t.id,
      c.operation_turn_id,
      v_subject,
      coalesce(c.candidate_payload->'evidence_refs','[]'::jsonb),
      jsonb_build_object(
        'classification_id',c.id::text,
        'conversation_id',t.conversation_id::text,
        'turn_index',t.turn_index
      ),
      c.created_by_user_id
    )
    returning id into v_id;

    v_ref := v_id::text;

    if v_subject is not null then
      insert into dcse_cp.escd_subject_links(
        subject_id,object_type,object_ref,relation_type,confidence,provenance,created_by_user_id
      ) values (
        v_subject,'knowledge',v_ref,'PRODUCED',c.confidence,
        jsonb_build_object('classification_id',c.id::text),
        c.created_by_user_id
      )
      on conflict do nothing;
    end if;

    update dcse_cp.escd_turn_classifications
    set disposition='MATERIALIZED',
        materialized_object_type='knowledge',
        materialized_object_ref=v_ref
    where id=c.id;

    return jsonb_build_object('classification_id',c.id,'object_type','knowledge','object_ref',v_ref);
  end if;

  raise exception 'category_not_auto_materializable:%', c.primary_category;
end;
$$;

revoke all on function dcse_cp.escd_materialize_classification(uuid,boolean) from public,anon;
grant execute on function dcse_cp.escd_materialize_classification(uuid,boolean)
to authenticated,service_role;

create or replace function dcse_cp.escd_recent_conversations(
  p_limit integer default 50
)
returns table(
  id uuid,
  external_ref text,
  title text,
  lane text,
  status text,
  started_at timestamptz,
  updated_at timestamptz,
  last_turn_at timestamptz,
  last_turn_summary text,
  turn_count bigint
)
language sql
security definer
set search_path to 'pg_catalog','dcse_cp'
as $$
  select
    c.id,c.external_ref,c.title,c.lane::text,c.status::text,c.started_at,c.updated_at,
    max(ct.created_at) as last_turn_at,
    (array_agg(ct.summary order by ct.created_at desc) filter (where ct.id is not null))[1] as last_turn_summary,
    count(ct.id) as turn_count
  from dcse_cp.conversations c
  left join dcse_cp.conversation_turns ct on ct.conversation_id=c.id
  where auth.role()='service_role'
     or (dcse_cp.is_dcs_owner() and (c.created_by=auth.uid() or c.created_by is null))
  group by c.id
  order by coalesce(max(ct.created_at),c.updated_at) desc
  limit greatest(1,least(coalesce(p_limit,50),200));
$$;

revoke all on function dcse_cp.escd_recent_conversations(integer) from public,anon;
grant execute on function dcse_cp.escd_recent_conversations(integer)
to authenticated,service_role;

create or replace function dcse_cp.escd_conversation_snapshot(
  p_conversation_id uuid
)
returns jsonb
language plpgsql
security definer
set search_path to 'pg_catalog','dcse_cp'
as $$
declare
  v_conv jsonb;
  v_turns jsonb;
  v_ops jsonb;
  v_subjects jsonb;
begin
  if not exists (
    select 1 from dcse_cp.conversations c
    where c.id=p_conversation_id
      and (auth.role()='service_role' or (dcse_cp.is_dcs_owner() and (c.created_by=auth.uid() or c.created_by is null)))
  ) then
    raise exception 'conversation_not_accessible';
  end if;

  select to_jsonb(c) into v_conv
  from dcse_cp.conversations c where c.id=p_conversation_id;

  select coalesce(jsonb_agg(
    to_jsonb(ct) || jsonb_build_object(
      'classification',(
        select to_jsonb(cl)
        from dcse_cp.escd_turn_classifications cl
        where cl.conversation_turn_id=ct.id
        limit 1
      )
    ) order by ct.turn_index
  ),'[]'::jsonb)
  into v_turns
  from dcse_cp.conversation_turns ct
  where ct.conversation_id=p_conversation_id;

  select coalesce(jsonb_agg(to_jsonb(o) order by o.created_at),'[]'::jsonb)
  into v_ops
  from dcse_cp.escd_operation_turns o
  where o.conversation_id=p_conversation_id;

  select coalesce(jsonb_agg(distinct to_jsonb(s)),'[]'::jsonb)
  into v_subjects
  from dcse_cp.escd_subjects s
  join dcse_cp.escd_subject_links sl on sl.subject_id=s.id
  where (
    (sl.object_type='conversation' and sl.object_ref=p_conversation_id::text)
    or
    (sl.object_type='conversation_turn' and sl.object_ref in (
      select id::text from dcse_cp.conversation_turns where conversation_id=p_conversation_id
    ))
  );

  return jsonb_build_object(
    'conversation',v_conv,
    'turns',v_turns,
    'operations',v_ops,
    'subjects',v_subjects
  );
end;
$$;

revoke all on function dcse_cp.escd_conversation_snapshot(uuid) from public,anon;
grant execute on function dcse_cp.escd_conversation_snapshot(uuid)
to authenticated,service_role;

