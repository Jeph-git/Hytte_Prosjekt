"""Changed primary key

Revision ID: 644f7af43255
Revises: 866b33f85acc
Create Date: 2024-04-23 13:56:23.293201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '644f7af43255'
down_revision = '866b33f85acc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('governor_user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('governor_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['governor_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('governor_user')
    # ### end Alembic commands ###
