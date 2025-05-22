from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "286ade602d14"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True, index=True),
        sa.Column("email", sa.String(), nullable=False, unique=True, index=True),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )

    # Create readers table
    op.create_table(
        "readers",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True, index=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False, unique=True, index=True),
        sa.UniqueConstraint("email", name="uq_readers_email"),
    )

    # Create books table
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True, index=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("author", sa.String(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("isbn", sa.String(), nullable=False, unique=True, index=True),
        sa.Column("copies_available", sa.Integer(), nullable=False, server_default="1"),
        sa.UniqueConstraint("title", name="uq_books_title"),
        sa.CheckConstraint("copies_available >= 0", name="ck_books_copies_nonnegative"),
    )

    # Create borrowed_books table
    op.create_table(
        "borrowed_books",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True, index=True),
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column("reader_id", sa.Integer(), nullable=False),
        sa.Column(
            "borrow_date",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("return_date", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["reader_id"], ["readers.id"], ondelete="CASCADE"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("borrowed_books")
    op.drop_table("books")
    op.drop_table("readers")
    op.drop_table("users")
