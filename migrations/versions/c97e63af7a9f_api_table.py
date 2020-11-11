"""api table

Revision ID: c97e63af7a9f
Revises: 9d46c25916c0
Create Date: 2020-10-27 11:40:43.471183

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c97e63af7a9f'
down_revision = '9d46c25916c0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('api_key',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('api_site', sa.String(length=20), nullable=True),
    sa.Column('key_hash', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_api_key_api_site'), 'api_key', ['api_site'], unique=True)
    op.drop_index('ix_user_email', table_name='user')
    op.create_unique_constraint(None, 'user', ['email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.create_index('ix_user_email', 'user', ['email'], unique=1)
    op.drop_index(op.f('ix_api_key_api_site'), table_name='api_key')
    op.drop_table('api_key')
    # ### end Alembic commands ###
