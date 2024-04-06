"""Added new table and ForeignKey

Revision ID: d5a26bf96eaa
Revises: c6cb4c526cb7
Create Date: 2024-04-02 12:05:43.982992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5a26bf96eaa'
down_revision = 'c6cb4c526cb7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bestilling',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ankomst', sa.Date(), nullable=False),
    sa.Column('avreise', sa.Date(), nullable=False),
    sa.Column('melding', sa.String(length=255), nullable=True),
    sa.Column('bestillings_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['bestillings_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bestilling')
    # ### end Alembic commands ###
