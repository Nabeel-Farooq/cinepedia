#!/usr/bin/env python3

from pathlib import Path
import logging
import sys
import types

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


def get_current_version() -> int:
    """
    Return current database migration version.
    """

    return api.db_version(
        SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_MIGRATE_REPO
    )


def generate_migration_path(version: int) -> Path:
    """
    Generate migration file path.
    """

    return (
        Path(SQLALCHEMY_MIGRATE_REPO)
        / 'versions'
        / f'{version:03d}_migration.py'
    )


def load_old_model_metadata():
    """
    Load metadata from previous migration state.
    """

    old_model = api.create_model(
        SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_MIGRATE_REPO
    )

    module = types.ModuleType('old_model')

    exec(old_model, module.__dict__)

    return module.meta


def create_migration_script(migration_path: Path) -> None:
    """
    Create migration script from model changes.
    """

    old_metadata = load_old_model_metadata()

    script = api.make_update_script_for_model(
        SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_MIGRATE_REPO,
        old_metadata,
        db.metadata
    )

    migration_path.write_text(
        script,
        encoding='utf-8'
    )


def upgrade_database() -> int:
    """
    Upgrade database and return latest version.
    """

    api.upgrade(
        SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_MIGRATE_REPO
    )

    return get_current_version()


def migrate_database() -> None:
    """
    Generate and apply database migration.
    """

    try:
        current_version = get_current_version()
        next_version = current_version + 1

        migration_path = generate_migration_path(
            next_version
        )

        create_migration_script(migration_path)

        logger.info(
            f'Migration script created: {migration_path}'
        )

        upgraded_version = upgrade_database()

        logger.info(
            'Database upgraded successfully '
            f'to version {upgraded_version}'
        )

    except Exception as error:
        logger.exception(
            f'Failed to generate migration: {error}'
        )
        sys.exit(1)


if __name__ == '__main__':
    migrate_database()
