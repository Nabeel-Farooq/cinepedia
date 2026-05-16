#!/usr/bin/env python3

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO


def upgrade_database() -> None:
    """
    Upgrade the database to the latest migration version
    and print the current version.
    """

    try:
        # Upgrade DB to latest available migration
        api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

        # Fetch current DB version
        version = api.db_version(
            SQLALCHEMY_DATABASE_URI,
            SQLALCHEMY_MIGRATE_REPO,
        )

        print(f"Current database version: {version}")

    except Exception as error:
        print(f"[MIGRATION ERROR] {error}")


if __name__ == "__main__":
    upgrade_database()
