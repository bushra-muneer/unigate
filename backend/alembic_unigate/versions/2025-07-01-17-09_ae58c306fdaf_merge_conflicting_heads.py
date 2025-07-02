"""merge conflicting heads

Revision ID: ae58c306fdaf
Revises: 137ad5ca1e5b, 1a5833755e2e
Create Date: 2025-07-01 17:09:12.120103

"""
from collections.abc import Sequence

import sqlalchemy as sa

# see https://stackoverflow.com/a/69063829 for sqlmodel
import sqlmodel
import sqlmodel.sql.sqltypes  # noqa: F401
from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'ae58c306fdaf'
down_revision: str | None = ('137ad5ca1e5b', '1a5833755e2e')
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
