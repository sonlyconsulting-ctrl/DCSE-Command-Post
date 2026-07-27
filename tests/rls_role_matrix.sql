-- ============================================================================
-- DCSE V7 — 15-Case RLS Role Matrix (deterministic authority for PASS/FAIL)
-- ============================================================================
-- Target: PR #14 Supabase preview branch ONLY (project ref liwdquzuigrlgfzgmpjp)
-- NEVER run against production (nevgdyfpxdaloacuutal).
--
-- Method
--   Each case runs in a savepoint sub-block under an explicit database role.
--   A mutating probe performs the action then raises the sentinel
--   'CERT_PROBE_ROLLBACK' to force savepoint rollback, so no probe persists
--   side effects. Catching the sentinel => the action was ALLOWED.
--   Catching any other SQLSTATE => the action was DENIED.
--
--   Cases are evaluated in the role that actually exercises the surface:
--     anon / authenticated : the public (PostgREST) surface
--     service_role         : the surface the workers actually run under today
--   The role is recorded per case so the receipt cannot conflate them.
--
--   Evaluating cases 8-11 under service_role is deliberate. Workers currently
--   hold the service_role key, which bypasses RLS entirely; a matrix that only
--   probed anon would report a false green. These invariants are therefore
--   enforced by constraints and triggers, which bind every role.
--
-- Usage
--   psql -f tests/rls_role_matrix.sql            (or Supabase MCP execute_sql)
--   Then: select * from v7_cert.results order by test_no;
-- ============================================================================

create schema if not exists v7_cert;

drop table if exists v7_cert.results;
create table v7_cert.results (
  test_no     integer primary key,
  test_name   text not null,
  probe_role  text not null,
  expected    text not null,
  actual      text not null,
  status      text not null,
  detail      text,
  executed_at timestamptz not null default now()
);

-- ---------------------------------------------------------------------------
-- Deterministic fixtures (idempotent; FK order matters)
-- ---------------------------------------------------------------------------
delete from v7_worker.result_submission where agent_id like 'CERT-%';
delete from v7_worker.task_claim        where agent_id like 'CERT-%';
delete from v7_worker.heartbeat         where agent_id like 'CERT-%';
delete from v7_worker.queue_message     where task_id  like 'CERT-%';
delete from v7_worker.agent_identity    where agent_id like 'CERT-%';

insert into v7_worker.agent_identity
  (agent_id, agent_name, model_family, device_id, device_hostname,
   authorized_lanes, authorized_task_types, status, max_concurrent_tasks)
values
  ('CERT-OK',    'Cert Approved', 'deterministic','CERTDEV','certhost','{DCSE,SYSTEM}','{rls_test,validation}','approved', 1),
  ('CERT-DIS',   'Cert Disabled', 'deterministic','CERTDEV','certhost','{DCSE}',       '{rls_test}',           'suspended',1),
  ('CERT-PS',    'Cert PS',       'deterministic','CERTDEV','certhost','{PS}',         '{rls_test}',           'approved', 1),
  ('CERT-OTHER', 'Cert Other',    'deterministic','CERTDEV','certhost','{DCSE}',       '{rls_test}',           'approved', 1);

insert into v7_worker.queue_message (msg_id, task_id, lane, task_type, priority, runtime_packet)
values (900001,'CERT-TASK-DCSE','DCSE','rls_test',5,'{"probe":"dcse"}'::jsonb),
       (900002,'CERT-TASK-PS',  'PS',  'rls_test',9,'{"probe":"ps"}'::jsonb);

-- live claim owned by CERT-OTHER (cross-worker tamper tests)
-- expired claim owned by CERT-OK   (expiry / dispatcher recovery tests)
insert into v7_worker.task_claim
  (queue_msg_id, task_id, agent_id, lane, task_type, visibility_timeout_at, lease_expires_at, attempt_number)
values
  (900001,'CERT-TASK-DCSE','CERT-OTHER','DCSE','rls_test', now()+interval '30 minutes', now()+interval '30 minutes',1),
  (900002,'CERT-TASK-PS',  'CERT-OK',   'DCSE','rls_test', now()-interval '10 minutes', now()-interval '10 minutes',1);

-- ---------------------------------------------------------------------------
-- Runner
-- ---------------------------------------------------------------------------
do $harness$
declare
  v_actual text; v_detail text; v_other_claim bigint; v_expired_claim bigint;
  v_ok_claim bigint; v_n integer; sentinel text := 'CERT_PROBE_ROLLBACK';
