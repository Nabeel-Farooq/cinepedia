#!/usr/bin/env python3

from pathlib import Path
import logging
import sys

from migrate.versioning import api

from app import db
from config import (
    SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_MIGRATE_REPO,
)

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)

logger = logging.getLogger(__name__)


def create_database_tables() -> None:
    """
    Create database tables if they do not exist.
    """

    db.create_all()
    logger.info('Database tables initialized')


def create_migration_repository(repo_path: Path) -> None:
    """
    Create migration repository and enable version control.
    """

    api.create(
        str(repo_path),
        'database repository'
    )

    api.version_control(
        SQLALCHEMY_DATABASE_URI,
        str(repo_path)
    )

    logger.info(
        'Migration repository created and version control initialized'
    )


def get_database_version(repo_path: Path) -> int:
    """
    Get current database migration version.
    """

    return api.db_version(
        SQLALCHEMY_DATABASE_URI,
        str(repo_path)
    )


def init_migrations() -> None:
    """
    Initialize migration system safely.
    """

    repo_path = Path(SQLALCHEMY_MIGRATE_REPO)

    try:
        create_database_tables()

        if not repo_path.exists():
            create_migration_repository(repo_path)
            return

        version = get_database_version(repo_path)

        logger.info(
            'Database already under version control '
            f'(version: {version})'
        )

    except Exception as error:
        logger.exception(
            f'Failed to initialize migrations: {error}'
        )
        sys.exit(1)


if __name__ == '__main__':
    init_migrations()
