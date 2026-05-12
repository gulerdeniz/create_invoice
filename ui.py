import tkinter as tk
from tkinter import ttk, messagebox
from database import local_session as SessionLocal
from service import create_invoice
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os, sys
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("Arial", "C:/Windows/Fonts/arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", "C:/Windows/Fonts/arialbd.ttf"))
def generate_pdf(invoice):
    output_dir = os.path.join(os.path.dirname(sys.executable), "faturalar")
    os.makedirs(output_dir, exist_ok=True)

    filename = f"fatura_{invoice.fatura_no[:8]}.pdf"
    filepath = os.path.join(output_dir, filename)

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    # Başlık
    c.setFont("Arial-Bold", 20)
    c.drawString(200, height - 60, "INVOICE")

    # Çizgi
    c.setLineWidth(1)
    c.line(40, height - 75, width - 40, height - 75)

    # Fatura no ve tarih
    c.setFont("Arial-Bold", 11)
    c.drawString(40, height - 110, "Invoice No:")
    c.drawString(40, height - 135, "Date:")

    c.setFont("Arial", 11)
    c.drawString(160, height - 110, invoice.fatura_no[:8])
    c.drawString(160, height - 135, str(invoice.tarih))

    # Alıcı ve satıcı
    c.setFont("Arial", 11)
    c.drawString(40, height - 175, "Recipient:")
    c.drawString(40, height - 200, "Seller:")

    c.setFont("Arial", 11)
    c.drawString(160, height - 175, invoice.alici_isim)
    c.drawString(160, height - 200, invoice.satici_firma)

    # Ürün tablosu başlığı
    c.setLineWidth(0.5)
    c.line(40, height - 230, width - 40, height - 230)

    c.setFont("Arial-Bold", 11)
    c.drawString(40,  height - 250, "Product")
    c.drawString(250, height - 250, "Quantity")
    c.drawString(350, height - 250, "Unit Price")
    c.drawString(460, height - 250, "VAT %")

    c.line(40, height - 260, width - 40, height - 260)

    # Ürün satırı
    c.setFont("Arial", 11)
    c.drawString(40,  height - 278, invoice.urun_adi)
    c.drawString(250, height - 278, str(invoice.miktar))
    c.drawString(350, height - 278, f"{invoice.fiyat:.2f} TL")
    c.drawString(460, height - 278, f"{invoice.kdv_orani * 100:.0f}%")

    c.line(40, height - 290, width - 40, height - 290)

    # Toplam
    c.setFont("Arial-Bold", 13)
    c.drawString(350, height - 320, "TOTAL:")
    c.drawString(460, height - 320, f"{invoice.toplam_tutar:.2f} TL")

    c.save()
    return filepath

def submit_invoice():
    # Formdaki değerleri al
    alici = entry_alici.get().strip()
    satici = entry_satici.get().strip()
    urun = entry_urun.get().strip()
    miktar_str = entry_miktar.get().strip()
    fiyat_str = entry_fiyat.get().strip()
    kdv_str = entry_kdv.get().strip()

    # Boş alan kontrolü
    if not all([alici, satici, urun, miktar_str, fiyat_str, kdv_str]):
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return

    # Sayısal dönüşüm kontrolü
    try:
        miktar = int(miktar_str)
        fiyat = float(fiyat_str)
        kdv = float(kdv_str) / 100  # Kullanıcı % olarak giriyor, örn: 18 → 0.18
    except ValueError:
        messagebox.showerror("Error", "Quantity must be a whole number, price and VAT must be numbers.")
        return

    # Veritabanına kaydet
    db = SessionLocal()
    try:
        invoice = create_invoice(alici, satici, urun, miktar, fiyat, kdv, db)
        filepath = generate_pdf(invoice)
        toplam = round(invoice.toplam_tutar, 2)
        messagebox.showinfo(
            "Success",
            f"Invoice created successfully!\n\n"
            f"Invoice No: {invoice.fatura_no[:8]}...\n"
            f"Date: {invoice.tarih}\n"  
            f"Total: {toplam} TL\n\n"
            f'PDF saved:\n{filepath}'
        )
        clear_form()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        db.close()


def clear_form():
    for entry in [entry_alici, entry_satici, entry_urun, entry_miktar, entry_fiyat, entry_kdv]:
        entry.delete(0, tk.END)
    entry_alici.focus()


# --- Ana pencere ---
root = tk.Tk()
root.title("Invoice Creator")
root.geometry("420x380")
root.resizable(False, False)

# Başlık
title_label = tk.Label(root, text="Create New Invoice", font=("Helvetica", 14, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=(15, 10))

# Etiket ve giriş alanları
fields = [
    ("Recipient Name:", "entry_alici"),
    ("Seller Company:", "entry_satici"),
    ("Product Name:", "entry_urun"),
    ("Quantity:", "entry_miktar"),
    ("Unit Price (TL):", "entry_fiyat"),
    ("VAT Rate (%):", "entry_kdv"),
]

entries = {}
for i, (label_text, var_name) in enumerate(fields):
    tk.Label(root, text=label_text, anchor="w").grid(row=i+1, column=0, padx=(20, 5), pady=6, sticky="w")
    entry = ttk.Entry(root, width=28)
    entry.grid(row=i+1, column=1, padx=(0, 20), pady=6)
    entries[var_name] = entry

entry_alici  = entries["entry_alici"]
entry_satici = entries["entry_satici"]
entry_urun   = entries["entry_urun"]
entry_miktar = entries["entry_miktar"]
entry_fiyat  = entries["entry_fiyat"]
entry_kdv    = entries["entry_kdv"]

# Butonlar
btn_frame = tk.Frame(root)
btn_frame.grid(row=8, column=0, columnspan=2, pady=(15, 10))

submit_btn = ttk.Button(btn_frame, text="Create Invoice", command=submit_invoice)
submit_btn.grid(row=0, column=0, padx=10)

clear_btn = ttk.Button(btn_frame, text="Clear Form", command=clear_form)
clear_btn.grid(row=0, column=1, padx=10)

entry_alici.focus()
root.mainloop()
