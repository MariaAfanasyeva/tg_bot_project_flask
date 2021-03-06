"""changed to_bot field

Revision ID: 3b7ec315f2fe
Revises: 1ed440064be6
Create Date: 2021-07-19 14:43:40.003742

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "3b7ec315f2fe"
down_revision = "1ed440064be6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "bot", "create_time", existing_type=postgresql.TIMESTAMP(), nullable=False
    )
    op.alter_column(
        "bot",
        "update_time",
        existing_type=postgresql.TIMESTAMP(),
        nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "category", "create_time", existing_type=postgresql.TIMESTAMP(), nullable=False
    )
    op.alter_column(
        "category",
        "update_time",
        existing_type=postgresql.TIMESTAMP(),
        nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.add_column("comment", sa.Column("to_bot_id", sa.Integer(), nullable=False))
    op.alter_column(
        "comment", "create_time", existing_type=postgresql.TIMESTAMP(), nullable=False
    )
    op.alter_column(
        "comment",
        "update_time",
        existing_type=postgresql.TIMESTAMP(),
        nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.drop_constraint("comment_to_bot_fkey", "comment", type_="foreignkey")
    op.create_foreign_key(
        None, "comment", "bot", ["to_bot_id"], ["id"], ondelete="CASCADE"
    )
    op.drop_column("comment", "to_bot")
    op.alter_column(
        "user", "create_time", existing_type=postgresql.TIMESTAMP(), nullable=False
    )
    op.alter_column(
        "user",
        "update_time",
        existing_type=postgresql.TIMESTAMP(),
        nullable=False,
        existing_server_default=sa.text("now()"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "user",
        "update_time",
        existing_type=postgresql.TIMESTAMP(),
        nullable=True,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "user", "create_time", existing_type=postgresql.TIMESTAMP(), nullable=True
    )
    op.add_column(
        "comment",
        sa.Column("to_bot", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "comment", type_="foreignkey")
    op.create_foreign_key(
        "comment_to_bot_fkey", "comment", "bot", ["to_bot"], ["id"], ondelete="CASCADE"
    )
    op.alter_column(
        "comment",
        "update_time",
        existing_type=postgresql.TIMESTAMP(),
        nullable=True,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "comment", "create_time", existing_type=postgresql.TIMESTAMP(), nullable=True
    )
    op.drop_column("comment", "to_bot_id")
    op.alter_column(
        "category",
        "update_time",
        existing_type=postgresql.TIMESTAMP(),
        nullable=True,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "category", "create_time", existing_type=postgresql.TIMESTAMP(), nullable=True
    )
    op.alter_column(
        "bot",
        "update_time",
        existing_type=postgresql.TIMESTAMP(),
        nullable=True,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "bot", "create_time", existing_type=postgresql.TIMESTAMP(), nullable=True
    )
    # ### end Alembic commands ###
