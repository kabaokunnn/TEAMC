"""empty message

Revision ID: dc78711dd75b
Revises: 412bb1e34ed7
Create Date: 2024-11-25 15:37:47.228623

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'dc78711dd75b'
down_revision = '412bb1e34ed7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('selected_ingredient', schema=None) as batch_op:
        batch_op.drop_column('id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('selected_ingredient', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False))

    # ### end Alembic commands ###
