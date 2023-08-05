--name: create_schema#
create table public.aiosqlembic
(
    id         serial    not null,
    version_id bigint    not null,
    is_applied boolean   not null,
    tstamp     timestamp null default now(),
    primary key (id)
);

--name: insert_revision<!
insert into public.aiosqlembic(version_id, is_applied) values(:version_id, :is_applied);

--name: get_version^
--record_class: Version
select public.aiosqlembic.version_id, is_applied from public.aiosqlembic order by id desc;

--name: migrate_revision^
--record_class: MigrateRevision
select tstamp, is_applied from public.aiosqlembic where version_id=:version_id order by tstamp desc limit 1;

--name: delete_revision
delete from public.aiosqlembic where version_id=:version_id;