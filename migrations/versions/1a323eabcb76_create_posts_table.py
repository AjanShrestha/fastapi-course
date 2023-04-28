"""create posts table

Revision ID: 1a323eabcb76
Revises: 
Create Date: 2023-04-28 08:40:34.431036

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1a323eabcb76"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("posts")
