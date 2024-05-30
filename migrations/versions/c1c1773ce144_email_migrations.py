"""Email migrations

Revision ID: c1c1773ce144
Revises: 0173ae5999f9
Create Date: 2024-05-30 12:17:17.007496

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1c1773ce144'
down_revision = '0173ae5999f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('unit_customer')
    # op.drop_table('unit_sector')
    # ### end Alembic commands ###
    pass


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('unit_sector',
    sa.Column('unit_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('sector_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['unit_id'], ['unit_customer.unit_id'], name='unit_sector_unit_id_fkey'),
    sa.PrimaryKeyConstraint('unit_id', name='unit_sector_pkey')
    )
    op.create_table('unit_customer',
    sa.Column('unit_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('customer_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], name='unit_customer_customer_id_fkey'),
    sa.PrimaryKeyConstraint('unit_id', name='unit_customer_pkey')
    )
    # ### end Alembic commands ###