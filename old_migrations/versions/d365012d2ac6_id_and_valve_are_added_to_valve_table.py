"""id and valve are added to Valve table

Revision ID: d365012d2ac6
Revises: 6c3fc3787eb9
Create Date: 2018-07-09 11:50:56.329986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd365012d2ac6'
down_revision = '6c3fc3787eb9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('valve', sa.Column('valve', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('valve', 'valve')
    # ### end Alembic commands ###
