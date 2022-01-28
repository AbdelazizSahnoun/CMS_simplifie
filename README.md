
# Création d'un CMS simple

Conception d'un logiciel de type CMS ( _Content Management System_ ), en version
simplifiée. Un CMS permet de gérer le contenu d'un site web, c'est-à-dire d'y mettre des articles, de
spécifier à quel moment ces articles seront publiés, bref de permettre à un non-programmeur de
modifier le contenu de son site web.


### Routes

## GET /

Cette route correspond à la page d'accueil du site. Elle doit afficher les 5 dernières publications en
date du jour (vous ne devez pas afficher les publications avec une date de publication dans le futur).
Pour chaque publication, vous devez afficher toutes les données que vous avez sur la publication.

La page d'accueil doit aussi contenir un champ texte représentant un moteur de recherche. Le texte
entré dans ce champ doit être recherché dans tous les titres et paragraphes connus du CMS. La liste
des articles qui contiennent l'expression recherchée sera retournée dans une page (avec une nouvelle
route, si vous le désirez). Pour chaque article dans le résultat de recherche, vous devez afficher le
titre de l'article et sa date de publication. Le titre sera également un lien vers la page de l'article.

Utilisez l'opérateur LIKE en SQL pour faire la recherche.


## GET /article/<identifiant>

Cette route correspond à la page d'un article en particulier. Vous devez récupérer les données de
l'article identifié par l'URL et afficher les données de l'article. Une page 404 doit être retournée si
l'identifiant n'existe pas.

## GET /admin

Cette route correspond au point d'entrée pour un administrateur de contenu du site web.

La page sur cette route doit présenter la liste de tous les articles connus du logiciel. Pour chaque
article, on présente son titre, la date de publication et un lien vers une page pour modifier l'article.

La page doit aussi contenir un lien vers une page de création d'un nouvel article.

La route à utiliser pour la page de modification d'un article est à votre discrétion. Lors de la
modification d'un article, uniquement le titre et le paragraphe sont modifiables.

## GET /admin-nouveau

Cette route permet d'afficher une page avec un formulaire pour créer un nouvel article. Le
formulaire doit contenir tous les champs requis par la base de données. La route à utiliser pour
envoyer les données au serveur est à votre discrétion. Le serveur doit valider les données selon les
exigences spécifiées dans la section sur la base de données. Également, tous les champs sont
obligatoires. En cas d'erreur de validation, la page du formulaire doit être affichée de nouveau avec
les champs contenant déjà les valeurs soumises (même celles erronées) et les messages d'erreurs
appropriés.





