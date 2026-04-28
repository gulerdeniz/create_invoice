# → iş mantığı, fatura oluştur
from sqlalchemy.orm import Session
from database import Base, engine
from models import Fatura
from datetime import date
import uuid

Base.metadata.create_all(bind=engine) # Tabloyu fiziksel olarak db'de oluşturduk.


def create_invoice(alici_isim: str, satici_firma: str, urun_adi: str, miktar: int, fiyat: float, kdv_orani: float, db: Session):
    new_invoice = Fatura(
        fatura_no = str(uuid.uuid4()),
        tarih = date.today(),
        alici_isim = alici_isim,
        satici_firma = satici_firma,
        urun_adi = urun_adi,
        miktar = miktar,
        fiyat = fiyat,
        kdv_orani = kdv_orani,
        toplam_tutar = fiyat*miktar*(1 + kdv_orani)
    )
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)
    return new_invoice