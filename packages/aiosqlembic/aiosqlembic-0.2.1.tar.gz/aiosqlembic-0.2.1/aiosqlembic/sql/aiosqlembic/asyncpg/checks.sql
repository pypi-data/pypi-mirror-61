--name: check_connection^
--record_class: ConDB
select exists(select 1);
--name: check_aiosqlembic^
--record_class: ConDBTable
select exists (
   select 1
   from   pg_tables
   where  schemaname = 'public'
   and    tablename = 'aiosqlembic'
   );