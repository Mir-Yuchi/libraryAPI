"""add book.description

Revision ID: b21c7c7c6ed6
Revises: 286ade602d14
Create Date: 2025-05-23 18:04:41.056332

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b21c7c7c6ed6"
down_revision: Union[str, None] = "286ade602d14"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "books",
        sa.Column("description", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("books", "description")
