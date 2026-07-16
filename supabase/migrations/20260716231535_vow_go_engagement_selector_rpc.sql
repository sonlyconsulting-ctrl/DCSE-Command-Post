create or replace function public.vow_go_engagements()
returns jsonb
language sql
stable
security invoker
set search_path = ''
as $$
  select coalesce(jsonb_agg(jsonb_build_object(
    'product_instance_id', pi.id,
    'title', pi.title,
    'status', pi.status,
    'role', pm.role::text,
    'product_mode', coalesce(ws.product_mode,'experience_only'),
    'planner_theme', coalesce(ws.planner_theme,'refined_dark'),
    'couple_theme', coalesce(ws.couple_theme,'romantic_light'),
    'guest_theme', coalesce(ws.guest_theme,'coastal_celebration')
  ) order by pi.title), '[]'::jsonb)
  from family_core.product_memberships pm
  join family_core.product_instances pi on pi.id=pm.product_instance_id
  left join family_vow_go.wedding_settings ws on ws.product_instance_id=pi.id
  where pm.user_id=(select auth.uid()) and pm.status='active' and pi.product_type='vow_go'
$$;

revoke execute on function public.vow_go_engagements() from public, anon;
grant execute on function public.vow_go_engagements() to authenticated;

comment on function public.vow_go_engagements() is 'Returns only active Vow & Go engagements assigned to the authenticated user for the engagement selector.';
