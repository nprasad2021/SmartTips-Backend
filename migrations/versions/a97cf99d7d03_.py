"""empty message

Revision ID: a97cf99d7d03
Revises: 556b1501607e
Create Date: 2018-04-22 03:26:08.890773

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a97cf99d7d03'
down_revision = '556b1501607e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('place', sa.Column('here_id', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('place', 'here_id')
    # ### end Alembic commands ###
