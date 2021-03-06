"""Added model Like

Revision ID: 4d89a34f8904
Revises: 3b7ec315f2fe
Create Date: 2021-07-29 12:28:39.692678

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4d89a34f8904"
down_revision = "3b7ec315f2fe"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "like",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("create_time", sa.DateTime(), nullable=False),
        sa.Column(
            "update_time",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("to_bot_id", sa.Integer(), nullable=False),
        sa.Column("add_by_user", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["add_by_user"], ["user.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["to_bot_id"], ["bot.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("like")
    # ### end Alembic commands ###
