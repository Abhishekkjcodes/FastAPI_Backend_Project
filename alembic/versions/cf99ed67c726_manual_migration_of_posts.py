"""manual migration of posts

Revision ID: cf99ed67c726
Revises: 
Create Date: 2026-07-01 16:28:19.883151

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf99ed67c726'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("posts",
                    sa.Column("id",sa.Integer,nullable=False,primary_key=True),
                    sa.Column("title",sa.String,nullable=False),
                    sa.Column("content",sa.String,nullable=False),
                    sa.Column("published",sa.Boolean,nullable=False,default=True),
                    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("posts")
    pass
