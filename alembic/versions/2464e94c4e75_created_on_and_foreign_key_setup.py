"""created on and foreign key setup

Revision ID: 2464e94c4e75
Revises: cf99ed67c726
Create Date: 2026-07-01 16:36:11.936357

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2464e94c4e75'
down_revision: Union[str, Sequence[str], None] = 'cf99ed67c726'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts",sa.Column("created_at",sa.TIMESTAMP(True),nullable=False,default=sa.text('now()')))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts","created_at")
    pass