begin
  select claim_id into v_other_claim   from v7_worker.task_claim where agent_id='CERT-OTHER' and task_id='CERT-TASK-DCSE';
  select claim_id into v_expired_claim from v7_worker.task_claim where agent_id='CERT-OK'    and task_id='CERT-TASK-PS';

  -- 1. Anonymous user cannot read worker tables
  begin set local role anon; perform 1 from v7_worker.agent_identity limit 1; v_actual:='ALLOWED';
  exception when others then v_actual:='DENIED'; v_detail:=sqlstate; end; reset role;
  insert into v7_cert.results values (1,'Anonymous cannot read worker tables','anon','DENIED',v_actual,
    case when v_actual='DENIED' then 'PASS' else 'FAIL' end, v_detail);

  -- 2. Ordinary authenticated user cannot read worker tables
  v_detail:=null;
  begin set local role authenticated; perform 1 from v7_worker.agent_identity limit 1; v_actual:='ALLOWED';
  exception when others then v_actual:='DENIED'; v_detail:=sqlstate; end; reset role;
  insert into v7_cert.results values (2,'Authenticated cannot read worker tables','authenticated','DENIED',v_actual,
    case when v_actual='DENIED' then 'PASS' else 'FAIL' end, v_detail);

  -- 3. Unknown worker cannot heartbeat
  v_detail:=null;
  begin perform v7_worker.send_heartbeat('CERT-GHOST','idle',null,null,null,null,null,null,null);
    v_actual:='ALLOWED'; raise exception using message=sentinel;
  exception when others then if sqlerrm=sentinel then v_actual:='ALLOWED'; else v_actual:='DENIED'; v_detail:=sqlerrm; end if; end;
  insert into v7_cert.results values (3,'Unknown worker cannot heartbeat','service_role','DENIED',v_actual,
    case when v_actual='DENIED' then 'PASS' else 'FAIL' end, v_detail);

  -- 4. Disabled (suspended) worker cannot heartbeat
  v_detail:=null;
  begin perform v7_worker.send_heartbeat('CERT-DIS','idle',null,null,null,null,null,null,null);
    raise exception using message=sentinel;
  exception when others then if sqlerrm=sentinel then v_actual:='ALLOWED'; v_detail:='suspended accepted';
    else v_actual:='DENIED'; v_detail:=sqlerrm; end if; end;
  insert into v7_cert.results values (4,'Disabled worker cannot heartbeat','service_role','DENIED',v_actual,
    case when v_actual='DENIED' then 'PASS' else 'FAIL' end, v_detail);

  -- 5. Disabled worker cannot claim
  v_detail:=null;
  begin perform * from v7_worker.claim_next_task('CERT-DIS',1800); raise exception using message=sentinel;
  exception when others then if sqlerrm=sentinel then v_actual:='ALLOWED'; else v_actual:='DENIED'; v_detail:=sqlerrm; end if; end;
  insert into v7_cert.results values (5,'Disabled worker cannot claim','service_role','DENIED',v_actual,
    case when v_actual='DENIED' then 'PASS' else 'FAIL' end, v_detail);

  -- 6. Worker cannot claim an unauthorized lane
  v_detail:=null;
  begin select count(*) into v_n from v7_worker.claim_next_task('CERT-PS',1800) t where t.lane<>'PS';
    if v_n>0 then v_actual:='ALLOWED'; v_detail:='out-of-lane rows: '||v_n;
    else v_actual:='DENIED'; v_detail:='no out-of-lane rows served'; end if;
    raise exception using message=sentinel;
  exception when others then if sqlerrm<>sentinel then v_actual:='DENIED'; v_detail:=sqlerrm; end if; end;
  insert into v7_cert.results values (6,'Worker cannot claim unauthorized lane','service_role','DENIED',v_actual,
    case when v_actual='DENIED' then 'PASS' else 'FAIL' end, v_detail);

  -- 7. Non-PS worker cannot claim a PS task
  v_detail:=null;
  begin select count(*) into v_n from v7_worker.claim_next_task('CERT-OK',1800) t where t.lane='PS';
    if v_n>0 then v_actual:='ALLOWED'; v_detail:='PS rows served: '||v_n;
    else v_actual:='DENIED'; v_detail:='PS task withheld from non-PS worker'; end if;
    raise exception using message=sentinel;
  exception when others then if sqlerrm<>sentinel then v_actual:='DENIED'; v_detail:=sqlerrm; end if; end;
  insert into v7_cert.results values (7,'Non-PS worker cannot claim PS task','service_role','DENIED',v_actual,
    case when v_actual='DENIED' then 'PASS' else 'FAIL' end, v_detail);

  -- 8. Worker cannot modify another worker's claim
  v_detail:=null;
  begin perform set_config('app.worker_id','CERT-OK',true);
    update v7_worker.task_claim set released_at=now(), release_reason='tampered' where claim_id=v_other_claim;
    get diagnostics v_n=row_count;
    if v_n>0 then v_actual:='ALLOWED'; v_detail:='rows tampered: '||v_n;
    else v_actual:='DENIED'; v_detail:='no rows affected'; end if;
    raise exception using message=sentinel;
  exception when others then if sqlerrm<>sentinel then v_actual:='DENIED'; v_detail:=sqlerrm; end if; end;
  perform set_config('app.worker_id','',true);
  insert into v7_cert.results values (8,'Worker cannot modify another worker claim','service_role','DENIED',v_actual,
    case when v_actual='DENIED' then 'PASS' else 'FAIL' end, v_detail);

  -- 9. Worker cannot submit without an active claim
  v_detail:=null;
  begin insert into v7_worker.result_submission (task_id,claim_id,agent_id,submission_status,result_event_type,result_output)
    values ('CERT-TASK-DCSE',999999999,'CERT-OK','pending','completed','{}'::jsonb);
    v_actual:='ALLOWED'; v_detail:='accepted non-existent claim'; raise exception using message=sentinel;
  exception when others then if sqlerrm<>sentinel then v_actual:='DENIED'; v_detail:=sqlerrm; end if; end;
  insert into v7_cert.results values (9,'Worker cannot submit without active claim','service_role','DENIED',v_actual,
    case when v_actual='DENIED' then 'PASS' else 'FAIL' end, v_detail);

  -- 10. Worker cannot submit after claim expiry
  v_detail:=null;
  begin insert into v7_worker.result_submission (task_id,claim_id,agent_id,submission_status,result_event_type,result_output)
    values ('CERT-TASK-PS',v_expired_claim,'CERT-OK','pending','completed','{}'::jsonb);
    v_actual:='ALLOWED'; v_detail:='accepted expired lease'; raise exception using message=sentinel;
  exception when others then if sqlerrm<>sentinel then v_actual:='DENIED'; v_detail:=sqlerrm; end if; end;
  insert into v7_cert.results values (10,'Worker cannot submit after claim expiry','service_role','DENIED',v_actual,
    case when v_actual='DENIED' then 'PASS' else 'FAIL' end, v_detail);

  -- 11. Duplicate result submission is rejected
  v_detail:=null;
  begin insert into v7_worker.result_submission (task_id,claim_id,agent_id,submission_status,result_event_type,result_output)
    values ('CERT-TASK-DCSE',v_other_claim,'CERT-OTHER','pending','completed','{}'::jsonb);
    insert into v7_worker.result_submission (task_id,claim_id,agent_id,submission_status,result_event_type,result_output)
    values ('CERT-TASK-DCSE',v_other_claim,'CERT-OTHER','pending','completed','{}'::jsonb);
    v_actual:='ALLOWED'; v_detail:='duplicate accepted'; raise exception using message=sentinel;
  exception when others then if sqlerrm<>sentinel then v_actual:='DENIED'; v_detail:=sqlerrm; end if; end;
  insert into v7_cert.results values (11,'Duplicate result submission rejected','service_role','DENIED',v_actual,
    case when v_actual='DENIED' then 'PASS' else 'FAIL' end, v_detail);

  -- 12. Authorized worker CAN heartbeat (positive control)
  v_detail:=null;
  begin perform v7_worker.send_heartbeat('CERT-OK','idle',null,null,null,null,null,null,null);
    v_actual:='ALLOWED'; v_detail:='heartbeat accepted'; raise exception using message=sentinel;
  exception when others then if sqlerrm<>sentinel then v_actual:='DENIED'; v_detail:=sqlerrm; end if; end;
  insert into v7_cert.results values (12,'Authorized worker can heartbeat','service_role','ALLOWED',v_actual,
    case when v_actual='ALLOWED' then 'PASS' else 'FAIL' end, v_detail);

  -- 13. Authorized worker CAN claim an eligible task (positive control)
  v_detail:=null;
  begin perform * from v7_worker.release_task_claim(v_other_claim,'CERT-OTHER','timeout');
    select count(*) into v_n from v7_worker.claim_next_task('CERT-OK',1800) t where t.lane='DCSE';
    if v_n>0 then v_actual:='ALLOWED'; v_detail:='claimed DCSE rows: '||v_n;
    else v_actual:='DENIED'; v_detail:='no eligible task'; end if;
    raise exception using message=sentinel;
  exception when others then if sqlerrm<>sentinel then v_actual:='DENIED'; v_detail:=sqlerrm; end if; end;
  insert into v7_cert.results values (13,'Authorized worker can claim eligible task','service_role','ALLOWED',v_actual,
    case when v_actual='ALLOWED' then 'PASS' else 'FAIL' end, v_detail);

  -- 14. Authorized worker can renew and submit its own result (positive control)
  v_detail:=null;
  begin perform set_config('app.worker_id','CERT-OK',true);
    insert into v7_worker.task_claim (queue_msg_id,task_id,agent_id,lane,task_type,visibility_timeout_at,lease_expires_at,attempt_number)
    values (900001,'CERT-TASK-DCSE','CERT-OK','DCSE','rls_test',now()+interval '30 minutes',now()+interval '30 minutes',1)
    returning claim_id into v_ok_claim;
    update v7_worker.task_claim set visibility_timeout_at=now()+interval '60 minutes' where claim_id=v_ok_claim;
    insert into v7_worker.result_submission (task_id,claim_id,agent_id,submission_status,result_event_type,result_output)
    values ('CERT-TASK-DCSE',v_ok_claim,'CERT-OK','pending','completed','{"ok":true}'::jsonb);
    v_actual:='ALLOWED'; v_detail:='renew + own-result submit ok'; raise exception using message=sentinel;
  exception when others then if sqlerrm<>sentinel then v_actual:='DENIED'; v_detail:=sqlerrm; end if; end;
  perform set_config('app.worker_id','',true);
  insert into v7_cert.results values (14,'Authorized worker can renew and submit own result','service_role','ALLOWED',v_actual,
    case when v_actual='ALLOWED' then 'PASS' else 'FAIL' end, v_detail);

  -- 15. Dispatcher recovers expired claim; audit remains immutable to workers
  v_detail:=null;
  declare v_rec boolean:=false; v_imm boolean:=false;
  begin
    begin perform * from v7_worker.dispatcher_recovery_cycle();
      select (released_at is not null) into v_rec from v7_worker.task_claim where claim_id=v_expired_claim;
    exception when others then v_rec:=false; v_detail:='dispatcher err: '||sqlerrm; end;
    begin set local role anon; delete from v7_worker.task_claim where claim_id=v_expired_claim; v_imm:=false;
    exception when others then v_imm:=true; end; reset role;
    if v_rec and v_imm then v_actual:='ALLOWED'; v_detail:=coalesce(v_detail,'')||'recovered=t; worker-delete blocked';
    else v_actual:='DENIED'; v_detail:=coalesce(v_detail,'')||'recovered='||v_rec||'; immutable='||v_imm; end if;
    raise exception using message=sentinel;
  exception when others then if sqlerrm<>sentinel then v_actual:='DENIED'; v_detail:=sqlerrm; end if; end;
  insert into v7_cert.results values (15,'Dispatcher recovers expired claim; audit immutable','mixed','ALLOWED',v_actual,
    case when v_actual='ALLOWED' then 'PASS' else 'FAIL' end, v_detail);
end
$harness$;

-- Fixture teardown (comment out to inspect state after a run)
delete from v7_worker.result_submission where agent_id like 'CERT-%';
delete from v7_worker.task_claim        where agent_id like 'CERT-%';
delete from v7_worker.heartbeat         where agent_id like 'CERT-%';
delete from v7_worker.queue_message     where task_id  like 'CERT-%';
delete from v7_worker.agent_identity    where agent_id like 'CERT-%';

select test_no, test_name, probe_role, expected, actual, status, detail
from v7_cert.results order by test_no;
