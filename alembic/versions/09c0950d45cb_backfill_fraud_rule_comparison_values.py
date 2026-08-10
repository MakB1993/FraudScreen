"""backfill fraud rule comparison values

Revision ID: 09c0950d45cb
Revises: bc7fa9980ea2
Create Date: 2026-08-07 01:36:42.114611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '09c0950d45cb'
down_revision: Union[str, Sequence[str], None] = 'bc7fa9980ea2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
    """
    UPDATE fraud_rules
    SET comparison_value = threshold_value
    WHERE comparison_value IS NULL
    """
)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
    """
    UPDATE fraud_rules
    SET comparison_value = NULL
    """
)
