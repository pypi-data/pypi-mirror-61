from datetime import datetime
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Union, Any, List, Tuple, Optional

import aiosql
from aiosql.aiosql import _ADAPTERS
import asyncclick as click
from aiosql.queries import Queries
from click import Context

from aiosqlembic.models.cli import (
    Version,
    MigrateRevision,
)
from aiosqlembic.utils import (
    get_revision_tree,
    print_version,
    get_connection,
    camel2snake,
    templateEnv,
    get_next_revision,
    get_current_revision,
    get_aiosqlembic_queries,
)

MIN_VERSION = 0
MAX_VERSION = 2 ** (64 - 1) - 1  # ie max size of sqlite3 integer and postgresql bigint

logging.basicConfig(
    format="%(levelname)s:%(filename)s.%(funcName)s:%(lineno)d %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class AiosqlembicContext:
    debug: bool
    migration_directory: Path
    driver: str
    driver_adapter: Union[str, Any]
    dsn: str
    logger: logging.Logger
    aiosqlembic_queries: Queries
    current_version: Version


pass_settings = click.make_pass_decorator(AiosqlembicContext)


@click.group()
@click.option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Prints aiosqlembic version and exits",
)
@click.option(
    "--debug/--no-debug",
    default=False,
    help="Sets the logging level to DEBUG or let it at INFO",
)
@click.option(
    "-m",
    "--migration-directory",
    default=Path("."),
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True,
        resolve_path=True,
    ),
    help="Where migrations files will be",
)
@click.argument("driver", required=True, type=click.Choice(["asyncpg", "aiosqlite"]))
@click.argument("dsn", required=True)
@click.pass_context
async def cli(
    ctx: Context, debug: bool, migration_directory: Path, driver: str, dsn: str
) -> None:
    """
    Main entry point for the application
    """
    if debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Logging set to DEBUG")
    else:
        logger.setLevel(logging.INFO)
        logger.info("Logging set to INFO")

    driver_adapter = _ADAPTERS[driver]
    aiosqlembic_queries = get_aiosqlembic_queries(driver=driver)
    try:
        async with get_connection(driver, dsn) as connection:
            # conn_db: ConDB = await aiosqlembic_queries.check_connection(connection)
            conn_db_table = await aiosqlembic_queries.check_aiosqlembic(connection)
            if not conn_db_table.exists:
                logger.debug("aiosqlembic table doesnt exist")
                await aiosqlembic_queries.create_schema(connection)

                applied = True if driver == "asyncpg" else 1
                inserted = await aiosqlembic_queries.insert_revision(
                    connection, version_id=0, is_applied=applied
                )
                logger.debug(f"inserted: {inserted}")
            else:
                click.echo(f"Connected")

            current_version = await aiosqlembic_queries.get_version(connection)
            ctx.obj = AiosqlembicContext(
                debug=debug,
                migration_directory=Path(migration_directory),
                driver=driver,
                dsn=dsn,
                logger=logger,
                driver_adapter=driver_adapter,
                aiosqlembic_queries=aiosqlembic_queries,
                current_version=current_version,
            )
    except Exception as e:
        logger.error(e)
        raise e
    finally:
        pass


@cli.command()
@pass_settings
async def status(settings: AiosqlembicContext) -> None:
    """Prints the status of revisions files and if those are applied or not"""
    logger.debug(
        f"STATUS with debug: {settings.debug} - migrations: {settings.migration_directory} - driver: {settings.driver} - dsn: {settings.dsn}"
    )
    revision_tree = get_revision_tree(
        settings.migration_directory, MIN_VERSION, MAX_VERSION
    )
    statusline = (
        "+" * 10
        + " time "
        + "+" * 10
        + " " * 4
        + "+" * 4
        + " applied at "
        + "+" * 3
        + " " * 4
        + "+" * 10
        + " revision file "
        + "+" * 10
    )
    click.echo(statusline)
    async with get_connection(settings.driver, settings.dsn) as connection:
        for revision in revision_tree:
            migrate_revision: MigrateRevision = await settings.aiosqlembic_queries.migrate_revision(
                connection, version_id=revision.version_id
            )

            if migrate_revision is not None and migrate_revision.is_applied:
                applied_ts = migrate_revision.tstamp.isoformat()
            else:
                applied_ts = "pending            "
            click.echo(
                f"{datetime.utcnow().isoformat():30s}{applied_ts:15s}    {revision.file}"
            )
    return


