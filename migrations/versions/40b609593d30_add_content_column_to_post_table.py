"""add content column to post table

Revision ID: 40b609593d30
Revises: 1a323eabcb76
Create Date: 2023-04-28 08:49:24.715163

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "40b609593d30"
down_revision = "1a323eabcb76"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
