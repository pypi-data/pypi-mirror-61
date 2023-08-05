import asyncio
import logging
from functools import wraps
from pathlib import Path

import aiosql
import asyncpg
import typer
from aiosql.queries import Queries

from aiosqlembic.schema import Amigration
from aiosqlembic.utils import (
    create_init_dir,
    check_connection,
    get_dsn_from_config,
    load_from_config,
    get_revision_tree,
    print_version,
    templateEnv,
    write_settings_to_config,
    create_test_database,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = typer.Typer()


def async_adapter(wrapped_func):  # type: ignore
    @wraps(wrapped_func)
    def run_sync(*args, **kwargs):  # type: ignore
        loop = asyncio.get_event_loop()
        if loop.is_running():
            from concurrent.futures import ThreadPoolExecutor

            pool = ThreadPoolExecutor(1)
            loop = asyncio.new_event_loop()
            pool.submit(asyncio.set_event_loop, loop).result()
            return pool.submit(
                loop.run_until_complete, wrapped_func(*args, **kwargs)
            ).result()
        else:
            task = wrapped_func(*args, **kwargs)
            return loop.run_until_complete(task)

    return run_sync


@app.command()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        is_flag=True,
        callback=print_version,
        expose_value=False,
        is_eager=True,
        help="Display the version and exit.",
    )
) -> None:
    pass


@app.command()
@async_adapter
async def init(
    migrations_directory_path: Path = Path("aiosqlembic_migrations"),
    config: Path = Path("aiosqlalembic.toml"),
) -> None:
    typer.echo(f"Initialize migrations")
    # creatings migration directory and config file
    if not migrations_directory_path.exists():
        if typer.confirm(  # pragma: no cover
            f"Create migrations directory to {migrations_directory_path.as_posix()} ?",
            default=True,
            abort=True,
        ):
            create_init_dir(
                migrations_directory_path=migrations_directory_path, config=config
            )
    else:
        if typer.confirm(  # pragma: no cover
            f"Existing migrations directory: {migrations_directory_path.as_posix()} overwrite it ?",
            default=False,
            abort=False,
        ):
            create_init_dir(
                migrations_directory_path=migrations_directory_path,
                config=config,
                overwrite=True,
            )

    # gettings dsn info right before creating tables !
    settings = load_from_config(config.resolve())
    config_dsn, secret_dsn = get_dsn_from_config(settings.dsn)
    connection_test = await check_connection(dsn=config_dsn)
    while not connection_test and typer.confirm(  # pragma: no cover
        "Default db connection seems to fail, change them ?", default=True, abort=True
    ):
        for prompt, default in [(p, d) for p, d in iter(settings.dsn)]:
            reply = typer.prompt(prompt, default=default)
            setattr(settings.dsn, prompt, reply)
        config_dsn, secret_dsn = get_dsn_from_config(settings.dsn)
        typer.echo(f"Setting new config dsn to: {secret_dsn}")
        write_settings_to_config(config, settings)
        settings = load_from_config(config)
        config_dsn, secret_dsn = get_dsn_from_config(settings.dsn)
        connection_test = await check_connection(dsn=config_dsn)


@app.command()
@async_adapter
async def revision(
    config: Path = Path("aiosqlalembic.toml"),
    revision_msg: str = typer.Option(..., "--message", "-m"),
    auto_generate: bool = typer.Option(True),
) -> None:
    if not config.exists():
        typer.echo(f"No config file {config.as_posix()} detected")
        raise typer.Abort()

    settings = load_from_config(config)
    config_dsn, secret_dsn = get_dsn_from_config(settings.dsn)
    connection_test = await check_connection(dsn=config_dsn)

    if not connection_test:
        typer.echo(f"Issue connecting to {secret_dsn}")
        raise typer.Abort()
    else:
        typer.echo(f"Connected to: {secret_dsn}")

        revision_tree = get_revision_tree(settings.migrations.base_directory)
        last_revision = revision_tree[-1]
        expected_revision_file = (
            settings.migrations.base_directory
            / f"{last_revision.rev_number + 1}_{revision_msg}.sql"
        )

        expected_revision_file.touch()
        revision_template = "revision.sql"
        template = templateEnv.get_template(revision_template)

        if auto_generate:
            typer.echo(
                "Attempt at generating sql statements! Please review them once written!"
            )
            # we load in theorical db the current list of revisions up the latest one
            async with create_test_database(
                config_dsn, "theorical_aiosqlembic"
            ) as theorical:
                try:
                    # putting theorical up to date with revision files
                    revision_queries: Queries = aiosql.from_path(
                        settings.migrations.base_directory, "asyncpg"
                    )
                    up_queries = [
                        x for x in revision_queries.available_queries if "up" in x
                    ]
                    pool_theorical = await asyncpg.create_pool(theorical)
                    if up_queries:
                        for up in up_queries:
                            await getattr(revision_queries, up)(pool_theorical)

                    pool_current = await asyncpg.create_pool(config_dsn)
                    # up
                    up_mig = await Amigration().create(pool_theorical, pool_current)
                    up_mig.set_safety(False)
                    up_mig.add_all_changes()
                    logger.debug(up_mig.statements)
                    up_ss = up_mig.sql
                    upgrade_statements = up_ss
                    # down
                    down_mig = await Amigration().create(pool_current, pool_theorical)
                    down_mig.set_safety(False)
                    down_mig.add_all_changes()
                    logger.debug(down_mig.statements)
                    down_ss = down_mig.sql
                    downgrade_statements = down_ss
                except Exception as e:
                    logger.error(e)
                    raise e
                finally:
                    await pool_current.close()
                    await pool_theorical.close()

        else:
            upgrade_statements = "add your upgrade statements here"
            downgrade_statements = "add your downgrade statements here"

        output = template.render(
            revision_up=last_revision.rev_number + 1,
            revision_down=last_revision.rev_number,
            upgrade_statements=upgrade_statements,
            downgrade_statements=downgrade_statements,
        )
        expected_revision_file.write_text(output)

        typer.echo(
            f"Generated revision: {last_revision.rev_number + 1} with message: {revision_msg}"
        )
        typer.echo(f"File has been saved to {expected_revision_file.as_posix()}")


# @app.command()
# @async_adapter
# async def upgrade(
#     migrations_directory_path: Path = Path("aiosqlembic_migrations"),
#     config: Path = Path("aiosqlalembic.toml"),
#     revision_id: int = typer.Option(..., "--revision-id", "-r"),
# ) -> None:
#     settings = load_from_config(config)
#     config_dsn, secret_dsn = get_dsn_from_config(settings.dsn)
#     connection_test = await check_connection(dsn=config_dsn)
#     if not connection_test:
#         typer.echo(f"Issue connecting to {secret_dsn}")
#         raise typer.Abort()
#     else:
#         typer.echo(f"Connected to: {secret_dsn}")
#
#     count, existing = get_list_revision(migrations_directory_path)
#     logger.debug(count)
#     logger.debug(existing)


if __name__ == "__main__":
    app()
