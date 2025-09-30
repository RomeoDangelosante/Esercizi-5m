-- database: :memory:
CREATE TABLE Tipologia(
    id INT PRIMARY KEY,
    nome VARCHAR(20)NOT NULL,
    descrizione VARCHAR(100)
);

CREATE TABLE Miele(
    id INT PRIMARY KEY,
    denominazione VARCHAR(20)NOT NULL,
    tipologia_id INT NOT NULL,
    FOREIGN KEY(tipologia_id) REFERENCES Tipologia(id)
);

CREATE TABLE Apicoltore(
    id INT PRIMARY KEY,
    nome VARCHAR(20)NOT NULL
);

CREATE TABLE Apiario(
    id INT PRIMARY KEY,
    numero_arnie INT NOT NULL,
    localita VARCHAR(100) NOT NULL,
    comune VARCHAR(20),
    provincia VARCHAR(20),
    regione VARCHAR(20),
    apicoltore_id INT,
    FOREIGN KEY (apicoltore_id) REFERENCES Apicoltore(id)
);

CREATE TABLE Produzione(
    id INT PRIMARY KEY,
    anno INT NOT NULL,
    quantita FLOAT NOT NULL,
    miele_id INT,
    apiario_id INT,
    FOREIGN KEY (miele_id) REFERENCES Miele(id),
    FOREIGN KEY (apiario_id) REFERENCES Apiario(id)
);

INSERT INTO Tipologia(id, nome) VALUES
(1, 'Acacia'),
(2, 'Castagno'),
(3, 'Millefiori');

INSERT INTO Miele(id, denominazione, tipologia_id) VALUES
(1, 'Miele di Acacia', 1),
(2, 'Miele di Castagno', 2),
(3, 'Miele Millefiori', 3);
UPDATE Miele
SET denominazione = 'Miele di Castagno Nero IGP'
WHERE id = 1;
UPDATE Miele
SET denominazione = 'Miele di Acacia Biologico'
WHERE id = 2;
UPDATE Miele
SET denominazione = 'Miele Millefiori delle Alpi'
WHERE id = 3;



INSERT INTO Apicoltore(id, nome) VALUES
(1, 'Luca Rossi'),
(2, 'Marco Bianchi'),
(3, 'Giulia Verdi');
UPDATE Apicoltore
SET nome = 'Luca Neri'
WHERE id = 1;
UPDATE Apicoltore
SET nome = 'Marco Blu'
WHERE id = 2;
UPDATE Apicoltore
SET nome = 'Giulia Rosa'
WHERE id = 3;

INSERT INTO Apiario(id, numero_arnie, localita, comune, provincia, regione, apicoltore_id) VALUES
(1, 26, 'Collina Verde', 'Fiorenzuola d''Arda', 'PC', 'Emilia-Romagna', 1),
(2, 37, 'Valle Fiorita', 'San Giovanni in Persiceto', 'BO', 'Emilia-Romagna', 2),
(3, 48, 'Bosco Incantato', 'Parma', 'PR', 'Emilia-Romagna', 3);
UPDATE Apiario
SET regione = 'Lombardia', provincia = 'BG', comune = 'Bergamo', localita = 'Collina Azzurra', numero_arnie = 60
WHERE id = 1;


INSERT INTO Produzione(id, anno, quantita, miele_id, apiario_id) VALUES
(1, 2022, 150.50, 1, 1),
(2, 2022, 200.75, 2, 2),
(3, 2022, 180.00, 3, 3);
UPDATE Produzione
SET anno = 2023, quantita = 160.00
WHERE id = 3;
UPDATE Produzione
set anno = 2024 WHERE id = 1;
UPDATE Produzione
set miele_id = 2 WHERE id = 2;
UPDATE Produzione
set miele_id = 3 WHERE id = 3;

-- 1. Seleziona la quantità totale prodotta per anno.
SELECT YEAR(data_produzione) AS anno, SUM(quantita) AS totale_prodotta
FROM produzione
GROUP BY YEAR(data_produzione);

-- 2. Seleziona la produzione media per apiario.
SELECT apiario_id, AVG(quantita) AS produzione_media
FROM produzione
GROUP BY apiario_id;

-- 3. Seleziona il numero di produzioni e la produzione totale per miele.
SELECT miele_id, COUNT(*) AS numero_produzioni, SUM(quantita) AS produzione_totale
FROM produzione
GROUP BY miele_id;

-- 4. Seleziona la produzione totale per miele nell'anno 2024.
SELECT miele_id, SUM(quantita) AS produzione_totale_2024
FROM produzione
WHERE YEAR(data_produzione) = 2024
GROUP BY miele_id;

-- 5. Seleziona il valore massimo e minimo di produzione per anno.
SELECT YEAR(data_produzione) AS anno, MAX(quantita) AS max_produzione, MIN(quantita) AS min_produzione
FROM produzione
GROUP BY YEAR(data_produzione);

-- 6. Seleziona gli apiari la cui produzione totale supera 200.
SELECT apiario_id, SUM(quantita) AS produzione_totale
FROM produzione
GROUP BY apiario_id
HAVING SUM(quantita) > 200;

-- 7. Seleziona la produzione totale per tipologia di miele (typology_id).
SELECT typology_id, SUM(quantita) AS produzione_totale
FROM produzione
GROUP BY typology_id;

-- 8. Seleziona il numero di mieli per ciascuna tipologia.
SELECT typology_id, COUNT(DISTINCT miele_id) AS numero_mieli
FROM miele
GROUP BY typology_id;

-- 9. Seleziona la produzione totale per apicoltore (beekeeper_id).
SELECT beekeeper_id, SUM(quantita) AS produzione_totale
FROM produzione
GROUP BY beekeeper_id;

-- 10. Seleziona la produzione media per arnia (produzione totale divisa per num_hives) per apiario.
SELECT apiario_id, SUM(quantita) / SUM(num_hives) AS produzione_media_per_arnia
FROM produzione
GROUP BY apiario_id;

-- 11. Seleziona per ogni anno il conteggio delle produzioni con quantità maggiore di 100.
SELECT YEAR(data_produzione) AS anno, COUNT(*) AS produzioni_over_100
FROM produzione
WHERE quantita > 100
GROUP BY YEAR(data_produzione);

-- 12. Seleziona per ogni miele e anno la somma delle quantità.
SELECT miele_id, YEAR(data_produzione) AS anno, SUM(quantita) AS totale
FROM produzione
GROUP BY miele_id, YEAR(data_produzione);