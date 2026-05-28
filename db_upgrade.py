#!/usr/bin/env python3

import logging
import sys

from migrate.versioning import api

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


def upgrade_database() -> None:
    """
    Upgrade database to the latest migration version.
    """

    try:
        current_version = get_current_version()

        logger.info(
            f'Current database version: {current_version}'
        )

        api.upgrade(
            SQLALCHEMY_DATABASE_URI,
            SQLALCHEMY_MIGRATE_REPO
        )

        upgraded_version = get_current_version()

        if upgraded_version == current_version:
            logger.info(
                'Database is already up to date'
            )
            return

        logger.info(
            'Database upgraded successfully '
            f'from version {current_version} '
            f'to {upgraded_version}'
        )

    except Exception as error:
        logger.exception(
            f'Failed to upgrade database: {error}'
        )
        sys.exit(1)


if __name__ == '__main__':
    upgrade_database()
