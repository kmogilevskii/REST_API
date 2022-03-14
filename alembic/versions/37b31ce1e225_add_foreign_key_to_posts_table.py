"""add foreign key to posts table

Revision ID: 37b31ce1e225
Revises: be315c3d2097
Create Date: 2022-03-13 20:43:32.767715

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37b31ce1e225'
down_revision = 'be315c3d2097'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("posts_users_fk", source_table="posts", 
                                            referent_table="users", 
                                            local_cols=["owner_id"], 
                                            remote_cols=["id"],
                                            ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
