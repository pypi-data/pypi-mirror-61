from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, BaseModel


class DSN(BaseModel):
    scheme: str
    user: str
    password: str
    host: str
    port: str
    db: str


class Migrations(BaseModel):
    base_directory: Path


class AiosqlembicSettings(BaseSettings):
    migrations: Migrations
    dsn: DSN


class Revision(BaseModel):
    rev_number: int
    rev_message: Optional[str]


class RevisionPath(Revision):
    file: Optional[Path]
