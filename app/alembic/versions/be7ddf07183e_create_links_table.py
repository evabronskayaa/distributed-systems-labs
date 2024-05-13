"""create links table

Revision ID: be7ddf07183e
Revises: 
Create Date: 2023-11-07 23:36:52.906991

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be7ddf07183e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'links',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('url', sa.String(), nullable=False)
    )


def downgrade():
    pass
