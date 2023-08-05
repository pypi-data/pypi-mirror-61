-- name: get_all_schemas
-- record_class: Schema
select nspname as schemaname
from pg_catalog.pg_namespace
where nspname not in ('pg_internal', 'pg_catalog', 'information_schema', 'pg_toast')
  and nspname not like 'pg_temp_%'
  and nspname not like 'pg_toast_temp_%'
order by 1;