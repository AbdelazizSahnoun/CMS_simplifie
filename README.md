# Description du projet :

Le projet consiste à récupérer un ensemble de données provenant de la ville de Montréal et d'offrir des

services à partir de ces données. Il s'agit de données ouvertes à propos d'installations pour faire des

activités sportives.


# Points développées :

**A1 15xp**
Trois listes de données doivent être obtenues à l'aide de requêtes HTTP et leur contenu doit être stocké
dans une base de données SQLite.

La liste des piscines et installations aquatiques en format CSV :
https://data.montreal.ca/dataset/4604afb7-a7c4-4626-a3ca-e136158133f2/resource/cbdca706-569e-
4b4a-805d-9af73af03b14/download/piscines.csv

La liste des patinoires en format XML :
https://data.montreal.ca/dataset/225ac315-49fe-476f-95bd-a1ce1648a98c/resource/5d1859cc-2060-
4def-903f-db24408bacd0/download/l29-patinoire.xml

La liste des aires de jeux d'hiver (glissades) en format XML :
[http://www2.ville.montreal.qc.ca/services_citoyens/pdf_transfert/L29_GLISSADE.xml](http://www2.ville.montreal.qc.ca/services_citoyens/pdf_transfert/L29_GLISSADE.xml)

Vous devez organiser la structure de vos données de façon à minimiser le nombre de requêtes faites à la
BD pour les fonctionnalités que vous réaliserez dans votre projet. N'hésitez pas à changer la
modélisation des données.

**A2 5xp**
L'importation de données du point A1 est faite automatiquement chaque jour à minuit à l’aide d’un
BackgroundScheduler.

**A3 5xp**
Le système écoute les requêtes HTTP sur le port 5000. La route « /doc » fait apparaître la
documentation de tous les services REST. La documentation est en format HTML, généré à partir de
fichiers RAML. Intégrez la fonctionnalité du point A2 à l’application Flask créée au point A3.

**A4 10xp**
Le système offre un service REST permettant d'obtenir la liste des installations pour un arrondissement
spécifié en paramètre. Les données retournées sont en format JSON.
Ex. GET /api/installations?arrondissement=LaSalle


**B1 10xp**
Le système détecte les nouvelles installations depuis la dernière importation de données, en dresse une
liste sans doublon et l'envoi par courriel automatiquement. L'adresse du destinataire du courriel est
stockée dans un fichier de configuration en format YAML.

**B2 10xp**
Les noms des nouvelles installations sont publiés automatiquement sur un compte Twitter.

**C1 10xp**
Le système offre un service REST permettant d'obtenir la liste des installations dont les données ont été
mises à jour en 2021. Pour chaque installation, on indique toute l'information connue. La liste est triée
en ordre croissant du nom de l'installation.

**C2 10xp**
Le système offre un service permettant d'obtenir exactement les mêmes données que le point C1 mais
en format XML. L'encodage de caractères doit être UTF-8.

**C3 5xp**
Le système offre un service permettant d'obtenir exactement les mêmes données que le point C1 mais
en format CSV. L'encodage de caractères doit être UTF-8.

**D1 15xp**
Le système offre un service REST permettant de modifier l'état d'une glissade. Le client doit envoyer
un document JSON contenant les modifications à apporter à la glissade. Le document JSON doit être
validé avec json-schema.

**D2 5xp**
Le système offre un service REST permettant de supprimer une glissade.

	

## Comment tester?

### A1) 

On doit instancier la base de données(database.db) au préalable avec db.sql. Ensuite on démarre l'application flask, il faudra attendre un petit moment avant que toutes les données soient téléchargées dans la base de données, cela peut prendre un bon 5-15 mins. L'importation de départ se fait une fois uniquement, les autres fois, le programme vérifie si les bases de données existent (possède au moins 1 élément) et il ne fait l'importation que si elle n'existe pas, il faudra donc supprimer la base de données et réinstancier une deuxième fois la base de données avec db.sql pour faire une nouvelle importation. 

### A2)

Ce point peut être testé en modifiant la ligne suivante dans `index.py`:

```
 sched.add_job(get_db().intialiaze_all,'cron',hour='00', minute='00'
```
On change les valeurs de `hour` et de `minute` pour les valeurs qu'on veut, et on démarre le programme, le programme va faire l'importation quotidienne en arrière-plan à l'heure spécifié. L'importation peut prendre un bon moment(10 min).
### A3)


La page principale redirige automatiquement vers `/doc` une fois que toutes les importations sont faites, sinon on peut y accéder avec le localhost au port 5000 en spécifiant `/doc`. 

### A4)

Cette fonctionnalité est disponible ici :
`/api/installations/arrondissement/<nom_arr>`, il faut spécifier le nom d'un arrondissement de Montréal et cela devrait  retourner les bonnes informations.



### B1)

On peut tester cette fonctionnalité avec la fonction suivante en la décommentant :

`get_db().testAddNewInstallations()`

Elle est au départ déjà préalablement configuré, elle permet d'insérer une nouvelle ligne dans chacun des trois tableaux de la base de données(installation_aquatiques,patinoires,glissades). Le programme détectera automatiquement ces nouvelles insertions comme étant nouvelles  et va envoyer un courriel et va les poster sur twitter, il faut spécifier dans le fichier Yaml, les informations liées au courriel et ceux liées au Twitter. Si la ligne existe déjà, l'insertion n'a pas lieu et les fonctionnalités email et tweet ne vont rien envoyer. Il faut donc modifier le nom de l'installation qu'on veut insérer car le programme distingue les nouvelles installations avec le nom et pas l'id.


### B2)

C'est la même chose que pour le point B1, il faut spécifier les informations de twitter sur Yaml et utliser la fonction mentionnée au B1 pour tester cette fonctionnalité.

### C1)


Cette fonctionnalité est disponible ici :
`/api/installations/recentes`.

### C2)

Cette fonctionnalité est disponible ici :
`/api/installations/recentes/xml`.

### C2)

Cette fonctionnalité est disponible ici :
`/api/installations/recentes/csv`.Le fichier csv est séparé par des virgules.

### D1)

Cette fonctionnalité est disponible ici :
`/api/installations/glissades/<id>`, cette route supporte `GET` et `POST` donc on peut `GET` pour voir l'état de la glissade et `POST` pour la modifier. Les id à mettre corresponde aux id dans la table Glissade dans la base de données.


### D2)

Cette fonctionnalité est disponible ici :
`/api/installations/glissades/<id>`, cette route supporte `GET` et `DELETE` donc on peut `GET` pour voir l'état de la glissade et `DELETE` pour la supprimer. Les id à mettre corresponde aux id dans la table Glissade dans la base de données.
