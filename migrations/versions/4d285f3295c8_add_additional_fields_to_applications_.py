"""Add additional fields to applications table

Revision ID: 4d285f3295c8
Revises: e840fa2e667b
Create Date: 2024-10-16 11:00:01.058618

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d285f3295c8'
down_revision = 'e840fa2e667b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('applications', schema=None) as batch_op:
        batch_op.add_column(sa.Column('full_name', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('email', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('phone_number', sa.String(length=20), nullable=False))
        batch_op.add_column(sa.Column('resume', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('portfolio', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('country_of_residence', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('notice_period', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('salary_expectation', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('years_of_experience', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('applications', schema=None) as batch_op:
        batch_op.drop_column('years_of_experience')
        batch_op.drop_column('salary_expectation')
        batch_op.drop_column('notice_period')
        batch_op.drop_column('country_of_residence')
        batch_op.drop_column('portfolio')
        batch_op.drop_column('resume')
        batch_op.drop_column('phone_number')
        batch_op.drop_column('email')
        batch_op.drop_column('full_name')

    # ### end Alembic commands ###
