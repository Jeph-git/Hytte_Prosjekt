"""changed user_customer table, changed primary key

Revision ID: 866b33f85acc
Revises: fbff3cea48d0
Create Date: 2024-04-23 10:37:01.357702

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '866b33f85acc'
down_revision = 'fbff3cea48d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_customer',
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('customer_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_customer')
    # ### end Alembic commands ###