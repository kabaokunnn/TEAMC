"""empty message

Revision ID: 460993d6b2f0
Revises: ca5a1b78f861
Create Date: 2024-11-29 11:59:49.847942

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '460993d6b2f0'
down_revision = 'ca5a1b78f861'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recipes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('recipe_name', sa.String(length=255), nullable=False),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.Column('is_favorite', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recipes')
    # ### end Alembic commands ###
