import sqlite3
from typing import List, Tuple

# Connessione al database SQLite 'libreria.db'
conn: sqlite3.Connection = sqlite3.connect("libreria.db")
cursor: sqlite3.Cursor = conn.cursor()

def create_tables():
    """Crea le tabelle se non esistono."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Autori (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            cognome TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Libri (
            id INTEGER PRIMARY KEY,
            titolo TEXT NOT NULL,
            autore_id INTEGER,
            anno INTEGER,
            genere TEXT,
            FOREIGN KEY (autore_id) REFERENCES Autori(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Prestiti (
            id INTEGER PRIMARY KEY,
            libro_id INTEGER,
            utente TEXT NOT NULL,
            data_prestito TEXT,
            data_restituzione TEXT,
            FOREIGN KEY (libro_id) REFERENCES Libri(id)
        )
    """)
    conn.commit()

def insert_data():
    """Inserisci i dati di esempio."""
    # Autori
    autori = [
        (1, 'Mario', 'Rossi'),
        (2, 'Lucia', 'Bianchi'),
        (3, 'Alessandro', 'Verdi')
    ]
    cursor.executemany("INSERT OR IGNORE INTO Autori (id, nome, cognome) VALUES (?, ?, ?)", autori)

    # Libri
    libri = [
        (1, 'Il mistero del castello', 1, 2020, 'Giallo'),
        (2, 'Viaggio nel tempo', 1, 2018, 'Fantascienza'),
        (3, 'La cucina italiana', 2, 2019, 'Cucina'),
        (4, 'Storia antica', 3, 2021, 'Storia'),
        (5, 'Romanzo moderno', 3, 2022, 'Narrativa'),
        (6, 'Il ritorno del castello', 1, 2023, 'Giallo')
    ]
    cursor.executemany("INSERT OR IGNORE INTO Libri (id, titolo, autore_id, anno, genere) VALUES (?, ?, ?, ?, ?)", libri)

    # Prestiti
    prestiti = [
        (1, 1, 'Mario Rossi', '2023-01-01', '2023-01-15'),
        (2, 2, 'Lucia Bianchi', '2023-02-01', None),
        (3, 3, 'Alessandro Verdi', '2023-03-01', '2023-03-10'),
        (4, 4, 'Mario Rossi', '2023-04-01', None)
    ]
    cursor.executemany("INSERT OR IGNORE INTO Prestiti (id, libro_id, utente, data_prestito, data_restituzione) VALUES (?, ?, ?, ?, ?)", prestiti)
    conn.commit()

def query_libri_per_autore(autore_id: int) -> List[Tuple[int, str, int, str]]:
    """Restituisce tutti i libri di un autore specifico (usa JOIN)."""
    cursor.execute("""
        SELECT Libri.id, Libri.titolo, Libri.anno, Libri.genere
        FROM Libri
        JOIN Autori ON Libri.autore_id = Autori.id
        WHERE Autori.id = ?
    """, (autore_id,))
    return cursor.fetchall()

def query_prestiti_per_utente(utente: str) -> List[Tuple[int, str, str, str]]:
    """Restituisce i prestiti di un utente (usa JOIN)."""
    cursor.execute("""
        SELECT Prestiti.id, Libri.titolo, Prestiti.data_prestito, Prestiti.data_restituzione
        FROM Prestiti
        JOIN Libri ON Prestiti.libro_id = Libri.id
        WHERE Prestiti.utente = ?
    """, (utente,))
    return cursor.fetchall()

def query_libri_per_genere() -> List[Tuple[str, int]]:
    """Restituisce il numero di libri per genere (usa GROUP BY)."""
    cursor.execute("""
        SELECT genere, COUNT(*) AS num_libri
        FROM Libri
        GROUP BY genere
    """)
    return cursor.fetchall()

def query_autori_con_piu_libri() -> List[Tuple[str, str, int]]:
    """Restituisce gli autori ordinati per numero di libri (usa JOIN, GROUP BY, ORDER BY)."""
    cursor.execute("""
        SELECT Autori.nome, Autori.cognome, COUNT(*) AS num_libri
        FROM Autori
        JOIN Libri ON Autori.id = Libri.autore_id
        GROUP BY Autori.id
        ORDER BY num_libri DESC
    """)
    return cursor.fetchall()

def query_prestiti_non_restituiti() -> List[Tuple[int, str, str, str]]:
    """Restituisce i prestiti non ancora restituiti (data_restituzione IS NULL)."""
    cursor.execute("""
        SELECT Prestiti.id, Libri.titolo, Prestiti.utente, Prestiti.data_prestito
        FROM Prestiti
        JOIN Libri ON Prestiti.libro_id = Libri.id
        WHERE Prestiti.data_restituzione IS NULL
    """)
    return cursor.fetchall()

