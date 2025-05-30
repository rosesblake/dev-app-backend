"""add slug fields

Revision ID: d41f0be4bc28
Revises: 
Create Date: 2025-05-16 13:09:35.257154

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd41f0be4bc28'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('projects', sa.Column('slug', sa.String(), nullable=True))
    op.create_index(op.f('ix_projects_slug'), 'projects', ['slug'], unique=True)
    op.add_column('users', sa.Column('slug', sa.String(), nullable=True))
    op.drop_index('ix_users_email', table_name='users')
    op.create_index(op.f('ix_users_slug'), 'users', ['slug'], unique=True)
    op.create_unique_constraint(None, 'users', ['email'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_index(op.f('ix_users_slug'), table_name='users')
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.drop_column('users', 'slug')
    op.drop_index(op.f('ix_projects_slug'), table_name='projects')
    op.drop_column('projects', 'slug')
    # ### end Alembic commands ###
