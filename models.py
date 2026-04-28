# → tablo tanımı
from sqlalchemy import Column, Integer, String, Float, Date
from database import Base

class Fatura(Base):
    __tablename__ = "fatura_bilgileri"
    id = Column(Integer, primary_key=True, index=True)
    fatura_no = Column(String, nullable = False)
    tarih = Column(Date, nullable=False)
    alici_isim = Column(String, nullable=False)
    satici_firma = Column(String, nullable=False)
    urun_adi = Column(String, nullable=False)
    miktar = Column(Integer, nullable=False)
    fiyat = Column(Float, nullable=False)
    kdv_orani = Column(Float, nullable=False)
    toplam_tutar = Column(Float, nullable=False)

