"""added complete date

Revision ID: 8a14828ceba5
Revises: 43075ef65d8a
Create Date: 2023-07-20 19:17:15.145201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a14828ceba5'
down_revision = '43075ef65d8a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('completed_at_time', sa.Date(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_column('completed_at_time')

    # ### end Alembic commands ###
