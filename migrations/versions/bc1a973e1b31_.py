"""empty message

Revision ID: bc1a973e1b31
Revises: 6bedb3478f07
Create Date: 2023-07-27 08:31:15.924935

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc1a973e1b31'
down_revision = '6bedb3478f07'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.add_column(sa.Column('times_rented', sa.Integer(), nullable=False))

    with op.batch_alter_table('clients', schema=None) as batch_op:
        batch_op.add_column(sa.Column('no_books_rented', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('clients', schema=None) as batch_op:
        batch_op.drop_column('no_books_rented')

    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.drop_column('times_rented')

    # ### end Alembic commands ###