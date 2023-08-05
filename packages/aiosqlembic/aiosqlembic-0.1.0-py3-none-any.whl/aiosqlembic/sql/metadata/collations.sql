-- name: get_all_collations
-- record_class: Collation
select collname     as name,
       n.nspname    as schemaname,
       case collprovider
           when 'd' then 'database default'
           when 'i' then 'icu'
           when 'c' then 'libc'
           end
                    as provider,
       collencoding as encoding,
       collcollate  as lc_collate,
       collctype    as lc_ctype,
       collversion  as version
from pg_collation c
         INNER JOIN pg_namespace n
                    ON n.oid = c.collnamespace
where nspname not in ('pg_internal', 'pg_catalog', 'information_schema', 'pg_toast')
  and nspname not like 'pg_temp_%'
  and nspname not like 'pg_toast_temp_%'
order by 2, 1
