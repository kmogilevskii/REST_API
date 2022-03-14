"""add content column to posts table

Revision ID: 389687da2ad2
Revises: a86bdfe9b707
Create Date: 2022-03-13 20:30:59.864235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '389687da2ad2'
down_revision = 'a86bdfe9b707'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
