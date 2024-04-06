"""Rename email column to phoneNumber

Revision ID: 75ac09650cc4
Revises: Previous_revision_id
Create Date: 2022-03-28 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75ac09650cc4'
down_revision = '25c283d3c01e'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('email', new_column_name='phoneNumber')


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('phoneNumber', new_column_name='email')
