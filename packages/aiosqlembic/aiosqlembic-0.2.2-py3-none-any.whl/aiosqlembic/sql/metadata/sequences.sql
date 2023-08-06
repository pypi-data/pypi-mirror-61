-- name: get_all_sequences
-- record_class: Sequence
select sequence_schema as schemaname,
       sequence_name   as name
from information_schema.sequences
where sequence_schema not in
      ('pg_internal', 'pg_catalog', 'information_schema', 'pg_toast')
  and sequence_schema not like 'pg_temp_%'
  and sequence_schema not like 'pg_toast_temp_%'
order by 1, 2;