from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions


@app.route('/', methods=['GET'])
def home():
    return render_template('bibliotheque/index.html')


@app.route('/livres', methods=['GET'])
def livres():

    data = query('SELECT * FROM vue_livres;')

    return render_template('bibliotheque/livres.html', data=data)


@app.route('/api/livres', methods=['GET'])
def apiLivres():

    data = query('SELECT * FROM vue_livres;')

    return jsonify(data), 200


@app.route('/api/livre/<titre>', methods=['GET'])
def apiLivre(titre):
    param = "%" + titre + "%"

    # data = query('SELECT * FROM vue_livres WHERE titre=? OR auteur=?;')

    conn = sqlite3.connect('database2.db')

    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM vue_livres WHERE titre LIKE ? OR auteur LIKE ?;',
        (param, param))
    data = cursor.fetchall()

    conn.close()

    return jsonify(data), 200


def estConnecte():
    return session.get('authentifie')


@app.route('/deconnection', methods=['GET'])
def deconnection():
    session.clear()
    # return redirect(url_for('home'))
    return jsonify({"disconnect": True}), 200


@app.route('/connection', methods=['GET', 'POST'])
def connection():

    return jsonify({"connection": True}), 200

    if estConnecte():
        # return redirect(url_for("home"))
        return jsonify({"connection": True}), 200

    if request.method == "POST":
        if request.form['username'] and request.form['password']:
            conn = sqlite3.connect('database2.db')

            cursor = conn.cursor()

            cursor.execute(
                'SELECT * FROM user WHERE login = ? AND password = ? ;',
                (request.form['username'], request.form['password']))

            userIdentifie = cursor.fetchall()

            conn.close()

            if userIdentifie:
                session['authentifie'] = {
                    'role': userIdentifie[0][3],
                    'login': userIdentifie[0][1]
                }
                # return redirect(url_for("home"))
                return jsonify({"connection": True}), 200
            else:
                return jsonify({"connection": False}), 401
                # return render_template('bibliotheque/connection.html',
                #                        error=True)

    # return render_template('bibliotheque/connection.html', error=False)
    return jsonify({"testconnection": True}), 200


def estAdmin():
    role = session.get('authentifie')

    if session.get(
            'authentifie') and session['authentifie']['role'] == 'admin':
        return True

    return False


@app.route('/api/users', methods=['GET'])
def users():
    if not estAdmin():
        return redirect(url_for('home'))

    data = query('SELECT * FROM user;')

    return jsonify(data), 200


# @app.route('/users')
# def users():


def query(sql):
    conn = sqlite3.connect('database2.db')
    cursor = conn.cursor()

    cursor.execute(sql)

    response = cursor.fetchall()

    conn.close()

    return response


@app.route('/api/user/<int:id>', methods=['GET'])
def user(id):
    if not estAdmin():
        return redirect(url_for('home'))

    conn = sqlite3.connect('database2.db')

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user WHERE id = ? ;', (id, ))
    data = cursor.fetchall()

    conn.close()

    return jsonify(data), 200


# @app.route('/users')
# def users():


def query(sql):
    conn = sqlite3.connect('database2.db')
    cursor = conn.cursor()

    cursor.execute(sql)

    response = cursor.fetchall()

    conn.close()

    return response


# # Fonction pour créer une clé "authentifie" dans la session utilisateur
# def est_authentifie():
#     return session.get('authentifie')

# @app.route('/')
# def hello_world():
#     return render_template('hello.html')

# @app.route('/lecture')
# def lecture():
#     if not est_authentifie():
#         # Rediriger vers la page d'authentification si l'utilisateur n'est pas authentifié
#         return redirect(url_for('authentification'))

#   # Si l'utilisateur est authentifié
#     return "<h2>Page Lecture</h2>"

# @app.route('/authentification', methods=['GET', 'POST'])
# def authentification():
#     if request.method == 'POST':
#         # Vérifier les identifiants
#         match request.form['username']:
#             case "admin":
#                 if request.form['password']=='password':

#                     session['authentifie']=True

#                       # Si l'utilisateur est authentifié
#                     return "<h2>Bravo, vous êtes authentifié</h2>"
#                 else:
#                     return render_template('formulaire_authentification.html', error=True)
#             case "user":
#                 if request.form['password']=='12345':
#                     session['authentifie']=True
#                       # Si l'utilisateur est authentifié
#                     return "<h2>Bravo, vous êtes authentifié</h2>"
#                 else:
#                     return render_template('formulaire_authentification.html', error=True)
#             case _:
#                     return render_template('formulaire_authentification.html', error=True)
#         # if request.form['username'] == 'admin' and request.form['password'] == 'password': # password à cacher par la suite
#         #     session['authentifie'] = True
#         #     # Rediriger vers la route lecture après une authentification réussie
#         #     return redirect(url_for('lecture'))
#         # else:
#         #     # Afficher un message d'erreur si les identifiants sont incorrects
#         #     return render_template('formulaire_authentification.html', error=True)

#     return render_template('formulaire_authentification.html', error=False)

# @app.route('/fiche_client/<int:post_id>')
# def Readfiche(post_id):
#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
#     data = cursor.fetchall()
#     conn.close()
#     # Rendre le template HTML et transmettre les données
#     return render_template('read_data.html', data=data)

# @app.route('/consultation/')
# def ReadBDD():
#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM clients;')
#     data = cursor.fetchall()
#     conn.close()
#     return render_template('read_data.html', data=data)

# @app.route('/enregistrer_client', methods=['GET'])
# def formulaire_client():
#     return render_template('formulaire.html')  # afficher le formulaire

# @app.route('/enregistrer_client', methods=['POST'])
# def enregistrer_client():
#     nom = request.form['nom']
#     prenom = request.form['prenom']

#     # Connexion à la base de données
#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()

#     # Exécution de la requête SQL pour insérer un nouveau client
#     cursor.execute('INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)', (1002938, nom, prenom, "ICI"))
#     conn.commit()
#     conn.close()
#     return redirect('/consultation/')  # Rediriger vers la page d'accueil après l'enregistrement

# @app.route('/fiche_nom/<nom>',methods=['GET'])
# def exercice(nom):
#     if not est_authentifie():
#         # Rediriger vers la page d'authentification si l'utilisateur n'est pas authentifié
#         return redirect(url_for('authentification'))

#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM clients WHERE nom = ?', (nom,))
#     data = cursor.fetchall()
#     conn.close()

#   # Si l'utilisateur est authentifié
#     return render_template('exercice.html',data=data)

if __name__ == "__main__":
    app.run(debug=True)
