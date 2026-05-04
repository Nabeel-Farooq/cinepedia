#!/usr/bin/env python3

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO
from app import db
from pathlib import Path


def main():
    repo_path = Path(SQLALCHEMY_MIGRATE_REPO)

    # Create database tables
    db.create_all()

    if not repo_path.exists():
        api.create(str(repo_path), "database repository")
        api.version_control(SQLALCHEMY_DATABASE_URI, str(repo_path))
        print("Migration repository created.")
    else:
        current_version = api.version(str(repo_path))
        api.version_control(
            SQLALCHEMY_DATABASE_URI,
            str(repo_path),
            current_version
        )
        print(f"Database under version control (version: {current_version})")


if __name__ == "__main__":
    main()
