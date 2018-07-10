"""Changed ScheduleValve to include Hour and Minute

Revision ID: 29361040bdac
Revises: f33a35b6eb94
Create Date: 2018-07-10 10:02:57.087072

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29361040bdac'
down_revision = 'f33a35b6eb94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schedule_valve', sa.Column('startHour', sa.Integer(), nullable=True))
    op.add_column('schedule_valve', sa.Column('startMinute', sa.Integer(), nullable=True))
    op.drop_index('ix_schedule_valve_startTime', table_name='schedule_valve')
    op.drop_column('schedule_valve', 'startTime')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schedule_valve', sa.Column('startTime', sa.DATETIME(), nullable=True))
    op.create_index('ix_schedule_valve_startTime', 'schedule_valve', ['startTime'], unique=False)
    op.drop_column('schedule_valve', 'startMinute')
    op.drop_column('schedule_valve', 'startHour')
    # ### end Alembic commands ###
