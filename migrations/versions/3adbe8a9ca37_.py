"""empty message

Revision ID: 3adbe8a9ca37
Revises: 2fbf1ac8d1b5
Create Date: 2023-03-01 22:59:05.796105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3adbe8a9ca37'
down_revision = '2fbf1ac8d1b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('article_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'article', ['article_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('article_id')

    # ### end Alembic commands ###
