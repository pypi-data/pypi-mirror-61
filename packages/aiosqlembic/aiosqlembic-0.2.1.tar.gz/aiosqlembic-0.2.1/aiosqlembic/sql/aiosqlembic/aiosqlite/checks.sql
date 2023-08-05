--name: check_connection^
--record_class: ConDB
select 1 'exists';
--name: check_aiosqlembic^
--record_class: ConDBTable
select exists(select name from sqlite_master where type='table' and name='aiosqlembic') 'exists';