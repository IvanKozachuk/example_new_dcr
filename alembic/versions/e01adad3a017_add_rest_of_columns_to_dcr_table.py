"""add rest of columns to DCR table

Revision ID: e01adad3a017
Revises: 68e04155deaf
Create Date: 2022-11-14 15:18:02.488452

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e01adad3a017'
down_revision = '68e04155deaf'
branch_labels = None
depends_on = None

# calls = Column(Integer, server_default="0")
#   emails = Column(Integer, server_default="0")
#   chats = Column(Integer, server_default="0")
# created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()')

def upgrade() -> None:
    op.add_column("DCR", sa.Column("calls", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("DCR", sa.Column("emails", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("DCR", sa.Column("chats", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("DCR", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default='now()'))
    pass


def downgrade() -> None:
    op.drop_column("DCR", "calls")
    op.drop_column("DCR", "chats")
    op.drop_column("DCR", "emails")
    op.drop_column("DCR", "created_at")
    pass
