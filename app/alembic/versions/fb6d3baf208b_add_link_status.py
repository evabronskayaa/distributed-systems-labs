"""add link status

Revision ID: fb6d3baf208b
Revises: be7ddf07183e
Create Date: 2023-11-11 23:02:56.769078

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb6d3baf208b'
down_revision = 'be7ddf07183e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('links', sa.Column('status', sa.String(), nullable=True))
    op.alter_column('links', 'url',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('links', 'url',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('links', 'status')
    # ### end Alembic commands ###
