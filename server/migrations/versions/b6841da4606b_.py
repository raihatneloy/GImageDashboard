"""empty message

Revision ID: b6841da4606b
Revises: b333511c286c
Create Date: 2017-12-13 21:07:13.606696

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6841da4606b'
down_revision = 'b333511c286c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('_500px',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=1000), nullable=True),
    sa.Column('name', sa.String(length=1000), nullable=True),
    sa.Column('_500pxid', sa.String(length=1000), nullable=True),
    sa.Column('picture', sa.String(length=1000), nullable=True),
    sa.Column('cover', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pinned_500px',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('_500pxid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['_500pxid'], ['_500px.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pinned_500px')
    op.drop_table('_500px')
    # ### end Alembic commands ###