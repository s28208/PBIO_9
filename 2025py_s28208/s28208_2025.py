# ----------------------------------------------
# CEL PROGRAMU:
# Program generuje losowa sekwencje DNA w formacie FASTA.
# Pozwala uzytkownikowi podac dlugosc sekwencji, ID, opis i imie.
# Imie zostaje wstawione w losowym miejscu sekwencji (nie wplywa na statystyki).
# Wynik zapisywany jest do pliku FASTA z podanym ID jako nazwa pliku.
# Program wyswietla tez dokladne statystyki sekwencji.
#
# KONTEKST ZASTOSOWANIA:
# Edukacja z zakresu bioinformatyki, formatow sekwencyjnych oraz podstaw obliczen DNA.
# ----------------------------------------------

import random  # MODIFIED: Import do losowania sekwencji DNA i pozycji imienia
import re      # MODIFIED: Import do walidacji ID sekwencji (regex)

#--------------------3------------------------------
# ORIGINAL:
#
# MODIFIED (jedzna zmnienna dla nukleotydow, jezeli
# trzeba bedzie zmienic na RNA ):
NUCLEOTIDES = 'ACGT'  # zestaw znakow reprezentujacych nukleotydy

#----------------------4----------------------
# ORIGINAL:
#
# MODIFIED (podzielenie ciagow nukleotydow po 60znakow, jak jest w plikach fasta ):
# Dzieli sekwencje na linie o dlugosci 60 znakow.
def format_fasta_sequence(seq: str, line_length: int = 60) -> str:
    return '\n'.join(seq[i:i+line_length] for i in range(0, len(seq), line_length))

###--------1--------- MODIFIED (dodanie walidacji,zeby uniknanc bledow):

# MODIFIED: Walidacja poprawnosci dlugosci (czy to dodatnia liczba calkowita)
def get_valid_length():
    while True:  # petla nieskonczona - dopoki uzytkownik nie poda poprawnej wartosci
        length_input = input("Podaj dlugosc sekwencji: ")  # pobiera dane od uzytkownika jako tekst
        if length_input.isdigit() and int(length_input) > 0:  # sprawdza czy tekst to liczba i czy jest wieksza od zera
            return int(length_input)  # zwraca liczbe jako int, jezeli warunki sa spelnione
        else:  # jezeli dane sa niepoprawne
            print("Blad: dlugosc musi byc dodatnia liczba calkowita.")  # wypisuje komunikat o bledzie


# Walidacja ID — tylko litery, cyfry, myslniki i podkreslenia
def get_valid_id():
    while True:  # petla nieskonczona - powtarza sie dopoki nie zostanie podane poprawne ID
        seq_id = input("Podaj ID sekwencji: ")  # pobiera ID sekwencji od uzytkownika jako tekst
        if re.match(r'^[\w\-]+$', seq_id):  # sprawdza czy ID pasuje do wzorca: litery, cyfry, podkreslenia lub myslniki
            return seq_id  # jezeli ID jest poprawne - zwraca je jako wynik funkcji
        else:  # jesli ID nie pasuje do wzorca
            print("Blad: ID moze zawierac tylko litery, cyfry, myslnik i podkreslenie.")  # wypisuje komunikat bledu

# Walidacja — opis nie moze byc pusty
def get_valid_description():
    while True:  # petla nieskonczona - dopoki uzytkownik nie poda poprawnego opisu
        description = input("Podaj opis sekwencji: ").strip()  # pobiera opis i usuwa biale znaki z poczatku i konca
        if description:  # sprawdza czy po usunieciu bialych znakow cos zostalo
            return description  # jesli tak - zwraca opis
        else:  # jesli opis jest pusty
            print("Blad: opis nie moze byc pusty.")  # wypisuje komunikat o bledzie


# Walidacja imienia — tylko litery
def get_valid_name():
    while True:  # petla nieskonczona - trwa do momentu podania poprawnego imienia
        name = input("Podaj imie: ")  # pobiera imie od uzytkownika
        if name.isalpha():  # sprawdza czy imie sklada sie tylko z liter (bez spacji, cyfr i znakow specjalnych)
            return name  # jezeli tak, zwraca imie
        else:  # w przeciwnym razie
            print("Blad: imie moze zawierac tylko litery.")  # wyswietla komunikat o bledzie


#-------------1------------------------#
# Generuje losowa sekwencje zlozona z liter A, C, G, T.
def generate_dna_sequence(length):
    return ''.join(random.choices(NUCLEOTIDES, k=length))  # losuje 'length' liter z NUCLEOTIDES i laczy je w ciag

