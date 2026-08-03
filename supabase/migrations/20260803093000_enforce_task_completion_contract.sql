create or replace function dcse_cp.enforce_task_completion_contract()
returns trigger
language plpgsql
security invoker
set search_path = pg_catalog, dcse_cp
as $$
declare
  required_key text;
  deliverable text;
  evidence jsonb;
begin
  if new.status <> 'completed'
     or coalesce((new.policy_flags ->> 'completion_contract_version')::integer, 0) < 1 then
    return new;
  end if;

  if jsonb_typeof(new.output_refs) <> 'object' or new.output_refs = '{}'::jsonb then
    raise exception 'completion contract: output_refs must be a nonempty object for task %', new.task_key;
  end if;

  for required_key in
    select jsonb_array_elements_text(coalesce(new.policy_flags -> 'required_output_keys', '[]'::jsonb))
  loop
    evidence := new.output_refs -> required_key;
    if evidence is null or evidence = 'null'::jsonb or evidence = '""'::jsonb
       or evidence = '{}'::jsonb or evidence = '[]'::jsonb then
      raise exception 'completion contract: task % missing nonempty output_ref %', new.task_key, required_key;
    end if;
  end loop;

  if jsonb_typeof(new.output_refs -> 'deliverable_matrix') <> 'object' then
    raise exception 'completion contract: task % requires an object deliverable_matrix', new.task_key;
  end if;

  for deliverable in
    select jsonb_array_elements_text(coalesce(new.policy_flags -> 'required_deliverables', '[]'::jsonb))
  loop
    evidence := new.output_refs -> 'deliverable_matrix' -> deliverable;
    if evidence is null or evidence = 'null'::jsonb or evidence = '""'::jsonb
       or evidence = '{}'::jsonb or evidence = '[]'::jsonb then
      raise exception 'completion contract: task % missing evidence for deliverable %', new.task_key, deliverable;
    end if;
  end loop;

  if exists (select 1 from dcse_cp.agent_task_assignments a where a.task_id = new.id)
     and not exists (
       select 1 from dcse_cp.agent_task_assignments a
       where a.task_id = new.id
         and a.status = 'completed'
         and jsonb_typeof(a.result_payload) = 'object'
         and coalesce(a.result_payload ->> 'outcome','') in
             ('completed','success','approve','approve_with_findings')
     ) then
    raise exception 'completion contract: task % has assignments but no successful completed assignment result', new.task_key;
  end if;

  return new;
end;
$$;

drop trigger if exists trg_enforce_task_completion_contract on dcse_cp.agent_tasks;
create trigger trg_enforce_task_completion_contract
before insert or update of status, output_refs, policy_flags
on dcse_cp.agent_tasks
for each row
execute function dcse_cp.enforce_task_completion_contract();

comment on function dcse_cp.enforce_task_completion_contract() is
'Prevents completion-contract tasks from reaching completed until every required output and deliverable has a nonempty evidence reference and at least one assignment has a successful completed result.';
