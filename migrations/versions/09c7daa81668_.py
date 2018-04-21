"""empty message

Revision ID: 09c7daa81668
Revises: 96138c7323ad
Create Date: 2018-04-21 17:53:29.915810

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09c7daa81668'
down_revision = '96138c7323ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('place', sa.Column('is_place_tippting_available', sa.Boolean(), nullable=False, default=True))
    op.add_column('place', sa.Column('is_tipping_available', sa.Boolean(), nullable=False, default=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('place', 'is_tipping_available')
    op.drop_column('place', 'is_place_tippting_available')
    # ### end Alembic commands ###
