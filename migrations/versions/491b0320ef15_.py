"""empty message

Revision ID: 491b0320ef15
Revises: 5ea61ee19f3a
Create Date: 2024-12-04 12:19:09.516218

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '491b0320ef15'
down_revision = '5ea61ee19f3a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recipe_suggestion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=120), nullable=True),
    sa.Column('ingredients', sa.String(length=500), nullable=True),
    sa.Column('steps', sa.Text(), nullable=True),
    sa.Column('ingredient_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ingredient_id'], ['ingredient.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('recipe_suggestions')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recipe_suggestions',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('ingredients', mysql.TEXT(), nullable=False),
    sa.Column('steps', mysql.TEXT(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('recipe_suggestion')
    # ### end Alembic commands ###
