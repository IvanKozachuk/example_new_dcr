"""add user table

Revision ID: 9217a0c63d1c
Revises: 49e84c903686
Create Date: 2022-11-13 17:33:01.296413

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9217a0c63d1c'
down_revision = '49e84c903686'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True),
        server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email")
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
