-- Remove superseded duplicate permissive policies and cover new foreign keys.
drop policy if exists guestbook_contributor_insert on family_vow_go.guestbook_entries;
drop policy if exists guestbook_member_select on family_vow_go.guestbook_entries;
drop policy if exists wedding_media_contributor_insert on family_vow_go.wedding_media;
drop policy if exists wedding_media_member_select on family_vow_go.wedding_media;
drop policy if exists wedding_profile_member_select on family_vow_go.wedding_profiles;
drop policy if exists wedding_profile_admin_update on family_vow_go.wedding_profiles;
drop policy if exists wedding_tasks_member_select on family_vow_go.wedding_tasks;

create index if not exists engagement_invitations_created_by_idx on family_vow_go.engagement_invitations(created_by);
create index if not exists engagement_invitations_guest_id_idx on family_vow_go.engagement_invitations(guest_id) where guest_id is not null;
create index if not exists record_activity_actor_id_idx on family_vow_go.record_activity(actor_id) where actor_id is not null;
create index if not exists record_activity_record_id_idx on family_vow_go.record_activity(record_id);
create index if not exists wedding_notifications_created_by_idx on family_vow_go.wedding_notifications(created_by);
create index if not exists workspace_records_archived_by_idx on family_vow_go.workspace_records(archived_by) where archived_by is not null;
create index if not exists workspace_records_created_by_idx on family_vow_go.workspace_records(created_by);
create index if not exists workspace_records_updated_by_idx on family_vow_go.workspace_records(updated_by);
