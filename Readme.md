# FL45K-MU51C

## Description

FL45K-MU51C est un mini-site exploitant une base de données d'albums de musique. Il s'agit à l'origine d'un exercice donné aux étudiant d'Année Spéciale de la section Informatique de l'IUT d'orléans en avril 2017.

En tant que simple visiteur, vous pouvez consulter :
 - La liste des albums disponibles dans la base de données
 - La liste des artistes interprètes des albums et une liste de leurs albums
 - La liste des genres musicaux présents
 - La page descriptive d'un album qui, selon si l'album est présent sur Deezer,
 vous permettra davoir la liste des pistes et d'écouter un extrait de celle-ci.

Vous avez la possibilité de vous inscrire sur le site via un formulaire.
Vous pourrez ensuite vous connecter a votre compte, ce qui vous permettra :
- L'ajouter, la modification ou la suppression d'un album.


## Installation

1. Copier ce dossier à l'endroit désiré sur votre serveur web.

2. Vérifier que votre installation de python contient les modules listés dans le fichier requirements.txt. Vous pouvez également utiliser pip pour gérer cette étape avec la commande
```bash
pip install -r requirements.txt
```

3. Accorder les droits d'execution au fichier manage.py
```bash
chmod u+x manage.py
```
4. Créér la base de données du site avec la commande
```bash
./manage.py loaddb chemin/vers/votre/fichier/yaml/contenant/les/informations/des/albums
```
Un fichier extraits.py se trouve dans application/static si vous avez besoin d'un exemple sur la structure yaml. Veiller a alimenter le fichier application/static/img avec les images des albums.

5. Lancer le serveur avec la commande
```bash
./manage.py runserver -h 127.0.0.1 -p 5000
```
Ceci rendra la site accessible à l'adresse 127.0.0.1:5000. Vous pouvez changer ces parametres si vous le désirez.

Vous pourrez ensuite accéder au site.

## Détails techniques

Site réalisé en Flask, selon un modèle de données SQLite géré par SQLAlchemy. Le CSS est en grande majorité celui de Bootstrap.

Ce site utilise aussi l'API Deezer pour la récupération des informations des pistes des albums et leurs extraits.
