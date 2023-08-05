-- name: up_{{ revision_up }}#
{{ upgrade_statements }}

-- name: down_{{ revision_down }}#
{{ downgrade_statements }}
