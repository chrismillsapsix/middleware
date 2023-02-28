"""webui_attribute

Revision ID: 60a953d6da3a
Revises: 653ea1a2ba57
Create Date: 2023-02-17 12:50:10.441696+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60a953d6da3a'
down_revision = '653ea1a2ba57'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account_bsdusers_webui_attribute',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('attributes', sa.TEXT(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_account_bsdusers_webui_attribute')),
    sa.UniqueConstraint('uid', name=op.f('uq_account_bsdusers_webui_attribute_uid')),
    sqlite_autoincrement=True
    )
    op.execute("INSERT INTO account_bsdusers_webui_attribute (uid, attributes) "
               "SELECT bsdusr_uid, bsdusr_attributes FROM account_bsdusers WHERE bsdusr_attributes != '{}'")
    with op.batch_alter_table('account_bsdusers', schema=None) as batch_op:
        batch_op.drop_column('bsdusr_attributes')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('account_bsdusers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bsdusr_attributes', sa.TEXT(), nullable=False))

    op.drop_table('account_bsdusers_webui_attribute')
    # ### end Alembic commands ###