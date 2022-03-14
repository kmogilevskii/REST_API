"""additional columns to post table

Revision ID: 79e478d3de8a
Revises: 37b31ce1e225
Create Date: 2022-03-13 20:48:02.415827

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79e478d3de8a'
down_revision = '37b31ce1e225'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), 
                                                   nullable=False, 
                                                   server_default=sa.text("NOW()")))
    pass


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
