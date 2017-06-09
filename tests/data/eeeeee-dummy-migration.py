"""Some dummy migration script for alembic

Revision ID: eeeeee
Revises: cccccc, dddddd
Create Date: 2017-06-09 11:33:51.000000

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'eeeeee'
down_revision = ('cccccc', 'dddddd')


def upgrade():
    pass


def downgrade():
    pass
