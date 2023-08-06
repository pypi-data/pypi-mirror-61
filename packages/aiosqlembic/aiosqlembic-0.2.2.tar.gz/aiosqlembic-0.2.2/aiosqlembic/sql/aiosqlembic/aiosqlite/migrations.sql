--name: create_schema#
create table aiosqlembic
(
    id         integer primary key autoincrement,
    version_id integer not null,
    is_applied integer not null,
    tstamp     timestamp default (datetime('now'))
);

--name: insert_revision!
insert into aiosqlembic(version_id, is_applied) values(:version_id, :is_applied);

--name: get_version
--record_class: Version
select version_id, is_applied from aiosqlembic order by id desc;

--name: migrate_revision^
--record_class: MigrateRevision
select tstamp, is_applied from aiosqlembic where version_id=:version_id order by tstamp desc limit 1;

--name: delete_revision
delete from aiosqlembic where version_id=:version_id;