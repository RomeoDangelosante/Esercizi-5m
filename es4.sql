-- database: :memory:
CREATE TABLE Studenti(
    matricola int PRIMARY KEY,
    nome VARCHAR(30) not NULL,
    cognome VARCHAR(50) not NULL
);
INSERT INTO Studenti(matricola, nome, cognome) VALUES
(101, 'Mario', 'Rossi'),
(102, 'Lucia', 'Bianchi');


CREATE TABLE Esami(
    id int PRIMARY KEY,
    corso VARCHAR(30) not NULL,
    voto int not NULL,
    matricola int not NULL,
    FOREIGN KEY(matricola) REFERENCES Studenti(matricola)
)