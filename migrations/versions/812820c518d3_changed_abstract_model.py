"""changed abstract model

Revision ID: 812820c518d3
Revises: 27c571b334e7
Create Date: 2021-07-08 13:38:02.442953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '812820c518d3'
down_revision = '27c571b334e7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('bot_id_fkey', 'bot', type_='foreignkey')
    op.create_foreign_key(None, 'bot', 'base_model', ['id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('category_id_fkey', 'category', type_='foreignkey')
    op.create_foreign_key(None, 'category', 'base_model', ['id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'category', type_='foreignkey')
    op.create_foreign_key('category_id_fkey', 'category', 'base_model', ['id'], ['id'])
    op.drop_constraint(None, 'bot', type_='foreignkey')
    op.create_foreign_key('bot_id_fkey', 'bot', 'base_model', ['id'], ['id'])
    # ### end Alembic commands ###
