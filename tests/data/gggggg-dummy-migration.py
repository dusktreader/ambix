"""Some dummy migration script for alembic

Revision ID: gggggg
Revises: eeeeee, ffffff
Create Date: 2017-06-09 11:33:51.000000

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'gggggg'
down_revision = ('eeeeee', 'ffffff')


def upgrade():
    pass


def downgrade():
    pass
