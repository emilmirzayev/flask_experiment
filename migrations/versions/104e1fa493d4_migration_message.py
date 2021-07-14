"""migration message

Revision ID: 104e1fa493d4
Revises: 
Create Date: 2021-07-13 11:41:22.951493

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '104e1fa493d4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events',
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.String(), nullable=False),
    sa.Column('event_type', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('performances',
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.String(), nullable=False),
    sa.Column('objective_score', sa.Float(), nullable=False),
    sa.Column('performance_score', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('performances')
    op.drop_table('events')
    # ### end Alembic commands ###
