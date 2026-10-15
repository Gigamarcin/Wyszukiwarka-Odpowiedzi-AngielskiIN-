"""Okienko (tkinter) do wyszukiwarki zadań.

Uruchom:  python wyszukiwarka_gui.py   (albo dwuklik na pliku)
Musi leżeć w tym samym folderze co szukajzadaniaang.py i plik z rozwiązaniami.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext

from szukajzadaniaang import wyszukajzadanie


def szukaj(event=None):
    try:
        unit = int(unit_var.get())
        task = int(task_var.get())
    except ValueError:
        pokaz("Wpisz numer unitu i tasku jako liczby.")
        return
    try:
        wynik = wyszukajzadanie(unit, task)
    except FileNotFoundError as e:
        wynik = str(e)
    pokaz(wynik)


def pokaz(tekst):
    wyniki.config(state="normal")
    wyniki.delete("1.0", tk.END)
    wyniki.insert(tk.END, tekst)
    # pogrubienie linii z poleceniem i nagłówków
    for nr, linia in enumerate(tekst.splitlines(), start=1):
        if linia.startswith("Polecenie:"):
            wyniki.tag_add("polecenie", f"{nr}.0", f"{nr}.end")
        elif linia.startswith("[") or linia.startswith("UNIT") or linia.startswith("Task"):
            wyniki.tag_add("naglowek", f"{nr}.0", f"{nr}.end")
    wyniki.config(state="disabled")


okno = tk.Tk()
okno.title("Wyszukiwarka zadań – angielski C1")
okno.geometry("760x560")
okno.minsize(500, 350)

gora = ttk.Frame(okno, padding=10)
gora.pack(fill="x")

ttk.Label(gora, text="Unit:").pack(side="left")
unit_var = tk.StringVar(value="1")
ttk.Spinbox(gora, from_=1, to=9, width=4, textvariable=unit_var).pack(side="left", padx=(4, 15))

ttk.Label(gora, text="Task:").pack(side="left")
task_var = tk.StringVar(value="1")
ttk.Spinbox(gora, from_=1, to=25, width=4, textvariable=task_var).pack(side="left", padx=(4, 15))

ttk.Button(gora, text="Szukaj", command=szukaj).pack(side="left")
ttk.Label(gora, text="(Unit 9: task = numer testu 1–3)", foreground="gray").pack(side="left", padx=15)

wyniki = scrolledtext.ScrolledText(okno, wrap="word", font=("Consolas", 11), padx=8, pady=8)
wyniki.pack(fill="both", expand=True, padx=10, pady=(0, 10))
wyniki.tag_config("polecenie", font=("Consolas", 11, "italic"), foreground="#1a5fb4")
wyniki.tag_config("naglowek", font=("Consolas", 11, "bold"))
wyniki.config(state="disabled")

okno.bind("<Return>", szukaj)
pokaz("Wybierz unit i task, potem kliknij „Szukaj” albo naciśnij Enter.")

okno.mainloop()
