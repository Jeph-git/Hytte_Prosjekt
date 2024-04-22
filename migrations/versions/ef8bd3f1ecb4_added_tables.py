"""added tables

Revision ID: ef8bd3f1ecb4
Revises: fbe563daf138
Create Date: 2024-04-15 10:36:08.412618

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef8bd3f1ecb4'
down_revision = 'fbe563daf138'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('unit_customer', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'customers', ['customer_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('unit_customer', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###
