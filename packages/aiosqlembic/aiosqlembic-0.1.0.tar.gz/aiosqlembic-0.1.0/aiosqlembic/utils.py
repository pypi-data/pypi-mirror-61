import json
import logging
import platform
import re
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Tuple, List, Any, AsyncGenerator
from urllib.parse import urlparse, urlunparse

import aiosql
import asyncpg
import jinja2
import toml
import typer
from asyncpg import Connection
from pydantic import SecretStr

import aiosqlembic
from aiosqlembic.models.cli import (
    DSN,
    AiosqlembicSettings,
    Migrations,
    Revision,
    RevisionPath,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

templateLoader = jinja2.FileSystemLoader(
    searchpath=str(Path(__file__).parent / "templates")
)
templateEnv = jinja2.Environment(loader=templateLoader)
aiosqlembic_queries = aiosql.from_path(
    Path(__file__).parent / "sql", "asyncpg", record_classes={"Revision": Revision}
)
REVISION_PATTERN = r"(?P<rev_number>.*)_(?P<rev_message>.*)\.sql"


def create_init_dir(
    migrations_directory_path: Path, config: Path, overwrite: bool = False
) -> None:
    """
    Utility to create a base configuration with a config toml file and a migrations directory
    """
    typer.echo("Create directory")
    migrations_directory_path.mkdir(exist_ok=overwrite)
    config_path = migrations_directory_path.parent / config
    config_path.touch()

    config_template = "config.toml"
    template = templateEnv.get_template(config_template)
    output = template.render(
        base_directory=migrations_directory_path.absolute()
    )  # this is where to put args to the template renderer
    config_path.write_text(output)


async def check_connection(dsn: str) -> bool:
    """
    Checks if the database connection is alive
    """
    try:
        conn = await asyncpg.connect(dsn, timeout=5)
        await conn.execute("select 1")
        await conn.close()
        return True
    except Exception as e:
        logger.error(e)
    return False


def get_dsn_from_config(toml_dsn: DSN) -> Tuple[str, str]:
    """
    Get the database dsn from the config, returns a tuple with the second item being the secret form that hides password
    """
    config_dsn: str = f"{toml_dsn.scheme}://{toml_dsn.user}:{toml_dsn.password}@{toml_dsn.host}:{toml_dsn.port}/{toml_dsn.db}"
    secretuser = SecretStr(toml_dsn.user)
    secretpassword = SecretStr(toml_dsn.password)
    secret_dsn = f"{toml_dsn.scheme}://{secretuser}:{secretpassword}@{toml_dsn.host}:{toml_dsn.port}/{toml_dsn.db}"
    return config_dsn, secret_dsn


def load_from_config(config: Path) -> AiosqlembicSettings:
    """
    Loads a toml config file to an AiosqlembicSettings
    """
    toml_content = toml.load(config)
    migrations = Migrations(**toml_content["migrations"])
    dsn = DSN(**toml_content["dsn"])
    settings = AiosqlembicSettings(migrations=migrations, dsn=dsn)
    return settings


def write_settings_to_config(config: Path, settings: AiosqlembicSettings) -> None:
    """
    Writes new settings to config path
    """
    new_toml_string = toml.dumps(json.loads(settings.json()))
    config.write_text(new_toml_string)


def get_list_revision(base_directory: Path) -> Tuple[int, List[Path]]:
    """
    Get the number and a list of sql revisions from the revisions directory
    """
    revisions = list(base_directory.glob("*.sql"))
    if revisions:
        return len(revisions), revisions
    else:
        return 0, revisions


def get_revision_tree(base_directory: Path) -> List[RevisionPath]:
    """
    Builds a list of RevisionPath from the revision directory
    """
    revision_files = list(base_directory.glob("*.sql"))
    revision_tree = []
    if revision_files:
        for revision_file in sorted(revision_files):
            m = re.match(REVISION_PATTERN, revision_file.name)
            if m is not None:
                revision = RevisionPath(
                    rev_number=int(m.group("rev_number")),
                    rev_message=m.group("rev_message"),
                    file=revision_file,
                )
                revision_tree.append(revision)
            else:
                raise ValueError("Wrong filename")
    else:
        revision_tree = [RevisionPath(rev_number=0, rev_message=None, file=None)]
    return revision_tree


def print_version(ctx: typer.Context, param: Any, value: str) -> None:
    """
    Prints the aiosqlembic version as well as python version and the plateform used
    """
    if not value or ctx.resilient_parsing:
        return
    typer.echo(
        "Running aiosqlembic %s with %s %s on %s"
        % (
            aiosqlembic.__version__,
            platform.python_implementation(),
            platform.python_version(),
            platform.system(),
        )
    )
    ctx.exit()


@asynccontextmanager
async def create_test_database(dsn: str, dbname: str) -> AsyncGenerator[str, None]:
    """Async context manager to create databases

    .. highlight:: python
    .. code-block:: python

        async with create_test_database(TEST_DSN, "d0") as d0, create_test_database(
            TEST_DSN, "d1"
        ) as d1:
            try:
                p0: Pool = await asyncpg.create_pool(dsn=d0)
                p1: Pool = await asyncpg.create_pool(dsn=d1)
                await p0.execute("select 1")
                await p1.execute("select 1")
            finally:
                await p1.close()
                await p0.close()

    """

    logger.debug(f"create_test_database: {dbname}")
    try:
        conn: Connection = await asyncpg.connect(dsn=dsn)
        response = await conn.execute(f"create database {dbname};")
        assert response == "CREATE DATABASE"
        logger.debug(f"yield create_test_database: {dbname}")
        parsed = urlparse(dsn)
        replaced = parsed._replace(path=dbname)
        dsn_unparse = urlunparse(replaced)
        yield dsn_unparse
        logger.debug(f"end yield create_test_database: {dbname}")
    finally:
        # drop database here
        logger.debug(f"finally create_test_database: {dbname}")
        response = await conn.execute(f"drop database {dbname};")
        await conn.close()
        assert response == "DROP DATABASE"
        logger.debug(f"end create_test_database: {dbname}")


# def get_reviduuid_from_files(existing: List[Path]) -> List[str]:
#     results = []
#     for e in existing:
#         m = re.match(REVISION_PATTERN, e.name)
#         assert m is not None
#         results.append(m.group("rev_number"))
#     return results
