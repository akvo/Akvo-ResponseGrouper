"""add_dependency_column

Revision ID: 19c05e6b7198
Revises: b58990633204
Create Date: 2023-02-09 04:29:56.166504

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg


# revision identifiers, used by Alembic.
revision = "19c05e6b7198"
down_revision = "b58990633204"
branch_labels = None
depends_on = None


class CastingArray(pg.ARRAY):
    def bind_expression(self, bindvalue):
        return sa.cast(bindvalue, self)


def upgrade() -> None:
    op.add_column(
        "question",
        sa.Column("dependency", CastingArray(pg.JSONB()), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("question", "dependency")
