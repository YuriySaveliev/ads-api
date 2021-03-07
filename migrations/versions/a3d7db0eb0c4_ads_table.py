"""ads table

Revision ID: a3d7db0eb0c4
Revises: 
Create Date: 2021-02-21 22:11:45.588663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3d7db0eb0c4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ads',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('description', sa.String(length=8128), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('bids', sa.Integer(), nullable=True),
    sa.Column('create_date', sa.String(length=128), nullable=True),
    sa.Column('image_url', sa.String(length=256), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ads')
    # ### end Alembic commands ###