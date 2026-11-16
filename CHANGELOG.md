# Historique des versions

Le format s'inspire de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/).

## [2.0.0] – 2026-11-16

Refonte complète des deux projets : correction des défauts, restructuration, tests et intégration continue.

### Formulaire d'alerte (Django)

#### Corrigé

- **Les alertes peuvent enfin être enregistrées.** Auparavant, la source de l'alerte s'affichait sous la forme d'une case à cocher unique qui renvoyait `True` ou `False`. Ces valeurs étant refusées par le champ, aucune alerte ne pouvait être enregistrée. Les 8 sources sont maintenant proposées sous forme de boutons radio.
- **Le projet démarre.** Le projet hôte (`config/`) était absent et un import de `forms.py` était cassé. Les migrations et la liste des dépendances (`requirements.txt`) ont été ajoutées.
- **Des dates incohérentes produisent un message d'erreur au lieu d'une erreur serveur 500.** Le contrôle a été déplacé de `save()` vers `clean()`. Une contrainte en base de données le complète.
- **Le gabarit HTML est bien formé** : une balise `</div>` en trop a été supprimée.
- **La mise en page du formulaire est appliquée.** Le gabarit utilise maintenant la mise en page définie dans `FormHelper`, que crispy-forms ignorait jusqu'ici.
- **Le numéro de téléphone est réellement contrôlé** : de 7 à 15 chiffres, sans lettres.

#### Ajouté

- Champs obligatoires : identifiant, date et heure de l'alerte, source.
- Identifiant unique.
- Champ « Précision » affiché lorsque la source est « Autre ».
- Redirection et message de confirmation après l'enregistrement (motif *Post/Redirect/Get*).
- Administration complète : filtres, recherche, navigation par date.
- 23 tests automatisés.
- Configuration par variables d'environnement et réglages de sécurité pour la production.

#### Supprimé

- Le widget `CustomCheckbox`, ainsi que la dépendance à jQuery et à Font Awesome.

### Notebook PlantVillage

#### Corrigé

- **Le prétraitement correspond à celui des poids ImageNet.** Les pixels sont désormais ramenés dans [-1, 1], alors qu'ils l'étaient dans [0, 1].
- **Un jeu de test indépendant a été ajouté.** Le découpage est désormais en trois jeux (70 / 15 / 15 %) et stratifié ; l'évaluation finale porte sur le jeu de test.
- **Les fichiers ne sont plus déplacés** : le notebook peut être réexécuté autant de fois que nécessaire.
- **Les classes vides sont détectées et signalées.** Auparavant, elles étaient comptées en silence : seules 4 des 15 classes contenaient réellement des images.

#### Ajouté

- Entraînement en deux phases : la tête seule, puis l'affinage des dernières couches.
- Chaque modèle est entraîné à sa taille d'entrée native (299 px pour InceptionV3, 224 px pour MobileNetV2).
- Poids de classe pour compenser le déséquilibre entre classes.
- Évaluation détaillée : F1 macro, rapport par classe, matrice de confusion, taille et temps d'inférence des modèles.
- Fichiers de traçabilité : découpage, paramètres, résultats.
- Exécution du notebook de bout en bout dans l'intégration continue, sur données synthétiques.

#### Supprimé

- Les sorties enregistrées : le fichier passe de 2,9 Mo à 32 Ko.

### Dépôt

- Les deux projets sont rangés chacun dans son dossier.
- Ajout du `.gitignore`, de la configuration de ruff et de l'intégration continue GitHub Actions.

## [1.1.0] – 2024-05-18

- Ajout du notebook de classification PlantVillage (InceptionV3, MobileNetV2).

## [1.0.0] – 2023-05-28

- Première version des fichiers de l'application Django « Alerte et investigation ».
