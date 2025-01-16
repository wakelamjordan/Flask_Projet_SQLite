import sqlite3

connection = sqlite3.connect('database2.db')

with open('schema2.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
    
cur.execute("INSERT INTO user (login, password) VALUES (?, ?)", ('jdoe', 'password123'))
cur.execute("INSERT INTO user (login, password) VALUES (?, ?)", ('asmith', 'securepwd'))
cur.execute("INSERT INTO user (login, password) VALUES (?, ?)", ('bjackson', 'mypassword'))
cur.execute("INSERT INTO user (login, password) VALUES (?, ?)", ('clara', '12345'))
cur.execute("INSERT INTO user (login, password) VALUES (?, ?)", ('nathan', 'qwerty'))

# Table livres
cur.execute("INSERT INTO livres (titre, auteur, stock) VALUES (?, ?, ?)", ('1984', 'George Orwell', 5))
cur.execute("INSERT INTO livres (titre, auteur, stock) VALUES (?, ?, ?)", ('Le Petit Prince', 'Antoine de Saint-Exupéry', 3))
cur.execute("INSERT INTO livres (titre, auteur, stock) VALUES (?, ?, ?)", ('Harry Potter à l\'école des sorciers', 'J.K. Rowling', 7))
cur.execute("INSERT INTO livres (titre, auteur, stock) VALUES (?, ?, ?)", ('L\'Alchimiste', 'Paulo Coelho', 4))
cur.execute("INSERT INTO livres (titre, auteur, stock) VALUES (?, ?, ?)", ('Pride and Prejudice', 'Jane Austen', 2))

# Table emprunt
cur.execute("INSERT INTO emprunt (user_id, livre_id, date_retour) VALUES (?, ?, ?)", (1, 2, '2025-01-20'))
cur.execute("INSERT INTO emprunt (user_id, livre_id, date_retour) VALUES (?, ?, ?)", (2, 3, '2025-01-22'))
cur.execute("INSERT INTO emprunt (user_id, livre_id, date_retour) VALUES (?, ?, ?)", (3, 1, '2025-01-25'))
cur.execute("INSERT INTO emprunt (user_id, livre_id, date_retour) VALUES (?, ?, ?)", (4, 5, '2025-01-18'))
cur.execute("INSERT INTO emprunt (user_id, livre_id, date_retour) VALUES (?, ?, ?)", (5, 4, '2025-01-30'))

connection.commit()
connection.close()