"""Email migrations

Revision ID: 4739c91df8ab
Revises: 55e8ee90ff8a
Create Date: 2024-05-30 12:38:54.960280

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4739c91df8ab'
down_revision = '55e8ee90ff8a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('unit_sector')
    # op.drop_table('unit_customer')
    # ### end Alembic commands ###  
    pass

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('unit_customer',
    sa.Column('unit_id', sa.INTEGER(), server_default=sa.text("nextval('unit_customer_unit_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('customer_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], name='unit_customer_customer_id_fkey'),
    sa.PrimaryKeyConstraint('unit_id', name='unit_customer_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('unit_sector',
    sa.Column('unit_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('sector_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['unit_id'], ['unit_customer.unit_id'], name='unit_sector_unit_id_fkey'),
    sa.PrimaryKeyConstraint('unit_id', name='unit_sector_pkey')
    )
    # ### end Alembic commands ###
