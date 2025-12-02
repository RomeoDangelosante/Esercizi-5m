-- Schema for beekeeping database
CREATE TABLE Typology (
    id INT PRIMARY KEY,
    typology_name VARCHAR(50) NOT NULL,
    typology_description VARCHAR(300)
);

CREATE TABLE Honey (
    id INT PRIMARY KEY,
    denomination VARCHAR(50) NOT NULL,
    typology_id INT,
    FOREIGN KEY (typology_id) REFERENCES Typology(id)
);

CREATE TABLE Beekeeper (
    id INT PRIMARY KEY,
    beekeeper_name VARCHAR(50) NOT NULL
);

CREATE TABLE Apiary (
    code INT PRIMARY KEY,
    num_hives INT NOT NULL,
    locality VARCHAR(300) NOT NULL,
    comune VARCHAR(300) NOT NULL,
    province VARCHAR(300) NOT NULL,
    region VARCHAR(300) NOT NULL,
    beekeeper_id INT,
    FOREIGN KEY (beekeeper_id) REFERENCES Beekeeper(id)
);

CREATE TABLE Production (
    id INT PRIMARY KEY,
    year INT,
    quantity FLOAT,
    apiary_code INT,
    honey_id INT,
    FOREIGN KEY (apiary_code) REFERENCES Apiary(code),
    FOREIGN KEY (honey_id) REFERENCES Honey(id)
);

-- Insert sample data
INSERT INTO Typology (id, typology_name, typology_description) VALUES
(1, 'Monofloral', 'Miele prodotto prevalentemente da un unico fiore'),
(2, 'Polyfloral', 'Miele di millefiori, raccolto da più specie floreali'),
(3, 'Honeydew', 'Miele prodotto a partire dal melato (secrezioni di insetti)');

INSERT INTO Beekeeper (id, beekeeper_name) VALUES
(1, 'Marco Rossi'),
(2, 'Lucia Bianchi'),
(3, 'Alessandro Verdi');

INSERT INTO Honey (id, denomination, typology_id) VALUES
(1, 'Acacia', 1),
(2, 'Castagno', 1),
(3, 'Millefiori', 2),
(4, 'Eucalipto', 2),
(5, 'Melata di Bosco', 3);

INSERT INTO Apiary (code, num_hives, locality, comune, province, region, beekeeper_id) VALUES
(100, 12, 'Fattoria Le Rose', 'San Pietro', 'Pisa', 'Toscana', 1),
(101, 8, 'Colle Verde', 'Montevarchi', 'Arezzo', 'Toscana', 2),
(102, 20, 'Bosco Alto', 'Vercelli', 'Vercelli', 'Piemonte', 3),
(103, 5, 'Terrazza Sud', 'Verona', 'Verona', 'Veneto', 1);

INSERT INTO Production (id, year, quantity, apiary_code, honey_id) VALUES
(1, 2022, 120.5, 100, 1),
(2, 2022, 95.2, 101, 3),
(3, 2023, 210.0, 102, 5),
(4, 2023, 34.7, 103, 2),
(5, 2024, 150.0, 100, 3),
(6, 2024, 78.3, 101, 4);

SELECT a.id, a.NOME
FROM APICOLTORE a
JOIN APIARY ap ON ap.APICOLTORE_ID = a.id
JOIN PRODUCTION p ON p.apiary_id = ap.codice
JOIN HONEY h ON h.id = p.honey_id
JOIN TIPOLOGIA_HONEY t ON t.id = h.tipologia_id
WHERE ap.REGIONE = 'Emilia Romagna'
  AND t.NOME = 'DOP';

SELECT 