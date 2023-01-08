"""init_database

Revision ID: b58990633204
Revises:
Create Date: 2023-01-08 23:21:21.020805

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

# revision identifiers, used by Alembic.
revision = 'b58990633204'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Form
    op.create_table('form', sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String()),
                    sa.PrimaryKeyConstraint('id'))
    op.create_index(op.f('ix_form_id'), 'form', ['id'], unique=True)
    # Question Group
    op.create_table(
        'question_group',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order', sa.Integer(), default=None),
        sa.Column('name', sa.String()),
        sa.Column('form', sa.Integer(), sa.ForeignKey('form.id')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['form'], ['form.id'],
                                name='form_question_group_constraint',
                                ondelete='CASCADE'),
    )
    op.create_index(op.f('ix_question_group_id'),
                    'question_group', ['id'],
                    unique=True)
    # Question Table
    op.create_table(
        'question',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order', sa.Integer(), default=None),
        sa.Column('name', sa.String()),
        sa.Column('form', sa.Integer(), sa.ForeignKey('form.id')),
        sa.Column(
            'type',
            sa.Enum('text',
                    'number',
                    'option',
                    'multiple_option',
                    'photo',
                    'date',
                    'geo',
                    'administration',
                    name='questiontype')),
        sa.Column('question_group', sa.Integer(),
                  sa.ForeignKey('question_group.id')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['form'], ['form.id'],
                                name='form_question_constraint',
                                ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['question_group'], ['question_group.id'],
                                name='question_group_question_constraint',
                                ondelete='CASCADE'),
    )
    op.create_index(op.f('ix_question_id'), 'question', ['id'], unique=True)
    # Option Table
    op.create_table(
        'option',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order', sa.Integer(), default=None),
        sa.Column('name', sa.String()),
        sa.Column('question', sa.Integer(), sa.ForeignKey('question.id')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['question'], ['question.id'],
                                name='question_option_constraint',
                                ondelete='CASCADE'),
    )
    op.create_index(op.f('ix_option_id'), 'option', ['id'], unique=True)

    # Data Table
    op.create_table(
        'data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('form', sa.Integer(), sa.ForeignKey('form.id')),
        sa.Column('created',
                  sa.DateTime(),
                  nullable=True,
                  server_default=sa.text('(CURRENT_TIMESTAMP)')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['form'], ['form.id'],
                                name='form_data_constraint',
                                ondelete='CASCADE'),
    )
    op.create_index(op.f('ix_data_id'), 'data', ['id'], unique=True)

    # Answer Table
    op.create_table(
        'answer',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('question', sa.Integer(), sa.ForeignKey('question.id')),
        sa.Column('data', sa.Integer(), sa.ForeignKey('data.id')),
        sa.Column('value', sa.Float(), nullable=True),
        sa.Column('text', sa.Text(), nullable=True),
        sa.Column('options', pg.ARRAY(sa.String()), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['question'], ['question.id'],
                                name='question_answer_constraint',
                                ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['data'], ['data.id'],
                                name='data_answer_constraint',
                                ondelete='CASCADE'),
    )
    op.create_index(op.f('ix_answer_id'), 'answer', ['id'], unique=True)


def downgrade() -> None:
    # Drop Answer
    op.drop_index(op.f('ix_answer_id'), table_name='answer')
    op.drop_table('answer')
    # Drop Data
    op.drop_index(op.f('ix_data_id'), table_name='data')
    op.drop_table('data')
    # Drop Option
    op.drop_index(op.f('ix_option_id'), table_name='option')
    op.drop_table('option')
    # Drop Question
    op.drop_index(op.f('ix_question_id'), table_name='question')
    op.drop_table('question')
    op.execute('DROP TYPE questiontype')
    # Drop Question Group
    op.drop_index(op.f('ix_question_group_id'), table_name='question_group')
    op.drop_table('question_group')
    # Drop Form
    op.drop_index(op.f('ix_form_id'), table_name='form')
    op.drop_table('form')
