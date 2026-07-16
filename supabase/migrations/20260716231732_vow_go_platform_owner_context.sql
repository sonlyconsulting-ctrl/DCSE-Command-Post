create or replace function public.vow_go_platform_context()
returns jsonb
language sql
stable
security invoker
set search_path = ''
as $$
  select jsonb_build_object(
    'is_platform_owner', family_core.is_platform_owner(),
    'private_engagement_access', false,
    'support_access_requires_authorization', true
  )
$$;

revoke execute on function public.vow_go_platform_context() from public, anon;
grant execute on function public.vow_go_platform_context() to authenticated;

comment on function public.vow_go_platform_context() is 'Platform role check only. It deliberately returns no private engagement content.';
