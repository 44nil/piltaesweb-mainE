"""rename_chest_to_thigh

Revision ID: 7f044ce220bf
Revises: d9a7f5e2c4b3
Create Date: 2025-08-17 16:44:40.642967

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f044ce220bf'
down_revision = 'd9a7f5e2c4b3'
branch_labels = None
depends_on = None


def upgrade():
    # SQLite için doğrudan sütun adını değiştirmek mümkün değil
    # Geçici bir tablo oluşturup verileri kopyalamamız gerekiyor
    
    # Mevcut tabloyu yedekle ve yeni sütun adlarıyla yeniden oluştur
    conn = op.get_bind()
    
    # Veri kaybını önlemek için önce verileri saklayalım
    measurements_data = []
    for row in conn.execute(sa.text("SELECT id, member_id, date, weight, waist, hip, chest FROM measurements")).fetchall():
        measurements_data.append(row)
    
    # SQLite batch_alter_table kullanarak tablo yapısını değiştirelim
    with op.batch_alter_table('measurements', schema=None) as batch_op:
        batch_op.add_column(sa.Column('thigh', sa.Float(), nullable=True))
        
    # chest sütunundaki verileri thigh sütununa taşı
    for row in measurements_data:
        conn.execute(sa.text("UPDATE measurements SET thigh = :chest WHERE id = :id"),
                   {"chest": row[6], "id": row[0]})
    
    # Artık chest sütunu kaldırılabilir
    with op.batch_alter_table('measurements', schema=None) as batch_op:
        batch_op.drop_column('chest')


def downgrade():
    # Geri dönüşte aynı işlemi tersten yapalım
    conn = op.get_bind()
    
    # Veri kaybını önlemek için önce verileri saklayalım
    measurements_data = []
    for row in conn.execute(sa.text("SELECT id, member_id, date, weight, waist, hip, thigh FROM measurements")).fetchall():
        measurements_data.append(row)
    
    # SQLite batch_alter_table kullanarak tablo yapısını değiştirelim
    with op.batch_alter_table('measurements', schema=None) as batch_op:
        batch_op.add_column(sa.Column('chest', sa.Float(), nullable=True))
        
    # thigh sütunundaki verileri chest sütununa taşı
    for row in measurements_data:
        conn.execute(sa.text("UPDATE measurements SET chest = :thigh WHERE id = :id"),
                   {"thigh": row[6], "id": row[0]})
    
    # Artık thigh sütunu kaldırılabilir
    with op.batch_alter_table('measurements', schema=None) as batch_op:
        batch_op.drop_column('thigh')
