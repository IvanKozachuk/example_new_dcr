"""create DCR table

Revision ID: cba6b752368d
Revises: 
Create Date: 2022-11-13 17:02:09.767321

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cba6b752368d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('DCR', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
     sa.Column('language', sa.String(), nullable=False), sa.Column('ticket_number', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('DCR')
    pass
