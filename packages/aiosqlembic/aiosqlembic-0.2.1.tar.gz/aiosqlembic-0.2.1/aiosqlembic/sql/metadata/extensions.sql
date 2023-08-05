-- name: get_all_extensions
-- record_class: Extension
select nspname    as schemaname,
       extname    as name,
       extversion as version,
       e.oid      as oid
from pg_extension e
         INNER JOIN pg_namespace
                    ON pg_namespace.oid = e.extnamespace
order by schemaname, name;