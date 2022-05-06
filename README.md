# LITReview

## Table des matières
1. [Informations générales](#Informations_générales)
2. [Technologies](#technologies)
3. [Installation](#installation)
4. [Exécution](#Exécution)
5. [Vue générale du site](#Screenshot)
6. [Conformité du code aux directives PEP 8](#Conformité_PEP_8)

## Informations_générales
***
Application web permettant à une communauté d'utilisateurs de consulter ou de solliciter une critique de livres 
ou d'articles. 
+ Inscription & authentification des utilisateurs
+ Flux des demandes et réponses de critiques
+ Gestion des abonnements de suivi d'autres utilisateurs
+ Modification/Suppression des publications

## Technologies
***
Technologies ou packages majeurs utilisés dans ce projet :
* [windows 10 Famille](https://docs.microsoft.com/fr-fr/windows/whats-new/whats-new-windows-10-version-21h2) : version 21H2 
* [python](https://docs.python.org/fr/3.10/) : version 3.10.0
* [django](https://docs.djangoproject.com/fr/4.0/) : version 4.0.3
* [pillow](https://pillow.readthedocs.io/en/stable/index.html) : version 9.0.1
* [django-widget-tweaks](https://pypi.org/project/django-widget-tweaks/) : version 1.4.12
* [rules](https://pypi.org/project/rules/) : version 3.3

## Installation
***
Réaliser l'installation sous Windows avec le terminal PowerShell 

Le clonage (git clone) se fait dans le répertoire LITReview. Vous installez ensuite les dépendances du projet après 
avoir généré et activé l'environnement virtuel.
```
$ git clone https://github.com/FredericTNT/LITReview
$ cd LITReview
$ python -m venv venv
$ venv/Scripts/activate
(venv)$ pip install -r requirements.txt
```

## Exécution
***
Rendez-vous à la racine du répertoire litreview. Le serveur d'application se lance en exécutant le programme manage.py
dans l'environnement virtuel activé.

```
(venv)$ cd litreview
(venv)$ python manage.py runserver
```

La base SQLite de l'application (db.sqlite3) et le programme manage.py se situent dans le répertoire
LITReview\litreview

Lorsque le serveur fonctionne, l'application est accessible via un navigateur web à 
l'url suivante : http://localhost:8000/

## Screenshot
***
Connectez-vous...
<img src="/litreview/static/screenshot/login.jpg" alt="login" />

Flux des publications...
<img src="/litreview/static/screenshot/flux.jpg" alt="flux" />

## Conformité_PEP_8
***
La vérification de conformité du code aux directives PEP 8 peut s'effectuer en exécutant le programme flake8.exe 
à partir du répertoire courant LITReview avec les paramètres suivants et l'installation préalable des deux modules 
flake8 et flake8-html dans l'environnement virtuel activé :
```
(venv)$ pip install flake8
(venv)$ pip install flake8-html

(venv)$ venv\scripts\flake8.exe --show-source --statistics --max-line-length=120 --exclude=litreview\*\migrations --format=html --htmldir=flake8_rapport litreview\
```
Un rapport index.html est généré dans le sous-répertoire flake8_rapport avec la liste des éventuels points de
non-conformité.

<img src="/litreview/static/screenshot/Flake8.jpg" alt="PEP8" />
<!---
## FAQs
-->
