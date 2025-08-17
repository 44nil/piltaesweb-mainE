"""create measurements table

Revision ID: d9a7f5e2c4b3
Revises: 2a6d8156f1f8
Create Date: 2025-08-17 16:42:12.345678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9a7f5e2c4b3'
down_revision = '2a6d8156f1f8'
branch_labels = None
depends_on = None


def upgrade():
    # Önce measurements tablosunun var olup olmadığını kontrol et
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    tables = inspector.get_table_names()
    
    # Tablo yoksa oluştur
    if 'measurements' not in tables:
        op.create_table('measurements',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('member_id', sa.Integer(), nullable=False),
            sa.Column('date', sa.Date(), nullable=False),
            sa.Column('weight', sa.Float(), nullable=True),
            sa.Column('height', sa.Float(), nullable=True),
            sa.Column('waist', sa.Float(), nullable=True),
            sa.Column('hip', sa.Float(), nullable=True),
            sa.Column('shoulder', sa.Float(), nullable=True),
            sa.Column('bust', sa.Float(), nullable=True),
            sa.Column('arm', sa.Float(), nullable=True),
            sa.Column('thigh', sa.Float(), nullable=True),
            sa.Column('calf', sa.Float(), nullable=True),
            sa.ForeignKeyConstraint(['member_id'], ['members.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )
    
    # Index ekle (tablo varsa)
    if 'measurements' in tables:
        conn = op.get_bind()
        indexes = [idx['name'] for idx in inspector.get_indexes('measurements')]
        
        with op.batch_alter_table('measurements', schema=None) as batch_op:
            # Index yoksa ekle
            if 'ix_measurements_member_id' not in indexes:
                batch_op.create_index(batch_op.f('ix_measurements_member_id'), ['member_id'], unique=False)
            if 'ix_measurements_date' not in indexes:
                batch_op.create_index(batch_op.f('ix_measurements_date'), ['date'], unique=False)
    
    # Members tablosundan sütunları kaldır (varsa)
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('members')]
    
    # Varsa sil, yoksa hata verme
    with op.batch_alter_table('members', schema=None) as batch_op:
        for col_name in ['weight', 'height', 'waist', 'hip', 'shoulder', 'bust', 'arm', 'thigh', 'calf']:
            if col_name in columns:
                batch_op.drop_column(col_name)


def downgrade():
    # Önce measurements tablosundan referansları kaldır
    with op.batch_alter_table('measurements', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_measurements_member_id'))
        batch_op.drop_index(batch_op.f('ix_measurements_date'))
    
    # Measurements tablosunu sil
    op.drop_table('measurements')
    
    # Members tablosuna sütunları geri ekle
    with op.batch_alter_table('members', schema=None) as batch_op:
        # Sütunlar geri ekleniyor - eski veriler kaybolur
        batch_op.add_column(sa.Column('weight', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('height', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('waist', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('hip', sa.Float(), nullable=True))
        # Yeni eklenmiş sütunlar
        batch_op.add_column(sa.Column('shoulder', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('bust', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('arm', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('thigh', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('calf', sa.Float(), nullable=True))