@cli.command()
@click.option("--name", "-n", required=True)
@click.option("--auto", "-a", required=False, default=False, type=click.BOOL)
@pass_settings
async def create(settings: AiosqlembicContext, name: str, auto: bool) -> None:
    """Create a revision file"""
    logger.debug(
        f"Create with debug: {settings.debug} - migrations: {settings.migration_directory} - driver: {settings.driver} - dsn: {settings.dsn}"
    )
    version_id = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    logger.debug(version_id)
    nospacename = name.replace(" ", "_")
    expected_revision_file = (
        settings.migration_directory / f"{version_id}_{camel2snake(nospacename)}.sql"
    )
    logger.debug(expected_revision_file)
    expected_revision_file.touch()
    revision_template = "revision.sql"
    template = templateEnv.get_template(revision_template)

    # if auto:
    #     click.echo(
    #         "Attempt at generating sql statements! Please review them once written!"
    #     )
    #     # we load in theorical db the current list of revisions up the latest one
    #     async with create_test_database(
    #         settings.dsn, "theorical_aiosqlembic"
    #     ) as theorical:
    #         try:
    #             # putting theorical up to date with revision files
    #             revision_queries: Queries = aiosql.from_path(
    #                 settings.migration_directory, settings.driver
    #             )
    #             up_queries = [
    #                 x for x in revision_queries.available_queries if "up" in x
    #             ]
    #             pool_theorical = await asyncpg.create_pool(theorical)
    #             if up_queries:
    #                 for up in up_queries:
    #                     await getattr(revision_queries, up)(pool_theorical)
    #
    #             pool_current = await asyncpg.create_pool(settings.dsn)
    #             # up
    #             up_mig = await Amigration().create(pool_theorical, pool_current)
    #             up_mig.set_safety(False)
    #             up_mig.add_all_changes()
    #             logger.debug(up_mig.statements)
    #             up_ss = up_mig.sql
    #             upgrade_statements = up_ss
    #             # down
    #             down_mig = await Amigration().create(pool_current, pool_theorical)
    #             down_mig.set_safety(False)
    #             down_mig.add_all_changes()
    #             logger.debug(down_mig.statements)
    #             down_ss = down_mig.sql
    #             downgrade_statements = down_ss
    #         except Exception as e:
    #             logger.error(e)
    #             raise e
    #         finally:
    #             await pool_current.close()
    #             await pool_theorical.close()

    # else:
    upgrade_statements = "SELECT 'upgrade sql query here';"
    downgrade_statements = "SELECT 'downgrade sql query here';"

    output = template.render(
        upgrade_statements=upgrade_statements,
        downgrade_statements=downgrade_statements,
    )
    expected_revision_file.write_text(output)
    click.echo(f"Created: {expected_revision_file}")


async def get_current(settings: AiosqlembicContext) -> Version:
    async with get_connection(settings.driver, settings.dsn) as connection:
        versions: List[Version] = await settings.aiosqlembic_queries.get_version(
            connection
        )
    for version in versions:
        if version.is_applied:  # pragma: no cover
            return version
    return Version(version_id=-1, is_applied=False)


async def upTo(
    settings: AiosqlembicContext, version_id: int
) -> Tuple[List[int], Optional[Tuple[Exception, Optional[Path]]]]:
    revision_tree = get_revision_tree(
        settings.migration_directory, MIN_VERSION, version_id
    )
    revisions_applied = []
    error = None
    for _ in revision_tree:
        current: Version = await get_current(settings)
        next_revision = get_next_revision(revision_tree, current.version_id)
        if next_revision is not None:
            revision_query = aiosql.from_path(next_revision.file, settings.driver)
            async with get_connection(settings.driver, settings.dsn) as connection:
                try:
                    if settings.driver == "asyncpg":
                        async with connection.transaction():
                            result = await revision_query.up(connection)
                            logger.debug(f"up revision result: {result}")
                            await settings.aiosqlembic_queries.insert_revision(
                                connection,
                                version_id=next_revision.version_id,
                                is_applied=True,
                            )
                    elif settings.driver == "aiosqlite":
                        result = await revision_query.up(connection)
                        logger.debug(f"up revision result: {result}")
                        await settings.aiosqlembic_queries.insert_revision(
                            connection,
                            version_id=next_revision.version_id,
                            is_applied=1,
                        )
                    revisions_applied.append(next_revision.version_id)
                except Exception as e:
                    logger.error(e)
                    error = (e, next_revision.file)
    return revisions_applied, error


async def downTo(
    settings: AiosqlembicContext, version_id: int
) -> Tuple[List[int], Optional[Tuple[Exception, Optional[Path]]]]:
    revision_tree = get_revision_tree(
        settings.migration_directory, MIN_VERSION, MAX_VERSION
    )
    current: Version = await get_current(settings)
    current_revision = get_current_revision(revision_tree, current.version_id)
    revisions_applied = []
    error = None
    if current_revision is not None:
        revision_query = aiosql.from_path(current_revision.file, settings.driver)
        async with get_connection(settings.driver, settings.dsn) as connection:
            try:
                if settings.driver == "asyncpg":
                    async with connection.transaction():
                        result = await revision_query.down(connection)
                        logger.debug(f"down revision result: {result}")
                        await settings.aiosqlembic_queries.delete_revision(
                            connection, version_id=current_revision.version_id,
                        )
                elif settings.driver == "aiosqlite":
                    result = await revision_query.down(connection)
                    logger.debug(f"down revision result: {result}")
                    await settings.aiosqlembic_queries.delete_revision(
                        connection, version_id=current_revision.version_id,
                    )
                revisions_applied.append(current_revision.version_id)
            except Exception as e:
                error = (e, current_revision.file)
    return revisions_applied, error


@cli.command()
@pass_settings
async def up(settings: AiosqlembicContext) -> None:
    """Upgrade database to latest revision"""
    logger.debug(
        f"UP with debug: {settings.debug} - migrations: {settings.migration_directory} - driver: {settings.driver} - dsn: {settings.dsn}"
    )
    revisions_applied, error = await upTo(settings, MAX_VERSION)
    if error:
        click.echo(f"Errors in up: {error}")
    else:
        click.echo(f"Applied revisions up: {revisions_applied}")


@cli.command()
@pass_settings
async def down(settings: AiosqlembicContext) -> None:
    logger.debug(
        f"DOWN with debug: {settings.debug} - migrations: {settings.migration_directory} - driver: {settings.driver} - dsn: {settings.dsn}"
    )
    revisions_applied, error = await downTo(settings, MAX_VERSION)
    if error:
        click.echo(f"Errors in down: {error}")
    else:
        click.echo(f"Applied revisions down: {revisions_applied}")


def main() -> None:
    cli(_anyio_backend="asyncio")


if __name__ == "__main__":
    main()
