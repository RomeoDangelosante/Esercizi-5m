import sqlite3

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE Studenti(
    matricola int PRIMARY KEY,
    nome VARCHAR(30) not NULL,
    cognome VARCHAR(50) not NULL
);
""")
cursor.execute("""
CREATE TABLE Esami(
    id int PRIMARY KEY,
    corso VARCHAR(30) not NULL,
    voto int not NULL,
    matricola int not NULL,
    FOREIGN KEY(matricola) REFERENCES Studenti(matricola)
);
""")

cursor.executemany(
    "INSERT INTO Studenti(matricola, nome, cognome) VALUES (?, ?, ?);",
    [
        (101, 'Mario', 'Rossi'),
        (102, 'Lucia', 'Bianchi')
    ]
)
cursor.executemany(
    "INSERT INTO Esami(id, corso, voto, matricola) VALUES (?, ?, ?, ?);",
    [
        (1, 'Matematica', 28, 101),
        (2, 'Informatica', 30, 101),
        (3, 'Fisica', 26, 101),
        (4, 'Matematica', 24, 102),
        (5, 'Informatica', 27, 102),
        (6, 'Fisica', 29, 102)
    ]
)

print("Elenco studenti:")
for row in cursor.execute("SELECT matricola, nome, cognome FROM Studenti;"):
    print(row)

print("\nCorsi e voti per studente 101:")
for row in cursor.execute("SELECT corso, voto FROM Esami WHERE matricola = 101;"):
    print(row)

print("\nNumero di esami per ciascuno studente:")
for row in cursor.execute("SELECT matricola, COUNT(*) AS numero_esami FROM Esami GROUP BY matricola;"):
    print(row)

print("\nNome, cognome e corso per ogni esame:")
for row in cursor.execute("""
SELECT Studenti.nome, Studenti.cognome, Esami.corso
FROM Studenti
INNER JOIN Esami ON Studenti.matricola = Esami.matricola;
"""):
    print(row)

conn.close()