# Wstawia imie uzytkownika w losowa pozycje w sekwencji DNA.
def insert_name_into_sequence(sequence, name):
    position = random.randint(0, len(sequence))  # wybiera losowa pozycje od 0 do dlugosci sekwencji
    return sequence[:position] + name + sequence[position:]  # wstawia imie miedzy dwie czesci sekwencji


# ORIGINAL:
#<stara wersja>--------------------2----------------------
# def calculate_statistics(sequence):
#     total = len(sequence)
#     stats = {nuc: sequence.count(nuc) / total * 100 for nuc in 'ACGT'}
#     cg = stats['C'] + stats['G']
#     at = stats['A'] + stats['T']
#     cg_at_ratio = cg / at if at > 0 else 0
#     return stats, cg

# MODIFIED (ulepszenie polega na wyswietlaniu ilosci nukleotydow
# kazdego typu, zeby wiedziec ilosciowo nie tylko procentowo):
def calculate_statistics(sequence):
    total = len(sequence)  # oblicza laczna dlugosc sekwencji (bez imienia)
    counts = {nuc: sequence.count(nuc) for nuc in NUCLEOTIDES}  # tworzy slownik z iloscia wystapien kazdego nukleotydu
    percentages = {nuc: (counts[nuc] / total * 100) for nuc in NUCLEOTIDES}  # oblicza procentowy udzial kazdego nukleotydu
    cg = percentages['C'] + percentages['G']  # suma procentow C i G (zawartosc CG)
    at = percentages['A'] + percentages['T']  # suma procentow A i T (zawartosc AT)
    cg_at_ratio = cg / at if at > 0 else 0  # oblicza stosunek CG do AT, jezeli AT > 0
    return counts, percentages, cg  # zwraca ilosci, procenty i CG jako wynik


# GLOWNA FUNKCJA — zarzadza calym przeplywem programu
def main():
    # ORIGINAL: -------1-----------
    #     length = int(input("Podaj dlugosc sekwencji: "))
    #     seq_id = input("Podaj ID sekwencji: ")
    #     description = input("Podaj opis sekwencji: ")
    #     name = input("Podaj imie: ")

    # MODIFIED (dodanie walidacji,zeby uniknanc bledow): ----------1-------------
    # Pobieranie danych od uzytkownika z walidacja
    length = get_valid_length()  # pobiera poprawna dlugosc sekwencji
    seq_id = get_valid_id()  # pobiera poprawne ID sekwencji
    description = get_valid_description()  # pobiera opis sekwencji
    name = get_valid_name()  # pobiera imie uzytkownika

    # Generowanie sekwencji
    dna_sequence = generate_dna_sequence(length)  # generuje losowa sekwencje DNA o podanej dlugosci

    # Statystyki oryginalnej sekwencji (bez imienia)
#   OLD --------2-------------
#   stats, cg_content = calculate_statistics(dna_sequence)
#   NEW:
    counts, stats, cg_content = calculate_statistics(dna_sequence)  # liczy liczby i procenty nukleotydow + CG

    # Wstawienie imienia do sekwencji
    final_sequence = insert_name_into_sequence(dna_sequence, name)  # wstawia imie do losowej pozycji w sekwencji

    # Zapis do pliku FASTA
    filename = f"{seq_id}.fasta"  # tworzy nazwe pliku z ID
    with open(filename, 'w') as fasta_file:  # otwiera plik do zapisu
        fasta_file.write(f">{seq_id} {description}\n")  # naglowek FASTA z ID i opisem
    #-----------4-------------------
    #   fasta_file.write(final_sequence + '\n')
        fasta_file.write(format_fasta_sequence(final_sequence) + '\n')  # zapisuje sekwencje w liniach po 60 znakow

    # Wyswietlenie wynikow
    print(f"\nSekwencja zostala zapisana do pliku {filename}")  # informuje uzytkownika o zapisaniu pliku
    print("Statystyki sekwencji:")  # wypisuje naglowek sekcji statystyk
    for nuc in NUCLEOTIDES:  # dla kazdego nukleotydu w zestawie
    #----------------------2----------------------------------
    #     print(f"{nuc}: {stats[nuc]:.1f}%")
    # print(f"%CG: {cg_content:.1f}")
        print(f"{nuc}: {counts[nuc]} ({stats[nuc]:.1f}%)")  # wypisuje liczbe i procent dla danego nukleotydu
    print(f"%CG: {cg_content:.1f}")  # wypisuje laczna zawartosc C i G w procentach


# Uruchomienie programu — tylko jesli plik nie jest importowany
if __name__ == "__main__":
    main()
