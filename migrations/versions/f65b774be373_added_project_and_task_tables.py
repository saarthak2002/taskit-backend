"""added project and task tables

Revision ID: f65b774be373
Revises: 5de77374d48e
Create Date: 2023-07-19 12:05:38.414302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f65b774be373'
down_revision = '5de77374d48e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('project_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'project', ['project_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('project_id')

    # ### end Alembic commands ###
