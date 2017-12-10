"""empty message

Revision ID: 2677367a4563
Revises: 6ce156ae116e
Create Date: 2017-12-10 21:13:46.992633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2677367a4563'
down_revision = '6ce156ae116e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=1000), nullable=True),
    sa.Column('page_id', sa.String(length=1000), nullable=True),
    sa.Column('cover', sa.String(length=1000), nullable=True),
    sa.Column('picture', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pinned_pages',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('page_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['page_id'], ['pages.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pinned_pages')
    op.drop_table('pages')
    # ### end Alembic commands ###
