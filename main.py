# Importer Flask
from flask import Flask, render_template, session, redirect
import os

# Importer le tableau questions[]
from questions import questions
# Import des noms et descriptions des résultats
from resultat import resultats, noms

# Création de l'application 
app = Flask(__name__)
app.secret_key = os.urandom(24)


# Route de la page d'accueil
@app.route('/')
def index():
    # Cookie mémorisant le numéro de la question actuelle
    session["numero_question"] = 0
    # Cookie mémorisant le score pour chaque perso
    session["score"] =  {"M":0, "L":0, "P":0, "B":0, "Y":0, "H": 0}
    return render_template('index.html')

# Route affichant une question
@app.route('/question')
def question():
    # Accèder aux questions qui sont définies ailleurs dans le code
    global questions
    # Récupère le numéro de la question actuelle depuis la session
    numero = session["numero_question"]
    #Si le numéro de la question est inférieur aux nombres de questions
    if numero < len(questions):
        # Extrait l'énoncé de la question actuelle
        enonce = questions[numero]["enonce"]
        
        # Copie la question actuelle pour manipuler séparément les symboles et réponses
        symboles_et_reponses = questions[numero].copy()
        
        # Retire l'énoncé du dictionnaire pour ne garder que les symboles et réponses
        symboles_et_reponses.pop("enonce")
        
        # Crée une liste de symboles (clé de chaque réponse)
        symboles = list(symboles_et_reponses.keys())
        
        # Crée une liste des réponses associées aux symboles
        reponses = list(symboles_et_reponses.values())
        
        # Stocke les symboles actuels dans la session pour un accès dans d'autres routes
        session["symboles"] = symboles

        # Renvoie le template de la question avec les données nécessaires pour l'affichage
        return render_template("question.html", enonce=enonce, reponses=reponses, symboles=symboles)


    # Sinon, toutes les questions ont été répondues
        # alors on on passe au calcul des résultats
    else :
        global resultats  # Accède à la liste globale de descriptions associée aux symboles
        global noms  # Accède à la liste globale de noms associés aux symboles

        # Trie les symboles dans l'ordre décroissant du score pour déterminer le symbole gagnant
        symboles_dans_l_ordre = sorted(session["score"], key=session["score"].get, reverse=True)
        
        # Sélectionne le premier symbole dans l'ordre (symbole avec le score le plus élevé)
        symbole_gagnant = symboles_dans_l_ordre[0]
        
        # Récupère le nom et la description du symbole gagnant
        nom = noms[symbole_gagnant]
        description = resultats[symbole_gagnant]
        
        # Renvoie le template des résultats avec les informations du symbole gagnant
        return render_template("resultat.html", nom=nom, description=description)

# Route prenant en compte la réponse choisie ('numero' est le numéro de la réponse choisie)
@app.route("/reponse/<numero>")
def repondre(numero) :
  # On récupère le symbole choisi
  symbole = session["symboles"][int(numero)]
  # On ajoute 1 au score pour ce symbole
  session["score"][symbole] += 1
  # On passe à la question suivante
  session["numero_question"] += 1
  # On redirige vers la question suivante
  return redirect("/question")

# Route affichant le résultat
@app.route('/resultat')
def resultat():
    return render_template('resultat.html')

# Exécuter l'application
app.run(host='0.0.0.0', port=4200)


