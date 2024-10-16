"""String format

Revision ID: 963fd9eb86f4
Revises: e34463b3e92f
Create Date: 2024-10-16 16:46:20.078466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '963fd9eb86f4'
down_revision = 'e34463b3e92f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('applications', schema=None) as batch_op:
        batch_op.alter_column('notice_period',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=20),
               existing_nullable=False)
        batch_op.alter_column('salary_expectation',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('applications', schema=None) as batch_op:
        batch_op.alter_column('salary_expectation',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=False)
        batch_op.alter_column('notice_period',
               existing_type=sa.String(length=20),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###
