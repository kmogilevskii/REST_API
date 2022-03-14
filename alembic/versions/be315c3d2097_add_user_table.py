"""add user table

Revision ID: be315c3d2097
Revises: 389687da2ad2
Create Date: 2022-03-13 20:36:06.444697

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be315c3d2097'
down_revision = '389687da2ad2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users", sa.Column("id", sa.Integer(), nullable=False),
                             sa.Column("email", sa.String(), nullable=False),
                             sa.Column("password", sa.String(), nullable=False),
                             sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                                                     server_default=sa.text("NOW()"), nullable=False),
                            sa.PrimaryKeyConstraint("id"),
                            sa.UniqueConstraint("email"))
    pass


def downgrade():
    op.drop_table("users")
    pass
