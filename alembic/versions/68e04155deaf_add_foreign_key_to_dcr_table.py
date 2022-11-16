"""add foreign key to DCR table

Revision ID: 68e04155deaf
Revises: 9217a0c63d1c
Create Date: 2022-11-13 17:54:34.674515

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68e04155deaf'
down_revision = '9217a0c63d1c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("DCR", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("dcr_users_fk", source_table="DCR", referent_table="users", local_cols=['owner_id'],
    remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('dcr_users_fk', table_name="DCR")
    op.drop_column("DCR", "owner_id")
    pass
