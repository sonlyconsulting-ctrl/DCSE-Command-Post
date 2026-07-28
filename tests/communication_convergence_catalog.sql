-- Read-only DCSE V7 communication convergence validation.
-- Target: staging project liwdquzuigrlgfzgmpjp. No DDL or DML.
with checks(name, passed, detail) as (
  values
    ('v7_worker schema exists', to_regnamespace('v7_worker') is not null, 'catalog'),
    ('authoritative queue exists', to_regclass('v7_worker.queue_message') is not null, 'v7_worker.queue_message'),
    ('PGMQ physical queue absent', (select count(*) = 0 from pgmq.meta), 'pgmq.meta rows=0'),
    ('all v7_worker tables use RLS', not exists (
       select 1 from pg_class c join pg_namespace n on n.oid=c.relnamespace
       where n.nspname='v7_worker' and c.relkind in ('r','p') and not c.relrowsecurity
     ), 'pg_class.relrowsecurity'),
    ('security definer search paths locked', not exists (
       select 1 from pg_proc p join pg_namespace n on n.oid=p.pronamespace
       where n.nspname in ('v7_worker','v7_worker_api','v7_worker_private','public')
         and p.prosecdef and (p.proname like 'v7_%' or n.nspname <> 'public')
         and not ('search_path=""' = any(coalesce(p.proconfig,array[]::text[])))
     ), 'search_path empty'),
    ('worker identity derives from app metadata', exists (
       select 1 from pg_proc p join pg_namespace n on n.oid=p.pronamespace
       where n.nspname='v7_worker_private' and p.proname='session_agent_id'
         and pg_get_functiondef(p.oid) like '%app_metadata%'
         and pg_get_functiondef(p.oid) !~ $$v_claims\s*->\s*'user_metadata'$$
     ), 'v7_worker_private.session_agent_id'),
    ('gate submissions acknowledged', (
       select count(*)=3 and bool_and(submission_status='acked' and dc_event_id is not null)
       from v7_worker.result_submission where task_id like 'COMM-GATE-001-%'
     ), 'three acknowledged submissions including contained duplicate'),
    ('gate claims closed', (
       select count(*)=3 and bool_and(released_at is not null and acked_at is not null)
       from v7_worker.task_claim where task_id like 'COMM-GATE-001-%'
     ), 'three closed claims'),
    ('no active claims', not exists (
       select 1 from v7_worker.task_claim where released_at is null and visibility_timeout_at > now()
     ), 'queue quiescent'),
    ('no unacknowledged submissions', not exists (
       select 1 from v7_worker.result_submission where submission_status <> 'acked'
     ), 'result buffer quiescent')
)
select name, case when passed then 'PASS' else 'FAIL' end as status, detail
from checks
order by name;