# Codice principale
if __name__ == "__main__":
    try:
        create_tables()
        insert_data()
        print("Database creato e dati inseriti con successo.\n")

        # Query 3: Libri per autore (es. autore_id=1)
        print("3) Libri dell'autore con id 1:")
        libri_autore = query_libri_per_autore(1)
        for libro in libri_autore:
            print(f"ID: {libro[0]}, Titolo: {libro[1]}, Anno: {libro[2]}, Genere: {libro[3]}")
        print()

        # Query 4: Prestiti per utente (es. 'Mario Rossi')
        print("4) Prestiti dell'utente 'Mario Rossi':")
        prestiti_utente = query_prestiti_per_utente('Mario Rossi')
        for prestito in prestiti_utente:
            print(f"ID Prestito: {prestito[0]}, Titolo Libro: {prestito[1]}, Data Prestito: {prestito[2]}, Data Restituzione: {prestito[3]}")
        print()

        # Query 5: Libri per genere
        print("5) Numero di libri per genere:")
        libri_genere = query_libri_per_genere()
        for genere in libri_genere:
            print(f"Genere: {genere[0]}, Numero libri: {genere[1]}")
        print()

        # Query 6: Autori con più libri
        print("6) Autori ordinati per numero di libri:")
        autori_libri = query_autori_con_piu_libri()
        for autore in autori_libri:
            print(f"Nome: {autore[0]}, Cognome: {autore[1]}, Numero libri: {autore[2]}")
        print()

        # Query 7: Prestiti non restituiti
        print("7) Prestiti non ancora restituiti:")
        prestiti_non_restituiti = query_prestiti_non_restituiti()
        for prestito in prestiti_non_restituiti:
            print(f"ID Prestito: {prestito[0]}, Titolo Libro: {prestito[1]}, Utente: {prestito[2]}, Data Prestito: {prestito[3]}")

        # Query 8: Elenco di tutti i libri con titolo, anno e nome dell'autore (usa JOIN)
        print("\n8) Elenco di tutti i libri con titolo, anno e nome dell'autore:")
        cursor.execute("""
            SELECT Libri.titolo, Libri.anno, Autori.nome, Autori.cognome
            FROM Libri
            JOIN Autori ON Libri.autore_id = Autori.id
        """)
        tutti_libri = cursor.fetchall()
        for libro in tutti_libri:
            print(f"Titolo: {libro[0]}, Anno: {libro[1]}, Autore: {libro[2]} {libro[3]}")

        # Query 9: Elenco di tutti i prestiti con titolo del libro, utente e data di prestito (usa JOIN)
        print("\n9) Elenco di tutti i prestiti con titolo del libro, utente e data di prestito:")
        cursor.execute("""
            SELECT Libri.titolo, Prestiti.utente, Prestiti.data_prestito
            FROM Prestiti
            JOIN Libri ON Prestiti.libro_id = Libri.id
        """)
        tutti_prestiti = cursor.fetchall()
        for prestito in tutti_prestiti:
            print(f"Titolo Libro: {prestito[0]}, Utente: {prestito[1]}, Data Prestito: {prestito[2]}")

        # Query 10: Elenco di tutti i libri pubblicati dopo il 2020 (usa WHERE)
        print("\n10) Elenco di tutti i libri pubblicati dopo il 2020:")
        cursor.execute("""
            SELECT titolo, anno, genere
            FROM Libri
            WHERE anno > 2020
        """)
        libri_dopo_2020 = cursor.fetchall()
        for libro in libri_dopo_2020:
            print(f"Titolo: {libro[0]}, Anno: {libro[1]}, Genere: {libro[2]}")

        # Query 11: Numero di prestiti per ciascun utente (usa GROUP BY).
        print("\n11) Numero di prestiti per ciascun utente:")
        cursor.execute("""
            SELECT utente, COUNT(*) AS num_prestiti
            FROM Prestiti
            GROUP BY utente
        """)
        prestiti_per_utente = cursor.fetchall()
        for utente in prestiti_per_utente:
            print(f"Utente: {utente[0]}, Numero prestiti: {utente[1]}")

        # Query 12: Libri ordinati per genere e poi per anno (usa ORDER BY multiplo)
        print("\n12) Libri ordinati per genere e poi per anno:")
        cursor.execute("""
            SELECT titolo, anno, genere
            FROM Libri
            ORDER BY genere, anno DESC
        """)
        libri_ordinati = cursor.fetchall()
        for libro in libri_ordinati:
            print(f"Titolo: {libro[0]}, Anno: {libro[1]}, Genere: {libro[2]}")

        # Query 13: Prestiti restituiti (dove data_restituzione non è NULL).
        print("\n13) Prestiti restituiti:")
        cursor.execute("""
            SELECT Prestiti.id, Libri.titolo, Prestiti.utente, Prestiti.data_prestito, Prestiti.data_restituzione
            FROM Prestiti
            JOIN Libri ON Prestiti.libro_id = Libri.id
            WHERE Prestiti.data_restituzione IS NOT NULL
        """)
        prestiti_restituiti = cursor.fetchall()
        for prestito in prestiti_restituiti:
            print(f"ID Prestito: {prestito[0]}, Titolo Libro: {prestito[1]}, Utente: {prestito[2]}, Data Prestito: {prestito[3]}, Data Restituzione: {prestito[4]}")

        # Query 14:Autori e numero di libri, inclusi quelli senza libri (usa LEFT JOIN e GROUP BY)
        print("\n14) Autori e numero di libri, inclusi quelli senza libri:")
        cursor.execute("""
            SELECT Autori.nome, Autori.cognome, COUNT(Libri.id) AS num_libri
            FROM Autori
            LEFT JOIN Libri ON Autori.id = Libri.autore_id
            GROUP BY Autori.id
        """)
        autori_con_libri = cursor.fetchall()
        for autore in autori_con_libri:
            print(f"Nome: {autore[0]}, Cognome: {autore[1]}, Numero libri: {autore[2]}")
    finally:
        # Chiusura connessione
        conn.close()
        print("\nConnessione chiusa.")
