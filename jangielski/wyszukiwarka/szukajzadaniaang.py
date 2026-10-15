import re
from pathlib import Path

PLIK = Path(__file__).with_name("Rozwiazania_podrecznik_angielski_C1.txt")

_UNIT_RE = re.compile(r"^UNIT\s+(\d+)\.\s*(.*)$")
_TASK_RE = re.compile(r"^Task\s+(\d+)([a-z]?(?:/\d*[a-z])*)?(?:\s*[–-]\s*(\d+))?")
_PRACTICE_RE = re.compile(r"PRACTICE TEST No\.\s*(\d+)")


def _wczytaj_linie():
    if not PLIK.exists():
        raise FileNotFoundError(f"Nie znaleziono pliku z rozwiązaniami: {PLIK}")
    return PLIK.read_text(encoding="utf-8-sig").splitlines()


def _podziel_na_sekcje(linie):
    """Zwraca listę (nr_unitu, tytuł_sekcji, linie_sekcji)."""
    sekcje = []
    biezacy = None
    i = 0
    while i < len(linie):
        m = _UNIT_RE.match(linie[i].strip())
        # nagłówek unitu jest otoczony liniami "====="
        if m and i > 0 and linie[i - 1].startswith("===="):
            biezacy = (int(m.group(1)), linie[i].strip(), [])
            sekcje.append(biezacy)
            i += 2  # pomiń dolną linię "====="
            continue
        if biezacy is not None:
            biezacy[2].append(linie[i])
        i += 1
    return sekcje


def _czy_pasuje(linia, task):
    m = _TASK_RE.match(linia.strip())
    if not m:
        return False
    od = int(m.group(1))
    do = int(m.group(3)) if m.group(3) else od  # zakresy typu "Task 15–19"
    return od <= task <= do


def _koniec_bloku(linia):
    s = linia.strip()
    return bool(_TASK_RE.match(s)) or s.startswith("====") or s.startswith("--- ")


def wyszukajzadanie(unit, task):
    """Zwraca tekst rozwiązania dla podanego unitu i tasku (albo komunikat, że nie ma)."""
    unit, task = int(unit), int(task)
    sekcje = [s for s in _podziel_na_sekcje(_wczytaj_linie()) if s[0] == unit]
    if not sekcje:
        return f"Nie ma Unitu {unit} w pliku z rozwiązaniami."

    wyniki = []

    if unit == 9:  # testy próbne: task = numer testu
        for _, tytul, tresc in sekcje:
            m = _PRACTICE_RE.search(tytul)
            if m and int(m.group(1)) == task:
                wyniki.append(tytul + "\n" + "\n".join(tresc).strip())
        if not wyniki:
            return "W Unit 9 są tylko testy próbne 1, 2 i 3 – podaj numer testu jako task."
        return "\n\n".join(wyniki)

    for _, tytul, tresc in sekcje:
        j = 0
        while j < len(tresc):
            if _czy_pasuje(tresc[j], task):
                blok = [tresc[j]]
                j += 1
                while j < len(tresc) and not _koniec_bloku(tresc[j]):
                    blok.append(tresc[j])
                    j += 1
                wyniki.append(f"[{tytul}]\n" + "\n".join(blok).rstrip())
            else:
                j += 1

    if not wyniki:
        return f"Nie znaleziono: Unit {unit}, Task {task}."
    return "\n\n".join(wyniki)


def _parsuj_zapytanie(tekst):
    liczby = re.findall(r"\d+", tekst)
    if len(liczby) < 2:
        return None
    return int(liczby[0]), int(liczby[1])


if __name__ == "__main__":
    print("Wyszukiwarka zadań – wpisz np. 'unit 2 task 10' (Enter bez tekstu = koniec).")
    while True:
        zapytanie = input("\n> ").strip()
        if not zapytanie:
            break
        para = _parsuj_zapytanie(zapytanie)
        if para is None:
            print("Podaj numer unitu i tasku, np. 'unit 2 task 10' albo '2 10'.")
            continue
        print()
        print(wyszukajzadanie(*para))
