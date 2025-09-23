CREATE TABLE HONEY(
    id INT PRIMARY KEY,
    DENOMINAZIONE VARCHAR(50) NOT NULL,
    tipologia_id INT,
    FOREIGN KEY (tipologia_id) REFERENCES TIPOLOGIA_HONEY(id)
    
);

CREATE TABLE TIPOLOGIA_HONEY(
    id INT PRIMARY KEY,
    DESCRIZIONE VARCHAR(50) NOT NULL
    NOME VARCHAR(50) NOT NULL    
);

CREATE TABLE PRODUCTION(
    id INT PRIMARY KEY,
    apiary_id INT,
    FOREIGN KEY (apiary_id) REFERENCES APIARY(id),
    honey_id INT,
    FOREIGN KEY (honey_id) REFERENCES HONEY(id),
    anno_produzione int NOT NULL,
    QUANTITA float NOT NULL
);

CREATE TABLE APIARY(
    codice VARCHAR(50) PRIMARY KEY,
    NUMERO_ALVEARI INT NOT NULL,
    posizione VARCHAR(100) NOT NULL,
    COMUNE VARCHAR(50) NOT NULL,
    PROVINCIA VARCHAR(50) NOT NULL,
    REGIONE VARCHAR(50) NOT NULL,
    APICOLTORE_ID INT,
    FOREIGN KEY (APICOLTORE_ID) REFERENCES APICOLTORE(ID)
);

CREATE TABLE APICOLTORE(
    id INT PRIMARY KEY,
    NOME VARCHAR(50) NOT NULL,
);


INSERT INTO TIPOLOGIA_HONEY (id, DESCRIZIONE, NOME) VALUES
(1, 'Millefiori', 'Millefiori'),
(2, 'Acacia', 'Acacia'),
(3, 'Castagno', 'Castagno'),
(4, 'Eucalipto', 'Eucalipto'),
(5, 'Tiglio', 'Tiglio');


INSERT INTO HONEY (id, DENOMINAZIONE, tipologia_id) VALUES
(1, 'Miele di Millefiori', 1),
(2, 'Miele di Acacia', 2),
(3, 'Miele di Castagno', 3),
(4, 'Miele di Eucalipto', 4),
(5, 'Miele di Tiglio', 5);

INSERT INTO APICOLTORE (id, NOME) VALUES
(1, 'Mario Rossi'),
(2, 'Luigi Bianchi'),
(3, 'Giovanni Verdi');

INSERT INTO APIARY (codice, NUMERO_ALVEARI, posizione, COMUNE, PROVINCIA, REGIONE, APICOLTORE_ID) VALUES
('API001', 50, 'Via Roma 1', 'Milano', 'MI', 'Lombardia', 1),
('API002', 30, 'Via Milano 2', 'Torino', 'TO', 'Piemonte', 2),
('API003', 40, 'Via Napoli 3', 'Napoli', 'NA', 'Campania', 3);

INSERT INTO PRODUCTION (id, apiary_id, honey_id, anno_produzione, QUANTITA) VALUES
(1, 'API001', 1, 2022, 100.5),
(2, 'API001', 2, 2022, 80.0),
(3, 'API002', 3, 2022, 60.0),
(4, 'API003', 4, 2022, 90.0),
(5, 'API003', 5, 2022, 70.0);

