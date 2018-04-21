"""empty message

Revision ID: 510187f7afd6
Revises: 00f1b6b9b7a0
Create Date: 2018-04-21 21:08:53.800813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '510187f7afd6'
down_revision = '00f1b6b9b7a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('place', sa.Column('address', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('place', 'address')
    # ### end Alembic commands ###
