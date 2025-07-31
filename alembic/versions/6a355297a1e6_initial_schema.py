"""Initial schema

Revision ID: 6a355297a1e6
Revises: 
Create Date: 2025-07-30 20:14:07.066673

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a355297a1e6'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Створення таблиці груп
    op.create_table(
        'user_groups',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(length=50), nullable=False, unique=True),
    )

    # Створення таблиці користувачів
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.Column('hashed_password', sa.String, nullable=False),
        sa.Column('is_active', sa.Boolean, nullable=False, default=False),
        sa.Column('group_id', sa.Integer, sa.ForeignKey('user_groups.id'), nullable=False),
    )

    # Створення таблиці профілю
    op.create_table(
        'profiles',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('full_name', sa.String, nullable=True),
        sa.Column('bio', sa.Text, nullable=True),
        sa.Column('birth_date', sa.Date, nullable=True),
    )

    # Токен активації
    op.create_table(
        'activation_tokens',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('token', sa.String, nullable=False, unique=True),
        sa.Column('expires_at', sa.DateTime, nullable=False),
    )

    # Токени оновлення
    op.create_table(
        'refresh_tokens',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('token', sa.String, nullable=False, unique=True),
        sa.Column('expires_at', sa.DateTime, nullable=False),
    )

    # Токени скидання пароля
    op.create_table(
        'password_reset_tokens',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('token', sa.String, nullable=False, unique=True),
        sa.Column('expires_at', sa.DateTime, nullable=False),
    )

    # Сідимо групи
    op.execute("INSERT INTO user_groups (id, name) VALUES (1, 'USER'), (2, 'ADMIN')")


def downgrade() -> None:
    op.drop_table('password_reset_tokens')
    op.drop_table('refresh_tokens')
    op.drop_table('activation_tokens')
    op.drop_table('profiles')
    op.drop_table('users')
    op.drop_table('user_groups')
