# Détection de maladies des plantes : InceptionV3 vs MobileNetV2

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Eliaum/formulaire/blob/main/classification-plantvillage/Modele_InceptionV3_et_MobileNetV2.ipynb)

Ce notebook classe des photos de feuilles de **poivron, de pomme de terre et de tomate** en 15 classes, saines ou malades, issues du jeu de données PlantVillage [1]. Il compare deux réseaux pré-entraînés sur ImageNet et adaptés par **apprentissage par transfert** (TensorFlow / Keras) :

- **InceptionV3** : environ 21,8 millions de paramètres, entrée en 299 × 299 ;
- **MobileNetV2** : environ 2,3 millions de paramètres, entrée en 224 × 224, conçu pour les appareils mobiles.

## Méthode

| Étape | Choix | Justification |
|---|---|---|
| Inventaire | Étiquette = nom du dossier parent ; doublons, fichiers illisibles et classes trop petites écartés, avec un message | Gère les copies imbriquées et les restes d'exécutions précédentes |
| Découpage | 70 / 15 / 15 % (entraînement / validation / test), **stratifié**, graine fixée ; aucun fichier n'est déplacé | Jeu de test indépendant ; notebook réexécutable |
| Déséquilibre | Poids de classe (`compute_class_weight("balanced")`) | Les petites classes comptent autant dans la perte |
| Prétraitement | `Rescaling(1/127.5, offset=-1)` intégré au modèle | Reproduit exactement le `preprocess_input` des deux réseaux, qui ramène les pixels dans [-1, 1] |
| Augmentation | Retournements horizontal et vertical, rotation (±36°), zoom (±10 %) | Active seulement pendant l'entraînement |
| Phase 1 | Réseau de base gelé, tête entraînée (Adam, 1e-3) | Adapte la couche de classification sans détruire les poids ImageNet |
| Phase 2 | Dégel des 25 % dernières couches, hors BatchNorm (Adam, 1e-5) | Affinage stable des couches de haut niveau |
| Contrôle | Arrêt anticipé, réduction du taux d'apprentissage, sauvegarde du meilleur modèle selon la perte de validation | Évite le surapprentissage |
| Évaluation | Sur le **jeu de test** : exactitude, F1 macro et pondéré, rapport par classe, matrice de confusion, taille et temps d'inférence | Comparaison chiffrée de la précision et du coût |

## Exécution

1. **Données.** Placez le jeu PlantVillage dans Google Drive, avec un sous-dossier par classe : `Pepper__bell___Bacterial_spot/`, `Tomato_healthy/`, etc. Deux emplacements sont possibles :
   - le dossier `My Drive/Datasets/PlantVillage/` ;
   - l'archive `My Drive/archive.zip`.
2. **Ouverture.** Ouvrez le notebook avec le badge **Open in Colab** ci-dessus, puis choisissez un GPU (*Exécution › Modifier le type d'exécution*).
3. **Paramètres.** Ajustez au besoin la première cellule de code : chemins, tailles d'image, nombre d'époques, `MAX_IMAGES_PER_CLASS` pour un essai rapide.
4. **Lancement.** *Exécution › Tout exécuter*.

Pour l'exécuter hors de Colab, installez les dépendances avec `pip install -r requirements.txt`, puis adaptez `DATA_DIR` et `OUTPUT_DIR`.

### Fichiers produits dans `OUTPUT_DIR`

| Fichier | Contenu |
|---|---|
| `InceptionV3.keras`, `MobileNetV2.keras` | Meilleur modèle de chaque architecture, prétraitement inclus (il accepte des images brutes de 0 à 255) |
| `classes.json` | Ordre des classes en sortie du modèle |
| `decoupage.csv` | Affectation de chaque image à l'entraînement, à la validation ou au test |
| `*_historique.csv`, `courbes_apprentissage.png` | Perte et exactitude à chaque époque |
| `*_rapport_test.txt`, `matrices_confusion.png` | Précision, rappel et F1 par classe sur le jeu de test |
| `comparaison_test.csv`, `resultats.json` | Tableau comparatif et paramètres de l'expérience |

## Vérification du code

Le workflow d'intégration continue exécute le notebook **de bout en bout** avec [papermill](https://papermill.readthedocs.io/), sur un petit jeu d'images synthétiques produit par [`tests/creer_donnees_test.py`](tests/creer_donnees_test.py). Les poids ImageNet sont réels ; les images sont petites (96 × 96) et l'entraînement court (2 + 2 époques).

Ce jeu synthétique reproduit volontairement les pièges du jeu réel :
- doublons dans une copie imbriquée ;
- ancien dossier `train/` ;
- fichier corrompu ;
- fichier sans extension ;
- classe trop petite.

Ce test vérifie que tout le pipeline fonctionne. Les scores qu'il produit n'ont **aucune valeur scientifique**.

## Résultats

Les scores sur le jeu complet doivent être produits par une exécution sur GPU. Ils seront reportés ici, accompagnés du notebook exécuté.

> **Historique.** La première version du notebook (mai 2024, consultable dans l'historique Git) affichait 100 % d'exactitude en validation. Ce score n'était pas représentatif, pour quatre raisons :
> - seules 4 des 15 classes contenaient des images dans les données utilisées ;
> - il n'y avait pas de jeu de test ;
> - le prétraitement ne correspondait pas à celui des poids pré-entraînés ;
> - les fichiers étaient déplacés, ce qui empêchait de réexécuter le notebook.
>
> La version actuelle corrige ces quatre points.

## Limites

- Les photos PlantVillage sont prises dans des conditions homogènes. Une bonne performance sur ce jeu ne garantit pas une bonne performance sur des photos prises au champ.
- Chaque modèle n'est entraîné qu'une fois. Pour conclure qu'une architecture est meilleure, il faudrait répéter l'expérience avec plusieurs graines.
- Sur GPU, certaines opérations ne sont pas déterministes : des écarts de quelques millièmes entre deux exécutions sont possibles. Sur CPU, deux exécutions de test ont donné des scores identiques.

## Référence

[1] D. P. Hughes et M. Salathé, *An open access repository of images on plant health to enable the development of mobile disease diagnostics*, arXiv:1511.08060, 2015. <https://arxiv.org/abs/1511.08060>
