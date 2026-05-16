#!/usr/bin/env python3

from pathlib import Path

from migrate.versioning import api

from app import db
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO


def init_migrations() -> None:
    """
    Initialize migration repository and database version control.
    """

    repo_path = Path(SQLALCHEMY_MIGRATE_REPO)

    try:
        # Ensure tables exist before migration tracking
        db.create_all()

        # Create migration repo if it doesn't exist
        if not repo_path.exists():
            api.create(str(repo_path), "database repository")

            api.version_control(
                SQLALCHEMY_DATABASE_URI,
                str(repo_path),
            )

            print("Migration repository created and version control initialized.")
            return

        # Existing repo: ensure version control is set
        version = api.db_version(
            SQLALCHEMY_DATABASE_URI,
            str(repo_path),
        )

        print(f"Database already under version control (version: {version})")

    except Exception as error:
        print(f"[INIT MIGRATION ERROR] {error}")


if __name__ == "__main__":
    init_migrations()
