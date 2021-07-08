"""changed abstract model

Revision ID: ab18c512901f
Revises: 812820c518d3
Create Date: 2021-07-08 13:55:12.799623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab18c512901f'
down_revision = '812820c518d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('update_date', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.add_column('bot', sa.Column('create_date', sa.DateTime(), nullable=True))
    op.add_column('bot', sa.Column('update_date', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    op.add_column('category', sa.Column('create_date', sa.DateTime(), nullable=True))
    op.add_column('category', sa.Column('update_date', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('category', 'update_date')
    op.drop_column('category', 'create_date')
    op.drop_column('bot', 'update_date')
    op.drop_column('bot', 'create_date')
    op.drop_table('user')
    # ### end Alembic commands ###
