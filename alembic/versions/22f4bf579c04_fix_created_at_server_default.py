"""Fix created_at server default

Revision ID: 22f4bf579c04
Revises: f8ba64396fcd
Create Date: 2026-07-02 11:00:03.650903

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22f4bf579c04'
down_revision: Union[str, Sequence[str], None] = 'f8ba64396fcd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "posts",
        "created_at",
        server_default=sa.text("now()")
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "posts",
        "created_at",
        server_default=None
    )
    pass
