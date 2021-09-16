"""Added field 'add_by_user' into Bot model

Revision ID: f958ac70bc4d
Revises: b9c061d9863e
Create Date: 2021-07-13 13:21:27.242279

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f958ac70bc4d"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("bot", sa.Column("add_by_user", sa.Integer(), nullable=True))
    op.create_foreign_key(
        None, "bot", "user", ["add_by_user"], ["id"], ondelete="SET NULL"
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "bot", type_="foreignkey")
    op.drop_column("bot", "add_by_user")
    # ### end Alembic commands ###