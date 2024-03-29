"""add_repeat_column_to_question_group_and_answer_table

Revision ID: 8cd69d641604
Revises: 19c05e6b7198
Create Date: 2023-09-14 04:35:33.215673

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8cd69d641604"
down_revision = "19c05e6b7198"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "question_group",
        sa.Column("repeatable", sa.Boolean(), nullable=False, default=False),
    )
    op.add_column(
        "answer",
        sa.Column("repeat", sa.Integer(), nullable=True, default=0),
    )


def downgrade() -> None:
    op.drop_column("question_group", "repeatable")
    op.drop_column("answer", "repeat")
