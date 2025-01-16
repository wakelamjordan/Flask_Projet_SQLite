-- PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS livres;

CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  login TEXT NOT NULL,
  password TEXT NOT NULL
);

DROP TABLE IF EXISTS livres;

CREATE TABLE IF NOT EXISTS livres (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  titre TEXT NOT NULL,
  auteur TEXT NOT NULL,
  stock INTEGER DEFAULT 0
);

DROP TABLE IF EXISTS emprunt;

CREATE TABLE IF NOT EXISTS emprunt (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  livre_id INTEGER NOT NULL,
  date_emprunt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  date_retour DATE DEFAULT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (livre_id) REFERENCES livres (id) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP VIEW IF EXISTS vue_livres;

CREATE VIEW vue_livres AS
SELECT 
    l.id AS id,
    l.titre AS titre,
    l.auteur AS auteur,
    l.stock AS stock,
    COUNT(e.id) AS emprunt
FROM 
    livres l
LEFT JOIN 
    emprunt e ON l.id = e.livre_id
GROUP BY 
    l.id;

