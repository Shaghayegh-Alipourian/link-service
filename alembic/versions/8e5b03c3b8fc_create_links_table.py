from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "8e5b03c3b8fc"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: str | None = None


def upgrade() -> None:
    op.create_table(
        "links",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("original_url", sa.String(), nullable=False),
        sa.Column("short_code", sa.String(), nullable=False),
        sa.Column("clicks", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("short_code"),
    )


def downgrade() -> None:
    op.drop_table("links")