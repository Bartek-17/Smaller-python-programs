# Aby zainstalować potrzebne biblioteki komenda: pip install pandas python-docx docx2pdf

import os  # tworzenie folderów (os.makedirs) i zarządzania ścieżkami (os.path).
import pandas as pd  # wczytywanie danych z pliku CSV (pd.read_csv).
from datetime import datetime  # uzyskanie aktualnej daty (datetime.now().strftime).
from docx import Document  # manipulacja plikami .docx (wczytywanie szablonu i zamiana zmiennych).
from docx2pdf import convert  # konwersja pliku .docx na .pdf.
from tkinter import Tk, Label, Entry, Button, StringVar, OptionMenu, filedialog, messagebox  # okienko

# konwersja programu na exe: (z --noconsole nie działa docx2pdf)
# 1: pip install pyinstaller
# 2: pyinstaller --onefile  --add-data "Zaswiadczenie_dzialalnosc_w_IW_k.docx;." 
# --add-data "Zaswiadczenie_dzialalnosc_w_IW_m.docx;." Program.py

def generuj_plik(dane, plec, funkcja):
    szablon = "Zaswiadczenie_dzialalnosc_w_IW_k.docx" if plec == "K" else "Zaswiadczenie_dzialalnosc_w_IW_m.docx"
    document = Document(szablon)

    for paragraph in document.paragraphs:
        if 'dd.mm.rrrr' in paragraph.text:
            paragraph.text = paragraph.text.replace('dd.mm.rrrr', datetime.now().strftime('%d.%m.%Y'))
        paragraph.text = paragraph.text.replace('Imię Nazwisko', f"{dane['Imię']} {dane['Nazwisko']}")
        paragraph.text = paragraph.text.replace('Nazwa Kierunku', dane['Kierunek'])
        paragraph.text = paragraph.text.replace('Wydział Nazwa Wydziału', dane['Wydział'])
        paragraph.text = paragraph.text.replace('Numer Albumu', str(dane['Numer albumu']))
        paragraph.text = paragraph.text.replace('Nazwa Działu i Funkcja', funkcja)

    folder = f"{dane['Imię']}_{dane['Nazwisko']}"
    os.makedirs(folder, exist_ok=True)
    sciezka_docx = os.path.join(folder, f"zaswiadczenie_{dane['Imię']}_{dane['Nazwisko']}.docx")
    document.save(sciezka_docx)
    convert(sciezka_docx, folder)
    sciezka_pdf = sciezka_docx.replace('.docx', '.pdf')
    messagebox.showinfo("Sukces", f"Plik PDF zapisano w: {sciezka_pdf}")

def wczytaj_csv():
    sciezka = filedialog.askopenfilename(filetypes=[("Pliki CSV", "*.csv")])
    if sciezka:
        return pd.read_csv(sciezka)
    return None

def uruchom_gui():
    dane = wczytaj_csv()
    if dane is None:
        messagebox.showerror("Błąd", "Nie wybrano pliku CSV.")
        return

    root = Tk()
    root.title("Generator Zaświadczeń")
    root.geometry("600x200")

    imie_nazwisko_var = StringVar(root)
    imie_nazwisko_var.set(f"{dane.iloc[0]['Imię']} {dane.iloc[0]['Nazwisko']}")

    # lista rozwijana
    Label(root, text="Wybierz osobę:").grid(row=0, column=0, padx=10, pady=10, sticky="w") # "w" - wyrównanie do lewej 
    osoby = [f"{row['Imię']} {row['Nazwisko']}" for _, row in dane.iterrows()]
    OptionMenu(root, imie_nazwisko_var, *osoby).grid(row=0, column=1, padx=10, pady=10, sticky="w")

    # pole tekstowe dla funkcji
    Label(root, text="Podaj funkcję:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    funkcja_entry = Entry(root, width=50)
    funkcja_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    # Przykładowy input pasujący do formatki
    Label(
        root,
        text="Przykładowa funckja:\nDziału Mechanicznego – koordynując pracami sekcji Badań i Rozwoju",
        fg="blue",
        justify="left"
    ).grid(row=2, column=1, padx=10, pady=5, sticky="w")

    # Funkcja do obsługi przycisku
    def generuj():
        wybrana_osoba = imie_nazwisko_var.get()
        funkcja = funkcja_entry.get()
        if not funkcja:
            messagebox.showerror("Błąd", "Proszę podać funkcję.")
            return

        wybrane_dane = dane.loc[(dane['Imię'] + " " + dane['Nazwisko']) == wybrana_osoba].iloc[0]
        generuj_plik(wybrane_dane, wybrane_dane['Płeć'], funkcja)

    # Przycisk generowania
    Button(root, text="Generuj zaświadczenie", command=generuj).grid(row=3, column=0, columnspan=2, pady=20)

    root.mainloop()

if __name__ == "__main__":
    uruchom_gui()