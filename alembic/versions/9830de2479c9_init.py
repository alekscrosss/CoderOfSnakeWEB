"""Init

Revision ID: 9830de2479c9
Revises: 
Create Date: 2024-02-23 13:34:24.230975

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9830de2479c9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('refresh_token', sa.String(length=255), nullable=True),
    sa.Column('role', sa.Enum('user', 'admin', 'moderator', name='role'), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.Column('status_ban', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('photos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_photos_filename'), 'photos', ['filename'], unique=False)
    op.create_index(op.f('ix_photos_id'), 'photos', ['id'], unique=False)
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('photo_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['photo_id'], ['photos.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    op.drop_index(op.f('ix_photos_id'), table_name='photos')
    op.drop_index(op.f('ix_photos_filename'), table_name='photos')
    op.drop_table('photos')
    op.drop_table('users')
    # ### end Alembic commands ###
