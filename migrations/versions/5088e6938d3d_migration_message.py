"""migration message

Revision ID: 5088e6938d3d
Revises: 104e1fa493d4
Create Date: 2021-07-13 13:50:16.889013

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5088e6938d3d'
down_revision = '104e1fa493d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('choices',
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.String(), nullable=False),
    sa.Column('X', sa.Integer(), nullable=False),
    sa.Column('Y', sa.Integer(), nullable=False),
    sa.Column('Z', sa.Integer(), nullable=False),
    sa.Column('F', sa.Integer(), nullable=False),
    sa.Column('V', sa.Integer(), nullable=False),
    sa.Column('objective_score', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('choices')
    # ### end Alembic commands ###
