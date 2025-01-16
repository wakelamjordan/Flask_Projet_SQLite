-- PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  login TEXT NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS livres (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  titre TEXT NOT NULL,
  auteur TEXT NOT NULL,
  stock INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS emprunt (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  livre_id INTEGER NOT NULL,
  date_emprunt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  date_retour DATE DEFAULT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (livre_id) REFERENCES livres (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE VIEW vue_livres AS
SELECT 
    l.id AS livre_id,
    l.titre,
    l.auteur,
    l.stock,
    COUNT(e.id) AS nombre_emprunts
FROM 
    livres l
LEFT JOIN 
    emprunt e ON l.id = e.livre_id
GROUP BY 
    l.id;

