"""add source column to DCR table

Revision ID: 49e84c903686
Revises: cba6b752368d
Create Date: 2022-11-13 17:14:57.263734

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49e84c903686'
down_revision = 'cba6b752368d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("DCR", sa.Column("source", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("DCR", "source")
    pass
