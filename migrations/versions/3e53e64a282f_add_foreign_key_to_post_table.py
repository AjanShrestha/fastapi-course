"""add foreign-key to post table

Revision ID: 3e53e64a282f
Revises: 3c18797f05da
Create Date: 2023-04-28 15:39:08.471117

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3e53e64a282f"
down_revision = "3c18797f05da"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "post_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
